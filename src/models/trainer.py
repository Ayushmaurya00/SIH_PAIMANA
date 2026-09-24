"""
ML Model Training Routines for PAIMANA AI
"""

import numpy as np
from typing import Dict, Any
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBClassifier, XGBRegressor

RANDOM_STATE = 42


def train_classification_models(X_train: np.ndarray, y_train: np.ndarray) -> Dict[str, Any]:
    """Trains baseline Logistic Regression and XGBoost classifiers."""
    models = {
        'logistic_regression': LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, class_weight='balanced'),
        'xgboost_classifier': XGBClassifier(n_estimators=120, max_depth=4, learning_rate=0.08, subsample=0.85, colsample_bytree=0.85, random_state=RANDOM_STATE, eval_metric='logloss')
    }
    for name, model in models.items():
        model.fit(X_train, y_train)
    return models


def train_regression_models(X_train: np.ndarray, y_train: np.ndarray) -> Dict[str, Any]:
    """Trains baseline Ridge and XGBoost regressors."""
    models = {
        'ridge_regressor': Ridge(alpha=1.0, random_state=RANDOM_STATE),
        'xgboost_regressor': XGBRegressor(n_estimators=120, max_depth=4, learning_rate=0.08, subsample=0.85, colsample_bytree=0.85, random_state=RANDOM_STATE)
    }
    for name, model in models.items():
        model.fit(X_train, y_train)
    return models


def train_quantile_regressors(X_train: np.ndarray, y_train: np.ndarray) -> Tuple_Quantiles:
    """Trains lower (5th percentile) and upper (95th percentile) quantile regressors."""
    lower_model = GradientBoostingRegressor(loss='quantile', alpha=0.05, n_estimators=100, max_depth=3, random_state=RANDOM_STATE)
    upper_model = GradientBoostingRegressor(loss='quantile', alpha=0.95, n_estimators=100, max_depth=3, random_state=RANDOM_STATE)
    lower_model.fit(X_train, y_train)
    upper_model.fit(X_train, y_train)
    return lower_model, upper_model


from typing import Tuple as Tuple_Quantiles
