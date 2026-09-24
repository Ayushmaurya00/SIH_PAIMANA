"""
Project, Telemetry & Metric Schema Definitions
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class ProjectSummary(BaseModel):
    project_id: str
    project_name: str
    ministry: str
    sector: str
    implementing_agency: str
    state: str
    approved_cost_cr: float
    revised_cost_cr: float
    cumulative_expenditure_cr: float
    physical_progress_pct: float
    status: str
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    previous_score: Optional[float] = None
    top_factor: Optional[str] = None


class MonthlySnapshotItem(BaseModel):
    snapshot_id: int
    project_id: str
    snapshot_month: str
    revised_cost_cr: float
    cumulative_expenditure_cr: float
    physical_progress_pct: float
    status: str


class MilestoneItem(BaseModel):
    milestone_id: int
    project_id: str
    milestone_name: str
    planned_date: str
    achieved_date: Optional[str] = None
    is_delayed: bool


class ProjectDetail(BaseModel):
    project_id: str
    project_name: str
    ministry: str
    sector: str
    implementing_agency: str
    state: str
    approved_cost_cr: float
    revised_cost_cr: float
    cumulative_expenditure_cr: float
    approval_date: str
    scheduled_start: str
    scheduled_completion: str
    revised_completion: Optional[str] = None
    physical_progress_pct: float
    status: str
    risk_score: float
    risk_level: str
    previous_score: Optional[float] = None
    top_factors: List[Any] = []
    prescriptive_actions: Optional[List[Any]] = None
    cost_overrun_prob: Optional[float] = None
    cost_overrun_pct_pred: Optional[float] = None
    cost_overrun_pct_lower: Optional[float] = None
    cost_overrun_pct_upper: Optional[float] = None
    time_overrun_prob: Optional[float] = None
    time_overrun_months_pred: Optional[float] = None
    time_delay_lower_months: Optional[float] = None
    time_delay_upper_months: Optional[float] = None
    snapshots: List[MonthlySnapshotItem] = []
    milestones: List[MilestoneItem] = []


class DashboardKPIs(BaseModel):
    total_projects: int
    total_approved_cost_cr: float
    total_revised_cost_cr: float
    total_expenditure_cr: float
    net_cost_overrun_pct: float
    delayed_projects_count: int
    stalled_projects_count: int
    on_track_projects_count: int
    completed_projects_count: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    sector_distribution: List[Dict[str, Any]]
    ministry_distribution: List[Dict[str, Any]]
    cost_tier_distribution: List[Dict[str, Any]]
    state_distribution: List[Dict[str, Any]]
    top_at_risk_projects: List[ProjectSummary]


class AlertItem(BaseModel):
    alert_id: int
    project_id: str
    project_name: str
    ministry: str
    sector: str
    implementing_agency: str
    approved_cost_cr: float
    risk_score: float
    risk_level: str
    triggered_at: str
    trigger_reason: str
    severity: str
    status: str
    prescriptive_action: Optional[str] = None
    lead_time_months: Optional[float] = None


class ModelMetricItem(BaseModel):
    metric_id: int
    model_name: str
    model_version: Optional[str] = None
    feature_set: str
    target: str
    split_type: Optional[str] = 'temporal_out_of_time'
    accuracy: Optional[float] = None
    f1_score: Optional[float] = None
    auc: Optional[float] = None
    rmse: Optional[float] = None
    mae: Optional[float] = None
    r2: Optional[float] = None
    lead_time_months: Optional[float] = None
    coverage_90_pct: Optional[float] = None
    evaluated_at: Optional[str] = None
