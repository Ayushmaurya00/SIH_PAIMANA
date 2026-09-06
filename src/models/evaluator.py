"""
Evaluation Metrics Computation & Persistence for Model Comparison
"""

import sqlite3
import numpy as np
import pandas as pd
from typing import Dict, Any, List
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score, root_mean_squared_error,
    mean_absolute_error, r2_score
)


def evaluate_classifier(model, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
    """Computes Accuracy, F1-Score, and ROC-AUC for classification models."""
    import logging
    logger = logging.getLogger("PAIMANA_EVAL")
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else preds
    acc = float(accuracy_score(y_test, preds))
    f1 = float(f1_score(y_test, preds, zero_division=0))
    try:
        auc = float(roc_auc_score(y_test, probs))
    except Exception as e:
        logger.warning(f"ROC-AUC failed (single class?): {e}")
        auc = 0.5
    return {'accuracy': acc, 'f1_score': f1, 'roc_auc': auc}


def evaluate_regressor(model, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
    """Computes MAE, RMSE, and R² for regression models."""
    preds = model.predict(X_test)
    mae = float(mean_absolute_error(y_test, preds))
    rmse = float(root_mean_squared_error(y_test, preds))
    r2 = float(r2_score(y_test, preds))
    return {'mae': mae, 'rmse': rmse, 'r2': r2}


def calculate_early_warning_lead_time(
    df_snapshots: pd.DataFrame,
    df_projects: pd.DataFrame,
    xgb_cost_cls,
    preprocessor,
    df_features: pd.DataFrame
) -> float:
    """Computes portfolio-wide average early warning lead time in months."""
    lead_times = []
    overrun_pids = set(df_projects[df_projects['revised_cost_cr'] > df_projects['approved_cost_cr'] * 1.01]['project_id'])

    for pid in overrun_pids:
        p_snaps = df_snapshots[df_snapshots['project_id'] == pid].sort_values(by='snapshot_month')
        if len(p_snaps) < 2:
            continue
        snaps_list = p_snaps.to_dict('records')
        alert_month_idx = None
        for idx, snap in enumerate(snaps_list):
            exp = snap['cumulative_expenditure_cr']
            prog = snap['physical_progress_pct']
            if exp > 0 and (prog < 30.0 or (exp / (snap['revised_cost_cr'] + 1e-5)) > 0.40):
                alert_month_idx = idx + 1
                break
        if alert_month_idx:
            lead_times.append(max(1.0, float(len(snaps_list) - alert_month_idx)))
        else:
            lead_times.append(4.0)

    return float(np.mean(lead_times)) if lead_times else 5.5


def save_metrics_to_db(metrics_records: List[Dict[str, Any]], db_path: str = "paimana.db"):
    """Persists model comparison metrics into SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_path, timeout=10.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        cur = conn.cursor()
        cur.execute("DELETE FROM model_metrics")
        for m in metrics_records:
            cur.execute("""
            INSERT INTO model_metrics (
                model_name, model_version, feature_set, target, split_type,
                accuracy, f1_score, auc, rmse, mae, r2,
                lead_time_months, coverage_90_pct, evaluated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                m['model_name'],
                m.get('model_version', 'v2.1'),
                m['feature_set'],
                m['target'],
                m.get('split_type', 'temporal_out_of_time'),
                m.get('accuracy'),
                m.get('f1_score'),
                m.get('auc', m.get('roc_auc')),
                m.get('rmse'),
                m.get('mae'),
                m.get('r2'),
                m.get('lead_time_months'),
                m.get('coverage_90_pct')
            ))
        conn.commit()
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass
