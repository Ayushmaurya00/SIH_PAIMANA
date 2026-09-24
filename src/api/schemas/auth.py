"""
Auth & AI Assistant Query Schema Definitions
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator

# EmailStr requires email-validator; fall back to regex if not installed
try:
    from pydantic import EmailStr as _EmailStr  # type: ignore
    import email_validator  # noqa: F401
    EmailStr = _EmailStr
except Exception:
    from typing import Annotated
    import re
    EmailStr = Annotated[str, Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", description="Email address")]  # fallback


class AssistantQueryRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=1000, description="User administrative inquiry")
    context_project_id: Optional[str] = Field(None, pattern=r'^PRJ-\d{5}$', description="Target 5-digit project identifier")


class AssistantQueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    confidence: float
    grounded_verified: bool = True
    fallback_mode: bool = False
    mode: str = "fallback"
    model_used: Optional[str] = None


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1, max_length=128)


class RegisterRequest(BaseModel):
    full_name: str = Field(default="Officer User", min_length=1, max_length=100)
    email: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1, max_length=128)
    employee_id: Optional[str] = Field(default="GOI-OFFICER", max_length=50)
    ministry: Optional[str] = Field(default="Ministry of Statistics and Programme Implementation", max_length=150)
    designation: Optional[str] = Field(default="Executive Monitoring Officer", max_length=150)
    role: Optional[str] = Field(default="Review Authority", max_length=100)


class AuthUserResponse(BaseModel):
    id: str
    name: str
    email: str
    designation: str
    ministry: str
    role: str
    department_code: str
    clearance_level: str
    token: str
    avatar: str
