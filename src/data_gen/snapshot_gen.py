"""
Monthly Snapshot Time-Series Generator
"""

import random
import datetime
import numpy as np
from typing import List
from src.data_gen.models import MonthlySnapshot, Project


def generate_snapshots_for_project(
    project: Project,
    has_overrun: bool,
    reference_date: datetime.date
) -> List[MonthlySnapshot]:
    """Generates 12 continuous monthly snapshots prior to reference date."""
    snapshots = []
    current_cost = project.approved_cost_cr
    cost_revision_idx = random.randint(3, 9) if has_overrun else 13

    start_progress = max(0.0, project.physical_progress_pct - random.uniform(15.0, 35.0))
    progress_steps = np.linspace(start_progress, project.physical_progress_pct, 12)

    start_exp = max(0.0, project.cumulative_expenditure_cr - (project.cumulative_expenditure_cr * random.uniform(0.20, 0.40)))
    exp_steps = np.linspace(start_exp, project.cumulative_expenditure_cr, 12)

    for m_idx in range(12):
        offset = 11 - m_idx
        snap_year = reference_date.year
        snap_month = reference_date.month - offset
        while snap_month <= 0:
            snap_month += 12
            snap_year -= 1
        snap_date = datetime.date(snap_year, snap_month, 1)

        if m_idx >= cost_revision_idx and has_overrun:
            current_cost = project.revised_cost_cr

        snap_prog = round(float(progress_steps[m_idx]), 1)
        snap_exp = round(float(exp_steps[m_idx]), 2)

        if snap_prog >= 100.0:
            snap_status = "Completed"
        elif has_overrun and m_idx >= 4:
            snap_status = "Delayed" if snap_prog > 10 else "Stalled"
        else:
            snap_status = "On Track"

        snapshots.append(MonthlySnapshot(
            project_id=project.project_id,
            snapshot_month=snap_date,
            revised_cost_cr=current_cost,
            cumulative_expenditure_cr=snap_exp,
            physical_progress_pct=snap_prog,
            status=snap_status
        ))
    return snapshots
