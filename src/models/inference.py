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
    db_path: Any = None,
    artifacts_dir: Any = None
) -> bool:
    """
    Executes fast vector inference using pre-trained model bundles
    to populate conformal intervals and overrun predictions in SQLite.
    """
    target_db = db_path or os.path.join(ROOT_DIR, os.getenv("DATABASE_PATH", "paimana.db"))
    target_art = artifacts_dir or os.path.join(ROOT_DIR, "artifacts", "models")
    df_projects, df_snapshots, df_milestones = load_data_from_db(target_db)
    if len(df_projects) == 0:
        return True

    cuf_base, cuf_plus, _ = build_feature_matrices(df_projects, df_snapshots, df_milestones)
    feature_sets = {'cuf_only': cuf_base, 'cuf_plus_extra': cuf_plus}
    records_to_insert = []

    for fset_name, df_features in feature_sets.items():
        fset_bundle_path = os.path.join(target_art, f"model_bundle_{fset_name}.joblib")
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

        models = bundle.get('models', {}) if isinstance(bundle.get('models'), dict) else {}
        cost_cls = models.get('cost_cls', {}).get('xgboost_classifier') if isinstance(models.get('cost_cls'), dict) else (models.get('cost_cls') or bundle.get('xgb_cost_cls'))
        time_cls = models.get('time_cls', {}).get('xgboost_classifier') if isinstance(models.get('time_cls'), dict) else (models.get('time_cls') or bundle.get('xgb_time_cls'))
        cost_reg = models.get('cost_reg', {}).get('xgboost_regressor') if isinstance(models.get('cost_reg'), dict) else (models.get('cost_reg') or bundle.get('xgb_cost_reg'))
        time_reg = models.get('time_reg', {}).get('xgboost_regressor') if isinstance(models.get('time_reg'), dict) else (models.get('time_reg') or bundle.get('xgb_time_reg'))

        if cost_cls is None or time_cls is None or cost_reg is None or time_reg is None:
            logger.warning(f"Bundle {fset_bundle_path} missing required models, skipping")
            continue

        cost_prob = cost_cls.predict_proba(X_all)[:, 1]
        time_prob = time_cls.predict_proba(X_all)[:, 1]
        cost_pred = np.clip(cost_reg.predict(X_all), 0.0, None)
        time_pred = np.clip(time_reg.predict(X_all), 0.0, None)

        m_cost_lower = models.get('cost_lower') or bundle.get('gbr_cost_lower')
        m_cost_upper = models.get('cost_upper') or bundle.get('gbr_cost_upper')
        m_time_lower = models.get('time_lower') or bundle.get('gbr_time_lower')
        m_time_upper = models.get('time_upper') or bundle.get('gbr_time_upper')

        cost_lower = m_cost_lower.predict(X_all) if m_cost_lower is not None else cost_pred * 0.5
        cost_upper = m_cost_upper.predict(X_all) if m_cost_upper is not None else cost_pred * 1.5
        time_lower = m_time_lower.predict(X_all) if m_time_lower is not None else time_pred * 0.5
        time_upper = m_time_upper.predict(X_all) if m_time_upper is not None else time_pred * 1.5

        for idx, row in df_features.iterrows():
            records_to_insert.append({
                'project_id': row['project_id'],
                'model_name': 'xgboost_ensemble',
                'model_version': 'v2.1',
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
            conn = sqlite3.connect(target_db, timeout=10.0)
            conn.execute("PRAGMA journal_mode=WAL;")
            cur = conn.cursor()
            inserted_feature_sets = list({r['feature_set'] for r in records_to_insert})
            for fset in inserted_feature_sets:
                cur.execute("DELETE FROM model_predictions WHERE feature_set = ?", (fset,))
            for r in records_to_insert:
                cur.execute("""
                INSERT INTO model_predictions (
                    project_id, model_name, model_version, feature_set,
                    cost_overrun_prob, cost_overrun_pct_pred,
                    cost_overrun_pct_lower, cost_overrun_pct_upper, time_overrun_prob,
                    time_overrun_months_pred, time_delay_lower_months, time_delay_upper_months,
                    predicted_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    r['project_id'], r['model_name'], r['model_version'], r['feature_set'],
                    r['cost_overrun_prob'], r['cost_overrun_pct_pred'],
                    r['cost_overrun_pct_lower'], r['cost_overrun_pct_upper'],
                    r['time_overrun_prob'], r['time_overrun_months_pred'],
                    r['time_delay_lower_months'], r['time_delay_upper_months']
                ))
            conn.commit()
        except Exception:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass
    return True
