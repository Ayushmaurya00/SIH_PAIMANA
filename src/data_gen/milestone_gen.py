"""
Milestone Sequence Generator
"""

import random
import datetime
from typing import List
from src.data_gen.models import Milestone, Project
from src.data_gen.naming import MILESTONE_TEMPLATES


def generate_milestones_for_project(
    project: Project,
    has_overrun: bool
) -> List[Milestone]:
    """Generates milestone records mapped to project sector."""
    milestone_names = MILESTONE_TEMPLATES.get(project.sector, MILESTONE_TEMPLATES["Generic"])
    num_milestones = len(milestone_names)
    total_duration_days = (project.scheduled_completion - project.scheduled_start).days
    milestones = []

    for m_num, m_name in enumerate(milestone_names):
        frac = (m_num + 1) / (num_milestones + 0.5)
        planned_days = int(total_duration_days * frac)
        planned_date = project.scheduled_start + datetime.timedelta(days=planned_days)

        achieved_date = None
        is_delayed = False
        milestone_req_prog = frac * 100.0

        if project.physical_progress_pct >= milestone_req_prog:
            if has_overrun and m_num >= 1:
                achieved_date = planned_date + datetime.timedelta(days=random.randint(30, 240))
                is_delayed = True
            else:
                achieved_date = planned_date - datetime.timedelta(days=random.randint(0, 30))
                is_delayed = False
        else:
            if has_overrun and m_num <= 3:
                is_delayed = True

        milestones.append(Milestone(
            project_id=project.project_id,
            milestone_name=m_name,
            planned_date=planned_date,
            achieved_date=achieved_date,
            is_delayed=is_delayed
        ))
    return milestones
