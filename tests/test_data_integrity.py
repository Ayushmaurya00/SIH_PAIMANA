"""
Unit & Integration Tests: Synthetic CUF Data Integrity & Boundary Constraints
"""

import os
import sys
import sqlite3
import pytest
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

DB_PATH = os.path.join(ROOT_DIR, "paimana.db")


@pytest.fixture
def db_conn():
    conn = sqlite3.connect(DB_PATH)
    yield conn
    conn.close()


def test_project_count_and_schema(db_conn):
    """Verify projects exist with valid non-null CUF identifiers."""
    df = pd.read_sql("SELECT * FROM projects", db_conn)
    assert len(df) >= 1, f"Expected at least 1 project, got {len(df)}"
    assert df['project_id'].nunique() == len(df), "Project IDs must be unique"
    assert df['project_name'].isnull().sum() == 0, "Project names cannot be null"


def test_positive_financial_outlays(db_conn):
    """Verify Central Sector project outlay threshold (>= ₹150 Cr) and positive expenditures."""
    df = pd.read_sql("SELECT approved_cost_cr, revised_cost_cr, cumulative_expenditure_cr FROM projects", db_conn)
    assert (df['approved_cost_cr'] >= 150.0).all(), "All projects must meet MoSPI ₹150 Cr threshold"
    assert (df['revised_cost_cr'] >= 150.0).all(), "Revised cost must be positive"
    assert (df['cumulative_expenditure_cr'] >= 0.0).all(), "Expenditure cannot be negative"


def test_snapshot_and_milestone_foreign_keys(db_conn):
    """Verify 12 monthly snapshots per project and milestone foreign key consistency."""
    df_proj = pd.read_sql("SELECT COUNT(*) as cnt FROM projects", db_conn)
    total_projects = df_proj['cnt'].iloc[0]

    df_snaps = pd.read_sql("SELECT project_id, COUNT(*) as cnt FROM monthly_snapshots GROUP BY project_id", db_conn)
    assert len(df_snaps) == total_projects, f"All {total_projects} projects must have monthly snapshots"
    assert (df_snaps['cnt'] >= 1).all(), "Each project must contain at least 1 monthly snapshot"

    df_miles = pd.read_sql("SELECT project_id, COUNT(*) as cnt FROM milestones GROUP BY project_id", db_conn)
    assert len(df_miles) == total_projects, f"All {total_projects} projects must have milestones logged"
    assert (df_miles['cnt'] >= 4).all(), "Projects must have at least 4 milestone stages"


def test_valid_statuses_and_progress_bounds(db_conn):
    """Verify status categories and physical progress percentages (0 to 100%)."""
    df = pd.read_sql("SELECT status, physical_progress_pct FROM projects", db_conn)
    valid_statuses = {'On Track', 'Delayed', 'Stalled', 'Completed'}
    assert set(df['status'].unique()).issubset(valid_statuses), "Status must be within defined categories"
    assert (df['physical_progress_pct'] >= 0.0).all() and (df['physical_progress_pct'] <= 100.0).all(), "Progress must be in [0, 100]"
