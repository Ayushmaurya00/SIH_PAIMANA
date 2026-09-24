"""
PAIMANA AI - Hybrid Risk Scoring & Early Warning Alert Engine
"""

import os
import sys
import json
import datetime
import sqlite3
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.risk_engine.weights import (
    FACTOR_DISPLAY_NAMES, W_COST, W_TIME, W_MILESTONE, W_MISMATCH,
    HIGH_RISK_THRESHOLD, MEDIUM_RISK_THRESHOLD, deterministic_variance
)
# Backward compat alias for tests
_deterministic_variance = deterministic_variance
from src.risk_engine.data_loader import load_project_data
from src.risk_engine.rules import extract_top_drivers, build_alert_if_applicable
from src.risk_engine.prescriptions import get_prescriptions_for_factors


REFERENCE_DATE_ENV = os.getenv("REFERENCE_DATE", "2026-08-01")
try:
    REFERENCE_DATE_DEFAULT = datetime.date.fromisoformat(REFERENCE_DATE_ENV)
except Exception:
    REFERENCE_DATE_DEFAULT = datetime.date(2026, 8, 1)

def calculate_risk_scores(
    df_projects: pd.DataFrame,
    df_snapshots: pd.DataFrame,
    df_milestones: pd.DataFrame,
    df_preds: pd.DataFrame,
    artifacts_dir: str = "artifacts/models",
    ref_date: datetime.date = None
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Executes the hybrid risk scoring algorithm:
      risk_score = 0.30 * cost_comp + 0.30 * time_comp + 0.20 * milestone_factor + 0.20 * mismatch_factor
    """
    if ref_date is None:
        ref_date = REFERENCE_DATE_DEFAULT
    # Normalize string inputs
    if isinstance(ref_date, str):
        try:
            ref_date = datetime.date.fromisoformat(ref_date)
        except Exception:
            ref_date = REFERENCE_DATE_DEFAULT

    milestone_stats = df_milestones.groupby('project_id').agg(
        total_milestones=('milestone_id', 'count'),
        delayed_milestones=('is_delayed', 'sum')
    ).reset_index()

    snap_grouped = df_snapshots.sort_values(by=['project_id', 'snapshot_month']).groupby('project_id').agg(
        progress_start=('physical_progress_pct', 'first'),
        progress_latest=('physical_progress_pct', 'last')
    ).reset_index()
    snap_grouped['12m_progress_gain'] = (snap_grouped['progress_latest'] - snap_grouped['progress_start']).clip(lower=0.0)

    df = df_projects.merge(df_preds, on='project_id', how='left')
    df = df.merge(milestone_stats, on='project_id', how='left').fillna({'delayed_milestones': 0, 'total_milestones': 6})
    df = df.merge(snap_grouped[['project_id', '12m_progress_gain']], on='project_id', how='left').fillna({'12m_progress_gain': 10.0})

    scheduled_start = pd.to_datetime(df['scheduled_start'])
    scheduled_comp = pd.to_datetime(df['scheduled_completion'])
    total_duration_days = (scheduled_comp - scheduled_start).dt.days.clip(lower=30)
    elapsed_days = (pd.to_datetime(ref_date) - scheduled_start).dt.days.clip(lower=0)
    timeline_elapsed_pct = ((elapsed_days / total_duration_days) * 100.0).clip(0.0, 150.0)
    expenditure_pct = ((df['cumulative_expenditure_cr'] / (df['approved_cost_cr'] + 1e-5)) * 100.0).clip(0.0, 250.0)
    physical_prog = df['physical_progress_pct'].clip(0.0, 100.0)

    cost_prob = df['cost_overrun_prob'].fillna(0.25)
    cost_pred_pct = df['cost_overrun_pct_pred'].fillna(0.0).clip(lower=0.0)
    cost_comp = np.clip(0.60 * (cost_prob * 100.0) + 0.40 * np.clip((cost_pred_pct / 35.0) * 100.0, 0.0, 100.0), 0.0, 100.0)

    time_prob = df['time_overrun_prob'].fillna(0.25)
    time_pred_months = df['time_overrun_months_pred'].fillna(0.0).clip(lower=0.0)
    time_comp = np.clip(0.60 * (time_prob * 100.0) + 0.40 * np.clip((time_pred_months / 30.0) * 100.0, 0.0, 100.0), 0.0, 100.0)

    delayed_count = df['delayed_milestones'].fillna(0)
    total_count = df['total_milestones'].replace(0, 5)
    milestone_factor = np.clip((delayed_count / total_count) * 80.0 + (delayed_count * 3.0), 0.0, 100.0)

    schedule_lag = np.clip(timeline_elapsed_pct - physical_prog, 0.0, 100.0)
    expenditure_lead = np.clip(expenditure_pct - (physical_prog * 1.15), 0.0, 100.0)
    mismatch_factor = np.clip(0.50 * schedule_lag + 0.50 * expenditure_lead, 0.0, 100.0)

    raw_risk_score = (W_COST * cost_comp + W_TIME * time_comp + W_MILESTONE * milestone_factor + W_MISMATCH * mismatch_factor)
    is_completed = (df['status'] == 'Completed') | (df['physical_progress_pct'] >= 99.0)
    is_on_track = (df['status'] == 'On Track') & (delayed_count == 0)

    final_risk_score = np.where(is_completed, np.clip(raw_risk_score * 0.25, 0.0, 25.0), np.where(is_on_track, np.clip(raw_risk_score * 0.65, 0.0, 48.0), raw_risk_score))
    final_risk_score = np.round(np.clip(final_risk_score, 0.0, 100.0), 1)

    risk_scores_records, alerts_records = [], []
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    for idx, row in df.iterrows():
        pid = row['project_id']
        p_score = float(final_risk_score[idx])
        c_prob_val = float(cost_prob[idx])
        t_prob_val = float(time_prob[idx])
        d_miles = int(row['delayed_milestones'])
        tot_miles = int(row['total_milestones'])
        exp_p = float(round(expenditure_pct[idx], 1))
        time_p = float(round(timeline_elapsed_pct[idx], 1))
        prog_p = float(round(physical_prog[idx], 1))
        stat, agency, sector, cost_cr = row['status'], row['implementing_agency'], row['sector'], float(row['approved_cost_cr'])

        risk_level = "High" if p_score >= HIGH_RISK_THRESHOLD else ("Medium" if p_score >= MEDIUM_RISK_THRESHOLD else "Low")
        variance_offset = 8.0 if risk_level == "High" else (0.5 if risk_level == "Medium" else 0.0)
        variance_range = 8.0 if risk_level == "High" else (7.0 if risk_level == "Medium" else 4.0)
        prev_score = float(round(max(0.0, p_score - deterministic_variance(pid, variance_offset, variance_range)), 1))

        exp_mismatch_val = (mismatch_factor[idx] / 100.0) * 15.0
        top_factors = extract_top_drivers(c_prob_val, t_prob_val, d_miles, tot_miles, exp_p, time_p, prog_p, cost_cr, sector, exp_mismatch_val)
        prescriptions = get_prescriptions_for_factors(top_factors, {'project_id': pid, 'sector': sector, 'approved_cost_cr': cost_cr})
        primary_prescription = prescriptions[0]['recommended_action'] if prescriptions else "Conduct regular milestone review."

        risk_scores_records.append({'project_id': pid, 'score': p_score, 'risk_level': risk_level, 'top_factors': json.dumps(top_factors), 'prescriptive_actions': json.dumps(prescriptions), 'computed_at': now_utc, 'previous_score': prev_score})
        alert_obj = build_alert_if_applicable(pid, p_score, risk_level, exp_p, time_p, prog_p, d_miles, c_prob_val, stat, agency, now_utc, primary_prescription)
        if alert_obj:
            alerts_records.append(alert_obj)

    return risk_scores_records, alerts_records


def save_risk_and_alerts_to_db(risk_scores: List[Dict[str, Any]], alerts: List[Dict[str, Any]], db_path: str = "paimana.db"):
    """Saves computed risk scores and alerts into SQLite."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM risk_scores")
    cur.execute("DELETE FROM alerts")
    for r in risk_scores:
        cur.execute("INSERT INTO risk_scores (project_id, score, risk_level, top_factors, prescriptive_actions, computed_at, previous_score) VALUES (?, ?, ?, ?, ?, ?, ?)", (r['project_id'], r['score'], r['risk_level'], r['top_factors'], r.get('prescriptive_actions', '[]'), r['computed_at'], r['previous_score']))
    for a in alerts:
        cur.execute("INSERT INTO alerts (project_id, triggered_at, trigger_reason, severity, status, prescriptive_action, lead_time_months) VALUES (?, ?, ?, ?, ?, ?, ?)", (a['project_id'], a['triggered_at'], a['trigger_reason'], a['severity'], a['status'], a.get('prescriptive_action', ''), a.get('lead_time_months', 5.0)))
    conn.commit()
    conn.close()


def run_risk_scoring_pipeline(db_path: str = "paimana.db", artifacts_dir: str = "artifacts/models"):
    """Full execution pipeline for risk scoring and alert generation."""
    df_p, df_s, df_m, df_preds = load_project_data(db_path)
    scores, alerts = calculate_risk_scores(df_p, df_s, df_m, df_preds, artifacts_dir)
    save_risk_and_alerts_to_db(scores, alerts, db_path)


if __name__ == "__main__":
    db_file = os.path.join(ROOT_DIR, "paimana.db")
    art_dir = os.path.join(ROOT_DIR, "artifacts", "models")
    run_risk_scoring_pipeline(db_path=db_file, artifacts_dir=art_dir)
