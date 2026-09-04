"""
PAIMANA AI - Production ML Training & Evaluation Orchestrator
"""

import os
import sys
import datetime
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.models.features import load_data_from_db, build_feature_matrices, get_preprocessor
from src.models.trainer import (
    train_classification_models, train_regression_models, train_quantile_regressors
)
from src.models.evaluator import (
    evaluate_classifier, evaluate_regressor, calculate_early_warning_lead_time, save_metrics_to_db
)
from src.models.inference import run_fast_inference


def train_and_evaluate_all(db_path: str = "paimana.db", artifacts_dir: str = "artifacts/models"):
    """Full ML training, evaluation, and conformal interval generation pipeline."""
    os.makedirs(artifacts_dir, exist_ok=True)
    df_projects, df_snapshots, df_milestones = load_data_from_db(db_path)
    # Unified reference date from env or default
    import datetime
    ref_date_str = os.getenv("REFERENCE_DATE", "2026-08-01")
    try:
        ref_date = datetime.date.fromisoformat(ref_date_str)
    except Exception:
        ref_date = datetime.date(2026, 8, 1)
    # Temporal split ids first to avoid leakage
    df_sorted = df_projects.sort_values(by='approval_date')
    split_idx = int(len(df_sorted) * 0.80)
    train_pids = set(df_sorted.iloc[:split_idx]['project_id'])
    cuf_base, cuf_plus, targets = build_feature_matrices(df_projects, df_snapshots, df_milestones, ref_date=ref_date, train_ids=train_pids)

    feature_sets = {'cuf_only': cuf_base, 'cuf_plus_extra': cuf_plus}
    metrics_records = []

    # Temporal split already computed above for leakage-safe feature building

    for fset_name, df_features in feature_sets.items():
        is_train = df_features['project_id'].isin(train_pids)
        preprocessor, num_cols, cat_cols = get_preprocessor(df_features)

        X_train_raw = df_features[is_train]
        X_test_raw = df_features[~is_train]
        X_train = preprocessor.fit_transform(X_train_raw)
        X_test = preprocessor.transform(X_test_raw)

        # 1. Cost Overrun Classification
        cost_cls_models = train_classification_models(X_train, targets['cost_overrun_class'][is_train])
        for m_name, model in cost_cls_models.items():
            ev = evaluate_classifier(model, X_test, targets['cost_overrun_class'][~is_train])
            lead_time = calculate_early_warning_lead_time(df_snapshots, df_projects, model, preprocessor, df_features) if m_name == 'xgboost_classifier' else None
            metrics_records.append({'feature_set': fset_name, 'model_name': m_name, 'target': 'cost_overrun_classification', **ev, 'lead_time_months': lead_time})

        # 2. Time Overrun Classification
        time_cls_models = train_classification_models(X_train, targets['time_overrun_class'][is_train])
        for m_name, model in time_cls_models.items():
            ev = evaluate_classifier(model, X_test, targets['time_overrun_class'][~is_train])
            metrics_records.append({'feature_set': fset_name, 'model_name': m_name, 'target': 'time_overrun_classification', **ev})

        # 3. Cost Overrun Regression
        cost_reg_models = train_regression_models(X_train, targets['cost_overrun_reg'][is_train])
        for m_name, model in cost_reg_models.items():
            ev = evaluate_regressor(model, X_test, targets['cost_overrun_reg'][~is_train])
            metrics_records.append({'feature_set': fset_name, 'model_name': m_name, 'target': 'cost_overrun_regression_pct', **ev})

        # 4. Time Overrun Regression
        time_reg_models = train_regression_models(X_train, targets['time_overrun_reg'][is_train])
        for m_name, model in time_reg_models.items():
            ev = evaluate_regressor(model, X_test, targets['time_overrun_reg'][~is_train])
            metrics_records.append({'feature_set': fset_name, 'model_name': m_name, 'target': 'time_overrun_regression_months', **ev})

        # 5. Quantile Bounds
        cost_lower, cost_upper = train_quantile_regressors(X_train, targets['cost_overrun_reg'][is_train])
        time_lower, time_upper = train_quantile_regressors(X_train, targets['time_overrun_reg'][is_train])

        # Serialize Bundle
        bundle = {
            'feature_set': fset_name,
            'preprocessor': preprocessor,
            'num_cols': num_cols,
            'cat_cols': cat_cols,
            'models': {
                'cost_cls': cost_cls_models,
                'time_cls': time_cls_models,
                'cost_reg': cost_reg_models,
                'time_reg': time_reg_models,
                'cost_lower': cost_lower,
                'cost_upper': cost_upper,
                'time_lower': time_lower,
                'time_upper': time_upper
            }
        }
        joblib.dump(bundle, os.path.join(artifacts_dir, f"model_bundle_{fset_name}.joblib"))

    save_metrics_to_db(metrics_records, db_path)
    run_fast_inference(db_path, artifacts_dir)


if __name__ == "__main__":
    db_file = os.path.join(ROOT_DIR, "paimana.db")
    art_dir = os.path.join(ROOT_DIR, "artifacts", "models")
    train_and_evaluate_all(db_path=db_file, artifacts_dir=art_dir)
