"""
Authentication & Officer Identity Router
Enforces secure SQLite credential verification with salted PBKDF2 hashing.
"""

import logging
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from src.api.db import get_db
from src.api.schemas import LoginRequest, RegisterRequest, AuthUserResponse
from src.api.auth import (
    create_access_token,
    get_current_user,
    verify_password,
    hash_password,
)
from src.api.user_store import (
    init_users_table,
    get_user_by_identifier,
    create_user,
    PRESET_OFFICERS,
)

logger = logging.getLogger("PAIMANA_API.Auth")

router = APIRouter(tags=["Authentication"])


@router.post("/api/auth/login", response_model=AuthUserResponse)
@router.post("/auth/login", response_model=AuthUserResponse, include_in_schema=False)
async def login_officer(req: LoginRequest):
    """Authenticate an official monitoring officer with verified credentials."""
    conn = get_db()
    init_users_table(conn, hash_password)

    clean_identifier = req.email.strip().lower()
    user = get_user_by_identifier(conn, clean_identifier)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Account not found. Please verify your email/username or register."
        )

    if not verify_password(req.password, user["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password. Please verify credentials."
        )

    user_payload = {
        "id": user["id"],
        "name": user["full_name"],
        "email": user["email"],
        "designation": user["designation"],
        "ministry": user["ministry"],
        "role": user["role"],
        "department_code": user.get("department_code", "MoSPI-CENTRAL"),
        "clearance_level": user.get("clearance_level", "Level-3 (General Access)"),
        "avatar": user.get("avatar", "GO"),
    }
    token = create_access_token(user_payload)
    return {**user_payload, "token": token}


@router.post("/api/auth/register", response_model=AuthUserResponse)
@router.post("/auth/register", response_model=AuthUserResponse, include_in_schema=False)
async def register_officer(req: RegisterRequest):
    """Register a new government officer credentials profile with hashed password."""
    conn = get_db()
    init_users_table(conn, hash_password)

    clean_email = req.email.strip().lower()
    existing = get_user_by_identifier(conn, clean_email)
    if existing:
        raise HTTPException(
            status_code=409,
            detail="An officer account with this email or username already exists. Please sign in."
        )

    if len(req.password or "") < 6:
        raise HTTPException(
            status_code=422,
            detail="Password must be at least 6 characters in length."
        )

    initials = "".join([part[0] for part in req.full_name.split()[:2]]).upper() or "GO"
    hashed_pwd = hash_password(req.password)

    new_user = create_user(
        conn,
        {
            "full_name": req.full_name.strip(),
            "email": clean_email,
            "designation": req.designation or "Project Monitoring Officer",
            "ministry": req.ministry or "Ministry of Statistics and Programme Implementation",
            "role": req.role or "Review Authority",
            "department_code": req.employee_id or "MoSPI-IPMD",
            "clearance_level": "Level-3 (Nodal Oversight)",
            "avatar": initials,
        },
        hashed_pwd,
    )

    user_payload = {
        "id": new_user["id"],
        "name": new_user["full_name"],
        "email": new_user["email"],
        "designation": new_user["designation"],
        "ministry": new_user["ministry"],
        "role": new_user["role"],
        "department_code": new_user.get("department_code", "MoSPI-IPMD"),
        "clearance_level": new_user.get("clearance_level", "Level-3 (Nodal Oversight)"),
        "avatar": new_user.get("avatar", initials),
    }
    token = create_access_token(user_payload)
    return {**user_payload, "token": token}


@router.get("/api/auth/me")
@router.get("/auth/me", include_in_schema=False)
async def get_current_user_profile(user=Depends(get_current_user)):
    """Return current authenticated user from JWT."""
    return user


@router.get("/api/auth/profiles", response_model=List[Dict[str, Any]])
@router.get("/auth/profiles", response_model=List[Dict[str, Any]], include_in_schema=False)
async def get_demo_profiles():
    """List available preset administrative officer profiles for reference."""
    return [
        {k: v for k, v in p.items() if k != "password"}
        for p in PRESET_OFFICERS
    ]
