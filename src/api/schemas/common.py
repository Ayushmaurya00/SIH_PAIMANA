"""
Common API Error & Fundamental Schema Definitions
"""

from typing import Optional, Any, Union
from pydantic import BaseModel


class APIError(Exception):
    def __init__(self, status_code: int, detail: str, code: Union[int, str] = "API_ERROR", details: Optional[Any] = None):
        self.status_code = status_code
        self.detail = detail
        self.code = code
        self.details = details
        super().__init__(detail)


class ErrorResponse(BaseModel):
    status: str = "error"
    code: Union[int, str]
    message: str
    details: Optional[Any] = None


class RiskFactor(BaseModel):
    factor: str
    contribution: float
    detail: Optional[str] = None


class PrescriptiveAction(BaseModel):
    title: str
    authority: str
    statutory_timeline_days: int
    recommended_action: str
    category: str
    triggering_factor: Optional[str] = None
    contribution_pts: Optional[float] = None
