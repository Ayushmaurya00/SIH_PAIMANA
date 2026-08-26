"""
Pydantic response and request models for PAIMANA AI FastAPI service.
"""

from src.api.schemas.common import (
    APIError, ErrorResponse, RiskFactor, PrescriptiveAction
)
from src.api.schemas.projects import (
    ProjectSummary, MonthlySnapshotItem, MilestoneItem, ProjectDetail,
    DashboardKPIs, AlertItem, ModelMetricItem
)
from src.api.schemas.auth import (
    AssistantQueryRequest, AssistantQueryResponse,
    LoginRequest, RegisterRequest, AuthUserResponse
)

__all__ = [
    "APIError", "ErrorResponse", "RiskFactor", "PrescriptiveAction",
    "ProjectSummary", "MonthlySnapshotItem", "MilestoneItem", "ProjectDetail",
    "DashboardKPIs", "AlertItem", "ModelMetricItem",
    "AssistantQueryRequest", "AssistantQueryResponse",
    "LoginRequest", "RegisterRequest", "AuthUserResponse"
]
