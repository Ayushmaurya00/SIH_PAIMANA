"""
Feature Engineering & Matrix Construction for ML Models
"""

import sqlite3
import datetime
import numpy as np
import pandas as pd
from typing import Dict, Tuple, List
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


def load_data_from_db(db_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Loads projects, monthly snapshots, and milestones from SQLite database."""
    conn = sqlite3.connect(db_path)
    df_projects = pd.read_sql("SELECT * FROM projects", conn)
    df_snapshots = pd.read_sql("SELECT * FROM monthly_snapshots", conn)
    df_milestones = pd.read_sql("SELECT * FROM milestones", conn)
    conn.close()
    return df_projects, df_snapshots, df_milestones


REFERENCE_DATE = datetime.date(2026, 8, 1)
DAYS_PER_MONTH = 30.44  # unified constant across train/infer/score

def build_feature_matrices(
    df_projects: pd.DataFrame,
    df_snapshots: pd.DataFrame,
    df_milestones: pd.DataFrame,
    ref_date: datetime.date = REFERENCE_DATE,
    train_ids: set | None = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, pd.Series]]:
    """Constructs 'cuf_only' and 'cuf_plus_extra' feature matrices along with target variables."""
    df = df_projects.copy()
    cost_overrun_pct = ((df['revised_cost_cr'] - df['approved_cost_cr']) / df['approved_cost_cr'] * 100.0).clip(lower=0.0)
    has_cost_overrun = (cost_overrun_pct > 1.0).astype(int)

    scheduled_comp = pd.to_datetime(df['scheduled_completion'])
    revised_comp = pd.to_datetime(df['revised_completion'].fillna(df['scheduled_completion']))
    scheduled_start = pd.to_datetime(df['scheduled_start'])
    approval_dt = pd.to_datetime(df['approval_date'])

    time_overrun_months = ((revised_comp - scheduled_comp).dt.days / DAYS_PER_MONTH).clip(lower=0.0)
    has_time_overrun = (time_overrun_months > 0.5).astype(int)

    targets = {
        'cost_overrun_class': has_cost_overrun,
        'cost_overrun_reg': cost_overrun_pct,
        'time_overrun_class': has_time_overrun,
        'time_overrun_reg': time_overrun_months
    }

    planned_duration_months = ((scheduled_comp - scheduled_start).dt.days / DAYS_PER_MONTH).clip(lower=1.0)
    approval_to_start_months = ((scheduled_start - approval_dt).dt.days / DAYS_PER_MONTH).clip(lower=0.0)
    elapsed_months = ((pd.to_datetime(ref_date) - scheduled_start).dt.days / DAYS_PER_MONTH).clip(lower=0.0)

    cuf_base = pd.DataFrame({
        'project_id': df['project_id'], 'approved_cost_cr': df['approved_cost_cr'],
        'cumulative_expenditure_cr': df['cumulative_expenditure_cr'],
        'physical_progress_pct': df['physical_progress_pct'],
        'planned_duration_months': planned_duration_months,
        'approval_to_start_months': approval_to_start_months,
        'elapsed_months': elapsed_months,
        'ministry': df['ministry'], 'sector': df['sector'],
        'implementing_agency': df['implementing_agency'], 'state': df['state']
    })

    milestone_summary = df_milestones.groupby('project_id').agg(
        total_milestones=('milestone_id', 'count'), delayed_milestones=('is_delayed', 'sum')
    ).reset_index()
    milestone_summary['milestone_slippage_ratio'] = milestone_summary['delayed_milestones'] / (milestone_summary['total_milestones'] + 1e-5)

    df_snapshots_sorted = df_snapshots.sort_values(by=['project_id', 'snapshot_month'])
    snap_grouped = df_snapshots_sorted.groupby('project_id').agg(
        progress_start=('physical_progress_pct', 'first'), progress_latest=('physical_progress_pct', 'last'),
        expenditure_start=('cumulative_expenditure_cr', 'first'), expenditure_latest=('cumulative_expenditure_cr', 'last')
    ).reset_index()
    snap_grouped['12m_progress_gain'] = (snap_grouped['progress_latest'] - snap_grouped['progress_start']).clip(lower=0.0)
    snap_grouped['12m_expenditure_gain'] = (snap_grouped['expenditure_latest'] - snap_grouped['expenditure_start']).clip(lower=0.0)

    df_merged = cuf_base.merge(milestone_summary, on='project_id', how='left').fillna(0)
    df_merged = df_merged.merge(snap_grouped[['project_id', '12m_progress_gain', '12m_expenditure_gain']], on='project_id', how='left').fillna(0)

    expenditure_pct = (df_merged['cumulative_expenditure_cr'] / (df_merged['approved_cost_cr'] + 1e-5)) * 100.0
    expenditure_pct = expenditure_pct.clip(0.0, 250.0)
    timeline_elapsed_pct = (df_merged['elapsed_months'] / (df_merged['planned_duration_months'] + 1e-5)) * 100.0
    expenditure_to_progress_ratio = (expenditure_pct / (df_merged['physical_progress_pct'] + 1.0)).clip(upper=10.0)

    # Fix target leakage: compute historical overrun maps only on train split if provided
    _df_for_maps = df[df['project_id'].isin(train_ids)] if train_ids is not None else df
    agency_overrun_map = _df_for_maps.groupby('implementing_agency').apply(lambda g: ((g['revised_cost_cr'] - g['approved_cost_cr']) / g['approved_cost_cr'] > 0.01).mean(), include_groups=False).to_dict()
    sector_overrun_map = _df_for_maps.groupby('sector').apply(lambda g: ((g['revised_cost_cr'] - g['approved_cost_cr']) / g['approved_cost_cr'] > 0.01).mean(), include_groups=False).to_dict()
    state_overrun_map = _df_for_maps.groupby('state').apply(lambda g: ((g['revised_cost_cr'] - g['approved_cost_cr']) / g['approved_cost_cr'] > 0.01).mean(), include_groups=False).to_dict()

    cuf_plus = df_merged.copy()
    cuf_plus['expenditure_pct'] = expenditure_pct
    cuf_plus['timeline_elapsed_pct'] = timeline_elapsed_pct
    cuf_plus['expenditure_to_progress_ratio'] = expenditure_to_progress_ratio
    cuf_plus['expenditure_vs_time_gap'] = (expenditure_pct - timeline_elapsed_pct)
    cuf_plus['progress_vs_time_gap'] = (df_merged['physical_progress_pct'] - timeline_elapsed_pct)
    cuf_plus['agency_historical_overrun_avg'] = cuf_plus['implementing_agency'].map(agency_overrun_map).fillna(0.5)
    cuf_plus['sector_historical_overrun_avg'] = cuf_plus['sector'].map(sector_overrun_map).fillna(0.5)
    cuf_plus['state_historical_overrun_avg'] = cuf_plus['state'].map(state_overrun_map).fillna(0.5)
    cuf_plus['is_megaproject'] = (cuf_plus['approved_cost_cr'] >= 5000.0).astype(int)
    cuf_plus['cost_log'] = np.log1p(cuf_plus['approved_cost_cr'])

    return cuf_base, cuf_plus, targets


def get_preprocessor(df_features: pd.DataFrame) -> Tuple[ColumnTransformer, List[str], List[str]]:
    num_cols = [c for c in df_features.columns if c != 'project_id' and df_features[c].dtype in [np.float64, np.int64, float, int]]
    cat_cols = [c for c in df_features.columns if c != 'project_id' and df_features[c].dtype == object]

    num_pipeline = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
    cat_pipeline = Pipeline([('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')), ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])

    preprocessor = ColumnTransformer(transformers=[('num', num_pipeline, num_cols), ('cat', cat_pipeline, cat_cols)], remainder='drop')
    return preprocessor, num_cols, cat_cols
