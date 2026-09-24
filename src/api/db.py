"""
Database Connection & Persistence Utility for PAIMANA AI API
"""

import os
import sys
import json
import time
import sqlite3
import logging
from typing import Any, List
from src.api.schemas import APIError

logger = logging.getLogger("PAIMANA_API.DB")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(ROOT_DIR, os.getenv("DATABASE_PATH", "paimana.db"))
DB_RETRY_ATTEMPTS = int(os.getenv("DB_RETRY_ATTEMPTS", "3"))
DB_RETRY_DELAY_SEC = float(os.getenv("DB_RETRY_DELAY_SEC", "0.2"))


def get_db(retries: int = DB_RETRY_ATTEMPTS, delay: float = DB_RETRY_DELAY_SEC) -> sqlite3.Connection:
    """
    Acquires an SQLite connection with WAL mode and automated retry.
    """
    last_err = None
    for attempt in range(retries):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=10.0, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            # Enable WAL for concurrent readers + secure settings
            try:
                conn.execute("PRAGMA journal_mode=WAL;")
                conn.execute("PRAGMA synchronous=NORMAL;")
                conn.execute("PRAGMA foreign_keys=ON;")
                conn.execute("PRAGMA busy_timeout=5000;")
            except Exception:
                pass
            # Ensure indexes exist (idempotent)
            try:
                conn.execute("CREATE INDEX IF NOT EXISTS idx_projects_ministry ON projects(ministry)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_projects_sector ON projects(sector)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_projects_state ON projects(state)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_risk_score ON risk_scores(score DESC)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_risk_level ON risk_scores(risk_level)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_ms_proj_month ON monthly_snapshots(project_id, snapshot_month)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_milestones_proj ON milestones(project_id)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_alerts_sev_stat ON alerts(severity, status)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_model_pred_pid ON model_predictions(project_id)")
            except Exception:
                pass
            return conn
        except sqlite3.OperationalError as e:
            last_err = e
            time.sleep(delay * (attempt + 1))
    logger.error(f"Failed to connect to database at {DB_PATH} after {retries} retries: {last_err}")
    raise APIError(
        status_code=503,
        detail="Database connection unavailable. Please ensure paimana.db is initialized.",
        code="DB_UNAVAILABLE"
    )


def parse_json_payload(raw_val: Any) -> List[Any]:
    """Safely unpacks JSON lists or strings handling double-serialization."""
    if not raw_val:
        return []
    if isinstance(raw_val, list):
        return raw_val
    try:
        val = json.loads(raw_val)
        if isinstance(val, str):
            val = json.loads(val)
        return val if isinstance(val, list) else ([val] if val else [])
    except Exception:
        return []
