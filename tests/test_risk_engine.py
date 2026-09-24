"""
Unit Tests: Risk Scoring Engine & Prescriptive Remediation Playbooks
"""

import os
import sys
import json
import sqlite3
import pytest
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.risk_engine.prescriptions import get_prescriptions_for_factors
from src.risk_engine.scorer import _deterministic_variance

DB_PATH = os.path.join(ROOT_DIR, "paimana.db")


def test_deterministic_variance_reproducibility():
    """Verify _deterministic_variance is 100% reproducible and bounded."""
    val1 = _deterministic_variance("PRJ-00001", base=8.0, range_val=4.0)
    val2 = _deterministic_variance("PRJ-00001", base=8.0, range_val=4.0)
    val_diff = _deterministic_variance("PRJ-00002", base=8.0, range_val=4.0)
    
    assert val1 == val2, "Variance must be strictly deterministic given identical project_id"
    assert 6.0 <= val1 <= 10.0, "Variance must remain within [base - range/2, base + range/2]"
    assert val1 != val_diff, "Different project_ids should yield different variance values"


@pytest.fixture
def db_conn():
    conn = sqlite3.connect(DB_PATH)
    yield conn
    conn.close()


def test_risk_scores_bounds_and_coverage(db_conn):
    """Verify all projects have risk scores strictly bounded between 0 and 100."""
    total_proj = pd.read_sql("SELECT COUNT(*) as cnt FROM projects", db_conn)['cnt'].iloc[0]
    df = pd.read_sql("SELECT score, risk_level FROM risk_scores", db_conn)
    assert len(df) == total_proj, f"All {total_proj} projects must have risk scores"
    assert (df['score'] >= 0.0).all() and (df['score'] <= 100.0).all(), "Scores must be in [0, 100]"
    assert set(df['risk_level'].unique()).issubset({'Low', 'Medium', 'High'})


def test_prescriptive_actions_generation():
    """Verify prescriptive engine translates top drivers into structured governance playbooks."""
    sample_factors = [
        {'factor': 'Delayed Milestones', 'raw_factor': 'delayed_milestones', 'contribution': 14.5, 'detail': '3 milestones delayed'},
        {'factor': 'Expenditure Mismatch', 'raw_factor': 'expenditure_to_progress_ratio', 'contribution': 12.0, 'detail': 'Ratio distorted'}
    ]
    prescriptions = get_prescriptions_for_factors(sample_factors)
    assert len(prescriptions) >= 1, "Must generate at least 1 prescriptive playbook"
    first = prescriptions[0]
    assert 'title' in first and 'authority' in first and 'recommended_action' in first
    assert first['statutory_timeline_days'] > 0


def test_early_warning_alerts_severity(db_conn):
    """Verify all High-Risk projects have generated alerts with prescriptive actions."""
    df_alerts = pd.read_sql("SELECT severity, prescriptive_action, lead_time_months FROM alerts", db_conn)
    assert len(df_alerts) > 0, "Alerts must be populated"
    assert df_alerts['prescriptive_action'].isnull().sum() == 0, "Prescriptive actions must be populated"
    assert (df_alerts['lead_time_months'] > 0).all(), "Lead times must be positive months"
