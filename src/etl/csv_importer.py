"""
PAIMANA AI - Automated CSV Scraper & ETL Ingestion
"""

import os
import sys
import time
import datetime
import sqlite3
import logging
from typing import Dict, Any, List, Optional
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.etl.cuf.schema import SECTOR_TO_MINISTRY_MAP

logger = logging.getLogger("PAIMANA_CSV_INGEST")


def clean_string_field(val: Any, default: str = "") -> str:
    if pd.isna(val) or val is None:
        return default
    s = str(val).strip()
    if s.lower() in ['nan', 'none', '', 'n/a', 'na', 'null', '-']:
        return default
    return s


def parse_float_field(val: Any, default: float = 0.0) -> float:
    if pd.isna(val) or val is None:
        return default
    try:
        return float(str(val).replace(',', '').strip())
    except (ValueError, TypeError):
        return default


def ingest_csv_file(csv_path: str, db_path: str, reference_month: Optional[str] = None) -> Dict[str, Any]:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    warnings: List[str] = []
    p_cnt, s_cnt = 0, 0
    snap_month = reference_month or str(datetime.date.today().replace(day=1).isoformat())

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    try:
        for row_idx, (_, row) in enumerate(df.iterrows(), start=1):
            raw_pid = row.get('project_id')
            pid = clean_string_field(raw_pid, f"PRJ-{int(time.time())}_{row_idx}")
            if pid.upper().startswith('PRJ-TOTAL') or pid.upper().startswith('PRJ-SUMMARY'):
                continue

            raw_pname = row.get('project_name')
            pname = clean_string_field(raw_pname, f"Imported Infrastructure Project {row_idx}")
            if pname.lower() in ['total', 'summary', 'all projects', 'grand total', 'none', '']:
                continue

            sector = clean_string_field(row.get('sector'), "Road Transport & Highways") or "Road Transport & Highways"
            raw_min = clean_string_field(row.get('ministry'), "")
            ministry = raw_min if raw_min else SECTOR_TO_MINISTRY_MAP.get(sector, "Ministry of Road Transport and Highways (MoRTH)")
            agency = clean_string_field(row.get('implementing_agency'), "Central PSU")
            state = clean_string_field(row.get('state'), "National")
            status = clean_string_field(row.get('status'), "On Track")

            app_cost = parse_float_field(row.get('approved_cost_cr'), 500.0)
            rev_cost = parse_float_field(row.get('revised_cost_cr'), app_cost)
            exp = parse_float_field(row.get('cumulative_expenditure_cr'), 0.0)
            prog = parse_float_field(row.get('physical_progress_pct'), 0.0)

            approval_date = clean_string_field(row.get('approval_date'), "2023-01-01")
            scheduled_start = clean_string_field(row.get('scheduled_start'), "2023-03-01")
            scheduled_completion = clean_string_field(row.get('scheduled_completion'), "2026-12-31")
            revised_completion = clean_string_field(row.get('revised_completion'), "2027-06-30")

            cur.execute("""
                INSERT INTO projects (
                    project_id, project_name, ministry, sector, implementing_agency, state,
                    approved_cost_cr, revised_cost_cr, cumulative_expenditure_cr,
                    physical_progress_pct, status, approval_date, scheduled_start,
                    scheduled_completion, revised_completion, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ON CONFLICT(project_id) DO UPDATE SET
                    project_name = excluded.project_name, ministry = excluded.ministry,
                    sector = excluded.sector, implementing_agency = excluded.implementing_agency,
                    state = excluded.state, approved_cost_cr = excluded.approved_cost_cr,
                    revised_cost_cr = excluded.revised_cost_cr,
                    cumulative_expenditure_cr = excluded.cumulative_expenditure_cr,
                    physical_progress_pct = excluded.physical_progress_pct, status = excluded.status
            """, (pid, pname, ministry, sector, agency, state, app_cost, rev_cost, exp, prog, status, approval_date, scheduled_start, scheduled_completion, revised_completion))
            p_cnt += 1

            cur.execute("INSERT OR REPLACE INTO monthly_snapshots (project_id, snapshot_month, revised_cost_cr, cumulative_expenditure_cr, physical_progress_pct, status) VALUES (?, ?, ?, ?, ?, ?)", (pid, snap_month, rev_cost, exp, prog, status))
            s_cnt += 1

            cur.execute("SELECT COUNT(*) FROM milestones WHERE project_id=?", (pid,))
            if cur.fetchone()[0] == 0:
                milestones_def = [
                    ("Statutory Environmental & Forest Clearance", "2024-03-01", "2024-03-01", 0),
                    ("Land Acquisition & Right of Way Handover", "2024-08-01", "2024-11-01", 1 if status in ['Delayed', 'Stalled'] else 0),
                    ("Detailed Engineering Design & Procurement", "2025-01-01", "2025-01-01", 0),
                    ("Major Structural Civil Construction Phase", "2025-09-01", None, 1 if status in ['Delayed', 'Stalled'] else 0),
                    ("Equipment Testing, Pre-Commissioning & Handover", scheduled_completion, None, 0)
                ]
                for m_name, p_dt, a_dt, is_d in milestones_def:
                    cur.execute("INSERT INTO milestones (project_id, milestone_name, planned_date, achieved_date, is_delayed) VALUES (?, ?, ?, ?, ?)", (pid, m_name, p_dt, a_dt, is_d))

        conn.commit()
        return {"status": "success", "total_rows_scanned": len(df), "projects_upserted": p_cnt, "snapshots_inserted": s_cnt, "warnings": warnings}
    finally:
        conn.close()
