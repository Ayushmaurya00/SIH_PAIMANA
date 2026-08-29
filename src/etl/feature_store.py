"""
PAIMANA AI - Dual Feature Store & In-CUF vs. Beyond-CUF Ablation
"""

import os
import datetime
import sqlite3
import pandas as pd
import numpy as np
from typing import Tuple, Optional
from src.etl.indices import SECTOR_COMPLEXITY_INDEX, STATE_LAND_FRICTION_INDEX

REFERENCE_DATE = datetime.date(2026, 8, 1)


def load_telemetry_data(db_path: str = "paimana.db") -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Loads projects, monthly_snapshots, and milestones from SQLite database."""
    conn = sqlite3.connect(db_path)
    df_projects = pd.read_sql("SELECT * FROM projects", conn)
    df_snapshots = pd.read_sql("SELECT * FROM monthly_snapshots", conn)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='milestones'")
    if cur.fetchone():
        df_milestones = pd.read_sql("SELECT * FROM milestones", conn)
    else:
        df_milestones = pd.DataFrame(columns=['project_id', 'milestone_id', 'is_delayed'])
    conn.close()
    return df_projects, df_snapshots, df_milestones


def build_feature_matrices(
    df_projects: pd.DataFrame,
    df_snapshots: pd.DataFrame,
    df_milestones: Optional[pd.DataFrame] = None,
    ref_date: datetime.date = REFERENCE_DATE
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Constructs cuf_only, cuf_plus_extra, and targets dataframes."""
    df = df_projects.copy()
    start_dt = pd.to_datetime(df['scheduled_start'])
    sched_comp_dt = pd.to_datetime(df['scheduled_completion'])
    rev_comp_dt = pd.to_datetime(df['revised_completion'].fillna(df['scheduled_completion']))
    ref_dt = pd.to_datetime(ref_date)

    planned_duration_months = ((sched_comp_dt - start_dt).dt.days / 30.44).clip(lower=1.0)
    elapsed_months = ((ref_dt - start_dt).dt.days / 30.44).clip(lower=0.0)
    elapsed_ratio = (elapsed_months / planned_duration_months).clip(0.0, 2.5)

    cuf_only = pd.DataFrame({
        'project_id': df['project_id'], 'approved_cost_cr': df['approved_cost_cr'].astype(float),
        'cumulative_expenditure_cr': df['cumulative_expenditure_cr'].astype(float),
        'physical_progress_pct': df['physical_progress_pct'].astype(float),
        'planned_duration_months': planned_duration_months, 'elapsed_months': elapsed_months,
        'ministry': df['ministry'].astype(str), 'sector': df['sector'].astype(str),
        'state': df['state'].astype(str), 'implementing_agency': df['implementing_agency'].astype(str)
    })

    financial_velocity = ((df['cumulative_expenditure_cr'] / (df['approved_cost_cr'] + 1e-5)) * 100.0).clip(0.0, 250.0)
    expenditure_progress_ratio = (financial_velocity / (df['physical_progress_pct'] + 1.0)).clip(0.0, 50.0)
    schedule_performance_gap = (elapsed_ratio - (df['physical_progress_pct'] / 100.0)).clip(-1.0, 2.0)

    if not df_snapshots.empty:
        df_snaps_sorted = df_snapshots.sort_values(by=['project_id', 'snapshot_month'])
        snap_agg = df_snaps_sorted.groupby('project_id').agg(
            snap_count=('snapshot_month', 'count'), exp_first=('cumulative_expenditure_cr', 'first'),
            exp_last=('cumulative_expenditure_cr', 'last'), prog_first=('physical_progress_pct', 'first'),
            prog_last=('physical_progress_pct', 'last')
        ).reset_index()
        snap_agg['delta_expenditure_12m'] = (snap_agg['exp_last'] - snap_agg['exp_first']).clip(lower=0.0)
        snap_agg['delta_progress_12m'] = (snap_agg['prog_last'] - snap_agg['prog_first']).clip(lower=0.0)
        snap_agg['burn_rate_monthly_cr'] = snap_agg['delta_expenditure_12m'] / snap_agg['snap_count'].clip(lower=1)
        snap_agg['velocity_monthly_pct'] = snap_agg['delta_progress_12m'] / snap_agg['snap_count'].clip(lower=1)
        df = df.merge(snap_agg[['project_id', 'delta_expenditure_12m', 'delta_progress_12m', 'burn_rate_monthly_cr', 'velocity_monthly_pct']], on='project_id', how='left')
    else:
        df['delta_expenditure_12m'], df['delta_progress_12m'], df['burn_rate_monthly_cr'], df['velocity_monthly_pct'] = 0.0, 10.0, 5.0, 1.0

    df['delta_expenditure_12m'] = df['delta_expenditure_12m'].fillna(0.0)
    df['delta_progress_12m'] = df['delta_progress_12m'].fillna(10.0)
    df['burn_rate_monthly_cr'] = df['burn_rate_monthly_cr'].fillna(5.0)
    df['velocity_monthly_pct'] = df['velocity_monthly_pct'].fillna(1.0)

    if df_milestones is not None and not df_milestones.empty:
        ms_agg = df_milestones.groupby('project_id').agg(
            total_milestones=('milestone_id', 'count'), delayed_milestones=('is_delayed', 'sum')
        ).reset_index()
        ms_agg['milestone_slippage_ratio'] = (ms_agg['delayed_milestones'] / ms_agg['total_milestones'].clip(lower=1)).clip(0.0, 1.0)
        df = df.merge(ms_agg[['project_id', 'delayed_milestones', 'total_milestones', 'milestone_slippage_ratio']], on='project_id', how='left')
    else:
        df['delayed_milestones'], df['total_milestones'], df['milestone_slippage_ratio'] = 0, 6, 0.0

    df['delayed_milestones'] = df['delayed_milestones'].fillna(0).astype(int)
    df['total_milestones'] = df['total_milestones'].fillna(6).astype(int)
    df['milestone_slippage_ratio'] = df['milestone_slippage_ratio'].fillna(0.0)

    sector_complexity = df['sector'].map(SECTOR_COMPLEXITY_INDEX).fillna(0.60)
    state_friction = df['state'].map(STATE_LAND_FRICTION_INDEX).fillna(0.50)
    agency_delay_rate = df.groupby('implementing_agency')['status'].transform(lambda s: (s.isin(['Delayed', 'Stalled'])).mean()).fillna(0.35)
    megaproject_flag = (df['approved_cost_cr'] >= 5000.0).astype(int)

    cuf_plus_extra = pd.DataFrame({
        'project_id': df['project_id'], 'approved_cost_cr': df['approved_cost_cr'].astype(float),
        'cumulative_expenditure_cr': df['cumulative_expenditure_cr'].astype(float),
        'physical_progress_pct': df['physical_progress_pct'].astype(float),
        'planned_duration_months': planned_duration_months, 'elapsed_months': elapsed_months,
        'elapsed_ratio': elapsed_ratio, 'ministry': df['ministry'].astype(str),
        'sector': df['sector'].astype(str), 'state': df['state'].astype(str),
        'implementing_agency': df['implementing_agency'].astype(str),
        'financial_velocity_pct': financial_velocity, 'expenditure_progress_ratio': expenditure_progress_ratio,
        'schedule_performance_gap': schedule_performance_gap,
        'delta_expenditure_12m': df['delta_expenditure_12m'], 'delta_progress_12m': df['delta_progress_12m'],
        'burn_rate_monthly_cr': df['burn_rate_monthly_cr'], 'velocity_monthly_pct': df['velocity_monthly_pct'],
        'delayed_milestones': df['delayed_milestones'], 'total_milestones': df['total_milestones'],
        'milestone_slippage_ratio': df['milestone_slippage_ratio'],
        'sector_complexity_index': sector_complexity, 'state_friction_index': state_friction,
        'agency_delay_rate': agency_delay_rate, 'megaproject_flag': megaproject_flag
    })

    cost_overrun_amount = (df['revised_cost_cr'] - df['approved_cost_cr']).clip(lower=0.0)
    cost_overrun_pct = ((cost_overrun_amount / (df['approved_cost_cr'] + 1e-5)) * 100.0).clip(lower=0.0)
    cost_overrun_class = (df['revised_cost_cr'] > df['approved_cost_cr'] * 1.01).astype(int)
    time_delay_months = (((rev_comp_dt - sched_comp_dt).dt.days) / 30.44).clip(lower=0.0)
    time_overrun_class = (time_delay_months > 0.5).astype(int)

    targets = pd.DataFrame({
        'project_id': df['project_id'], 'cost_overrun_class': cost_overrun_class,
        'cost_overrun_pct': cost_overrun_pct, 'cost_overrun_amount_cr': cost_overrun_amount,
        'time_overrun_class': time_overrun_class, 'time_overrun_months': time_delay_months
    })

    return cuf_only, cuf_plus_extra, targets
