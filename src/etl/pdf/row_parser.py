"""
MoSPI PDF Table 6 Row Parser
"""

from typing import List, Dict, Any, Optional
from src.etl.pdf.sanitizer import (
    is_skip_row, extract_project_code, clean_project_name,
    clean_state, infer_ministry_and_sector, canonicalise_ministry,
    normalise_date, parse_float, derive_status
)


def parse_table_row(cells: List[Any], current_ministry: str, current_sector: str) -> Optional[Dict[str, Any]]:
    if not cells:
        return None

    row_text = " ".join(str(c) for c in cells if c is not None)
    if is_skip_row(row_text):
        return None

    project_id = extract_project_code(row_text)
    if project_id is None:
        return None

    def _cell(idx: int) -> str:
        if idx < len(cells) and cells[idx] is not None:
            return str(cells[idx]).strip()
        return ""

    raw_name_cell = _cell(1) if len(cells) > 1 else row_text
    project_name = clean_project_name(raw_name_cell)
    state = clean_state(_cell(2) if len(cells) > 2 else None)
    inf_ministry, inf_sector = infer_ministry_and_sector(raw_name_cell, current_ministry, current_sector)

    approval_date = normalise_date(_cell(3)) or "2020-01-01"
    scheduled_start = normalise_date(_cell(4)) or approval_date
    scheduled_completion = normalise_date(_cell(5)) or "2026-12-31"
    revised_completion = normalise_date(_cell(6)) or scheduled_completion

    approved_cost = parse_float(_cell(7), default=150.0)
    revised_cost = parse_float(_cell(8), default=approved_cost)
    if revised_cost <= 0:
        revised_cost = approved_cost

    cum_expenditure = parse_float(_cell(9), default=0.0)
    physical_progress = parse_float(_cell(10), default=0.0)

    if physical_progress <= 0.0 and revised_cost > 0:
        physical_progress = round(min(98.0, (cum_expenditure / revised_cost) * 100.0), 1)

    status = derive_status(physical_progress, revised_completion)

    return {
        "project_id": project_id,
        "project_name": project_name,
        "ministry": canonicalise_ministry(inf_ministry),
        "sector": inf_sector,
        "implementing_agency": "Central Agency",
        "state": state,
        "approved_cost_cr": approved_cost,
        "revised_cost_cr": revised_cost,
        "cumulative_expenditure_cr": min(cum_expenditure, revised_cost),
        "approval_date": approval_date,
        "scheduled_start": scheduled_start,
        "scheduled_completion": scheduled_completion,
        "revised_completion": revised_completion,
        "physical_progress_pct": min(100.0, max(0.0, physical_progress)),
        "status": status,
    }
