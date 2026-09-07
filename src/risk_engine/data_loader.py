"""
Data Loading Queries for Risk Calculation Engine
"""

import sqlite3
import pandas as pd
from typing import Tuple


def load_project_data(db_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Loads projects, snapshots, milestones, and model predictions from SQLite."""
    conn = sqlite3.connect(db_path)
    df_projects = pd.read_sql("SELECT * FROM projects", conn)
    df_snapshots = pd.read_sql("SELECT * FROM monthly_snapshots", conn)
    df_milestones = pd.read_sql("SELECT * FROM milestones", conn)

    query_preds = """
        SELECT project_id, cost_overrun_prob, cost_overrun_pct_pred,
               time_overrun_prob, time_overrun_months_pred
        FROM model_predictions
        WHERE feature_set = 'cuf_plus_extra'
    """
    df_preds = pd.read_sql(query_preds, conn)
    conn.close()
    return df_projects, df_snapshots, df_milestones, df_preds
