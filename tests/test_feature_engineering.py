"""
Unit Tests: Feature Engineering Pipeline & Division-by-Zero Safeguards
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.models.train_and_evaluate import load_data_from_db, build_feature_matrices

DB_PATH = os.path.join(ROOT_DIR, "paimana.db")


def test_feature_matrix_shapes_and_columns():
    """Verify feature matrices have expected shape and non-empty columns."""
    df_projects, df_snapshots, df_milestones = load_data_from_db(DB_PATH)
    cuf_base, cuf_plus, targets = build_feature_matrices(df_projects, df_snapshots, df_milestones)

    assert len(cuf_base) == len(df_projects), f"CUF Base must match {len(df_projects)} projects"
    assert len(cuf_plus) == len(df_projects), f"CUF Plus must match {len(df_projects)} projects"
    assert len(cuf_plus.columns) > len(cuf_base.columns), "CUF Plus must include engineered extra columns"


def test_expenditure_to_progress_ratio_safeguard():
    """Verify expenditure-to-progress ratio handles zero progress gracefully without NaN or Inf."""
    df_projects, df_snapshots, df_milestones = load_data_from_db(DB_PATH)
    cuf_base, cuf_plus, targets = build_feature_matrices(df_projects, df_snapshots, df_milestones)

    ratios = cuf_plus['expenditure_to_progress_ratio']
    assert not ratios.isnull().any(), "Ratio must not contain NaN"
    assert not np.isinf(ratios).any(), "Ratio must not contain Infinity"
    assert (ratios >= 0.0).all() and (ratios <= 10.0).all(), "Ratio must be bounded in [0, 10]"


def test_target_classification_and_regression_alignment():
    """Verify binary classification target matches positive regression overrun target."""
    df_projects, df_snapshots, df_milestones = load_data_from_db(DB_PATH)
    cuf_base, cuf_plus, targets = build_feature_matrices(df_projects, df_snapshots, df_milestones)

    cost_cls = targets['cost_overrun_class']
    cost_reg = targets['cost_overrun_reg']

    # When cost_reg > 1.0%, cost_cls must be 1
    assert (cost_cls[cost_reg > 1.0] == 1).all()
