"""
CUF Data Cleaning & Normalization Routine
"""

import re
import datetime
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List
from src.etl.cuf.schema import COLUMN_MAPPINGS, VALID_STATUSES
from src.etl.cuf.ministry_resolver import resolve_ministry_and_sector


def normalize_columns(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    rename_map = {}
    unmapped = []
    for col in df.columns:
        cleaned = str(col).strip().lower().replace("\n", " ")
        if cleaned in COLUMN_MAPPINGS:
            rename_map[col] = COLUMN_MAPPINGS[cleaned]
        else:
            unmapped.append(col)
    return df.rename(columns=rename_map), unmapped


def parse_date(val: Any, fallback: datetime.date) -> datetime.date:
    if pd.isnull(val) or val is None or str(val).strip() in ['', 'NaT', 'None', 'nan']:
        return fallback
    try:
        return pd.to_datetime(str(val)).date()
    except Exception:
        return fallback


def clean_cuf_row(row: pd.Series, ref_date: datetime.date) -> Dict[str, Any]:
    pid = str(row.get('project_id', '')).strip()
    raw_pname = str(row.get('project_name', f'Infrastructure Project {pid}')).strip()
    pname = re.sub(r'\s*\([^\)]*\)\s*\(-\)\s*\(-\)\s*$', '', raw_pname)
    pname = re.sub(r'\s*\(-\)\s*\(-\)\s*$', '', pname)
    pname = re.sub(r'\s*\n\s*', ' ', pname)
    pname = re.sub(r'\s{2,}', ' ', pname).strip() or f'Infrastructure Project {pid}'
    agency = str(row.get('implementing_agency', 'Central Agency SPV')).strip() or 'Central Agency SPV'
    raw_min = str(row.get('ministry', '')).strip()
    raw_sec = str(row.get('sector', '')).strip()
    if raw_min and raw_min.lower() not in ['nan', 'none', '', 'n/a', 'na', 'null', '-']:
        ministry = raw_min
        sector = raw_sec or "Central Infrastructure"
    else:
        ministry, sector = resolve_ministry_and_sector(raw_min, raw_sec, pname, agency)
    state = str(row.get('state', 'National')).strip() or 'National'

    app_cost = float(np.clip(pd.to_numeric(row.get('approved_cost_cr'), errors='coerce') or 150.0, 150.0, 500000.0))
    rev_cost = float(np.clip(pd.to_numeric(row.get('revised_cost_cr'), errors='coerce') or app_cost, app_cost * 0.5, 1000000.0))
    cum_exp = float(np.clip(pd.to_numeric(row.get('cumulative_expenditure_cr'), errors='coerce') or 0.0, 0.0, rev_cost * 1.5))
    prog_pct = float(np.clip(pd.to_numeric(row.get('physical_progress_pct'), errors='coerce') or 0.0, 0.0, 100.0))

    approval_date = parse_date(row.get('approval_date'), ref_date - datetime.timedelta(days=730))
    sched_start = parse_date(row.get('scheduled_start'), approval_date + datetime.timedelta(days=60))
    sched_comp = parse_date(row.get('scheduled_completion'), sched_start + datetime.timedelta(days=1095))
    rev_comp = parse_date(row.get('revised_completion'), sched_comp)

    raw_status = str(row.get('status', '')).strip().title()
    if raw_status in VALID_STATUSES:
        status = raw_status
    elif prog_pct >= 99.0:
        status = "Completed"
    elif rev_comp and rev_comp < ref_date:
        status = "Delayed"
    else:
        status = "On Track"

    return {
        "project_id": pid, "project_name": pname, "ministry": ministry, "sector": sector,
        "implementing_agency": agency, "state": state, "approved_cost_cr": round(app_cost, 2),
        "revised_cost_cr": round(rev_cost, 2), "cumulative_expenditure_cr": round(cum_exp, 2),
        "approval_date": approval_date, "scheduled_start": sched_start,
        "scheduled_completion": sched_comp, "revised_completion": rev_comp,
        "physical_progress_pct": round(prog_pct, 1), "status": status
    }
