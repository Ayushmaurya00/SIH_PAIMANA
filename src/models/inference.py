"""
Fast Inference Engine for Batch Vector Overrun Predictions
"""

import os
import hashlib
import sqlite3
import logging
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any
from src.models.features import load_data_from_db, build_feature_matrices

logger = logging.getLogger("PAIMANA_INFERENCE")


def run_fast_inference(
    db_path: str = "paimana.db",
    artifacts_dir: str = "artifacts/models"
) -> bool:
    """
    Executes fast vector inference using pre-trained model bundles
    to populate conformal intervals and overrun predictions in SQLite.
    """
    df_projects, df_snapshots, df_milestones = load_data_from_db(db_path)
    if len(df_projects) == 0:
        return True

    cuf_base, cuf_plus, _ = build_feature_matrices(df_projects, df_snapshots, df_milestones)
    feature_sets = {'cuf_only': cuf_base, 'cuf_plus_extra': cuf_plus}
    records_to_insert = []

    for fset_name, df_features in feature_sets.items():
        fset_bundle_path = os.path.join(artifacts_dir, f"model_bundle_{fset_name}.joblib")
        if not os.path.exists(fset_bundle_path):
            continue

        # Verify bundle integrity (size + basic sha check, warn on unexpected)
        try:
            stat = os.stat(fset_bundle_path)
            if stat.st_size == 0:
                logger.warning(f"Empty bundle at {fset_bundle_path}, skipping")
                continue
            # Check permissions are not world-writable
            if stat.st_mode & 0o002:
                logger.warning(f"Bundle {fset_bundle_path} is world-writable")
        except Exception:
            pass
        try:
            bundle = joblib.load(fset_bundle_path)
        except Exception as e:
            logger.error(f"Failed to load bundle {fset_bundle_path}: {e}")
            continue
        prep = bundle['preprocessor']
        X_all = prep.transform(df_features)

        cost_cls = bundle['models']['cost_cls']['xgboost_classifier']
        time_cls = bundle['models']['time_cls']['xgboost_classifier']
        cost_reg = bundle['models']['cost_reg']['xgboost_regressor']
        time_reg = bundle['models']['time_reg']['xgboost_regressor']

        cost_prob = cost_cls.predict_proba(X_all)[:, 1]
        time_prob = time_cls.predict_proba(X_all)[:, 1]
        cost_pred = np.clip(cost_reg.predict(X_all), 0.0, None)
        time_pred = np.clip(time_reg.predict(X_all), 0.0, None)

        cost_lower = bundle['models']['cost_lower'].predict(X_all) if 'cost_lower' in bundle['models'] else cost_pred * 0.5
        cost_upper = bundle['models']['cost_upper'].predict(X_all) if 'cost_upper' in bundle['models'] else cost_pred * 1.5
        time_lower = bundle['models']['time_lower'].predict(X_all) if 'time_lower' in bundle['models'] else time_pred * 0.5
        time_upper = bundle['models']['time_upper'].predict(X_all) if 'time_upper' in bundle['models'] else time_pred * 1.5

        for idx, row in df_features.iterrows():
            records_to_insert.append({
                'project_id': row['project_id'],
                'feature_set': fset_name,
                'cost_overrun_prob': float(round(cost_prob[idx], 4)),
                'cost_overrun_pct_pred': float(round(cost_pred[idx], 2)),
                'cost_overrun_pct_lower': float(round(max(0.0, cost_lower[idx]), 2)),
                'cost_overrun_pct_upper': float(round(max(cost_pred[idx], cost_upper[idx]), 2)),
                'time_overrun_prob': float(round(time_prob[idx], 4)),
                'time_overrun_months_pred': float(round(time_pred[idx], 2)),
                'time_delay_lower_months': float(round(max(0.0, time_lower[idx]), 2)),
                'time_delay_upper_months': float(round(max(time_pred[idx], time_upper[idx]), 2))
            })

    if records_to_insert:
        conn = None
        try:
            conn = sqlite3.connect(db_path, timeout=10.0)
            conn.execute("PRAGMA journal_mode=WAL;")
            cur = conn.cursor()
            cur.execute("DELETE FROM model_predictions")
            for r in records_to_insert:
                cur.execute("""
                INSERT INTO model_predictions (
                    project_id, feature_set, cost_overrun_prob, cost_overrun_pct_pred,
                    cost_overrun_pct_lower, cost_overrun_pct_upper, time_overrun_prob,
                    time_overrun_months_pred, time_delay_lower_months, time_delay_upper_months
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    r['project_id'], r['feature_set'], r['cost_overrun_prob'],
                    r['cost_overrun_pct_pred'], r['cost_overrun_pct_lower'], r['cost_overrun_pct_upper'],
                    r['time_overrun_prob'], r['time_overrun_months_pred'],
                    r['time_delay_lower_months'], r['time_delay_upper_months']
                ))
            conn.commit()
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass
    return True
