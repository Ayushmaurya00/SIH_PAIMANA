"""
Synthetic Project Entity Generator
"""

import random
import datetime
import numpy as np
from src.data_gen.models import Project
from src.data_gen.constants import MINISTRY_SECTOR_MAP, SECTOR_AGENCY_MAP
from src.data_gen.naming import (
    SECTOR_RISK_MODIFIER, AGENCY_RISK_MODIFIER, STATE_TERRAIN_MODIFIER,
    INDIAN_STATES, generate_realistic_project_name
)


def generate_single_project(i: int, reference_date: datetime.date):
    """Generates a single realistic central sector project record."""
    project_id = f"PRJ-{i:05d}"
    all_ministries = list(MINISTRY_SECTOR_MAP.keys())
    ministry_weights = [0.24, 0.20, 0.14, 0.08, 0.05, 0.03, 0.08, 0.04, 0.03, 0.02, 0.01, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01]
    ministry = np.random.choice(all_ministries, p=ministry_weights)
    sector = random.choice(MINISTRY_SECTOR_MAP[ministry])
    agencies = SECTOR_AGENCY_MAP.get(sector, ["Central Agency SPV"])
    agency = random.choice(agencies)
    state = random.choice(INDIAN_STATES)
    project_name = generate_realistic_project_name(sector, state, i)

    raw_cost = np.random.lognormal(mean=6.5, sigma=1.1) + 150.0
    approved_cost_cr = round(float(raw_cost), 2)

    approval_date = datetime.date(random.randint(2020, 2025), random.randint(1, 12), random.randint(1, 28))
    scheduled_start = approval_date + datetime.timedelta(days=random.randint(30, 150))
    base_duration_months = int(np.clip(30 + (approved_cost_cr / 600) * 4 + np.random.normal(0, 5), 24, 84))
    scheduled_completion = scheduled_start + datetime.timedelta(days=base_duration_months * 30)

    p_overrun = 0.35 + SECTOR_RISK_MODIFIER.get(sector, 0.0) + AGENCY_RISK_MODIFIER.get(agency, 0.0) + STATE_TERRAIN_MODIFIER.get(state, 0.0)
    if approved_cost_cr > 5000:
        p_overrun += 0.25
    elif approved_cost_cr > 1500:
        p_overrun += 0.12
    elif approved_cost_cr < 300:
        p_overrun -= 0.08
    p_overrun = float(np.clip(p_overrun, 0.05, 0.95))
    has_overrun = (random.random() < p_overrun)

    if has_overrun:
        delay_months = int(np.clip(np.random.gamma(shape=3.0, scale=6.0), 4, 72))
        revised_completion = scheduled_completion + datetime.timedelta(days=delay_months * 30)
        cost_escalation_pct = (delay_months * 0.8) + np.random.normal(12.0, 6.0)
        if approved_cost_cr > 3000:
            cost_escalation_pct *= 1.2
        cost_escalation_pct = float(np.clip(cost_escalation_pct, 5.0, 120.0))
        revised_cost_cr = round(approved_cost_cr * (1.0 + cost_escalation_pct / 100.0), 2)
    else:
        revised_completion = scheduled_completion
        revised_cost_cr = approved_cost_cr if random.random() > 0.1 else round(approved_cost_cr * 1.01, 2)

    total_planned_days = (scheduled_completion - scheduled_start).days
    elapsed_days = (reference_date - scheduled_start).days

    if elapsed_days <= 0:
        physical_progress_pct = 0.0
        cumulative_expenditure_cr = round(approved_cost_cr * 0.02, 2)
        status = "On Track"
    elif reference_date >= (revised_completion if revised_completion else scheduled_completion):
        if has_overrun and random.random() < 0.3:
            physical_progress_pct = round(float(np.random.uniform(55.0, 88.0)), 1)
            cumulative_expenditure_cr = round(revised_cost_cr * (physical_progress_pct / 100.0) * 1.15, 2)
            status = "Stalled" if random.random() < 0.4 else "Delayed"
        else:
            physical_progress_pct = 100.0
            cumulative_expenditure_cr = revised_cost_cr
            status = "Completed"
    else:
        effective_days = (revised_completion - scheduled_start).days if revised_completion else total_planned_days
        fraction_elapsed = float(np.clip(elapsed_days / max(effective_days, 1), 0.01, 0.98))
        if has_overrun:
            progress_lag = np.random.uniform(0.12, 0.35)
            physical_progress_pct = round(float(np.clip((fraction_elapsed - progress_lag) * 100.0, 2.0, 92.0)), 1)
            expenditure_ratio = (physical_progress_pct / 100.0) + np.random.uniform(0.08, 0.25)
            cumulative_expenditure_cr = round(float(min(revised_cost_cr, revised_cost_cr * expenditure_ratio)), 2)
            status = "Delayed" if physical_progress_pct > 15.0 else ("Stalled" if random.random() < 0.25 else "Delayed")
        else:
            physical_progress_pct = round(float(np.clip(fraction_elapsed * 100.0 + np.random.normal(0, 3), 5.0, 95.0)), 1)
            cumulative_expenditure_cr = round(float(approved_cost_cr * (physical_progress_pct / 100.0) * np.random.uniform(0.92, 1.02)), 2)
            status = "On Track"

    cumulative_expenditure_cr = min(cumulative_expenditure_cr, revised_cost_cr)
    proj = Project(
        project_id=project_id, project_name=project_name, ministry=ministry, sector=sector,
        implementing_agency=agency, state=state, approved_cost_cr=approved_cost_cr,
        revised_cost_cr=revised_cost_cr, cumulative_expenditure_cr=cumulative_expenditure_cr,
        approval_date=approval_date, scheduled_start=scheduled_start,
        scheduled_completion=scheduled_completion, revised_completion=revised_completion,
        physical_progress_pct=physical_progress_pct, status=status,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc)
    )
    return proj, has_overrun
