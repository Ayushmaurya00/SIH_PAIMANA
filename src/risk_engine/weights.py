"""
Risk Engine Constants, Weights and Display Name Mappings
"""

import hashlib

FACTOR_DISPLAY_NAMES = {
    'expenditure_to_progress_ratio': 'Expenditure-to-progress ratio distortion',
    'delayed_milestones': 'Statutory & civil milestone slippages',
    'milestone_slippage_ratio': 'High proportion of delayed milestones',
    'agency_historical_overrun_avg': 'Implementing agency historical delay track record',
    'sector_historical_overrun_avg': 'Sector-level structural execution complexity',
    'state_historical_overrun_avg': 'State-level land acquisition & terrain friction',
    'expenditure_vs_time_gap': 'Expenditure pace disconnected from timeline elapsed',
    'progress_vs_time_gap': 'Physical progress lagging behind elapsed schedule',
    '12m_progress_gain': 'Sluggish 12-month progress velocity',
    'approved_cost_cr': 'Megaproject scale complexity & capital intensity',
    'is_megaproject': 'Megaproject scale (> ₹5,000 Cr) compounding friction',
    'planned_duration_months': 'Long project gestation cycle',
    'physical_progress_pct': 'Low cumulative physical progress'
}

# Hybrid Formula Weights
W_COST = 0.30
W_TIME = 0.30
W_MILESTONE = 0.20
W_MISMATCH = 0.20

HIGH_RISK_THRESHOLD = 58.0
MEDIUM_RISK_THRESHOLD = 32.0


def deterministic_variance(project_id: str, base: float, range_val: float) -> float:
    """Generate deterministic pseudo-random variance based on project_id."""
    seed_str = f"{project_id}:{base}:{range_val}"
    hash_val = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
    normalized = (hash_val % 10000) / 10000.0
    return base + (normalized - 0.5) * range_val
