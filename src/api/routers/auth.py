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

    stored_hash = user.get("hashed_password") or user.get("password_hash")
    if not stored_hash or not verify_password(req.password, stored_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password. Please verify credentials."
        )

    if not user.get("is_active", 1):
        raise HTTPException(
            status_code=403,
            detail="Account suspended by MoSPI Registry Official. Please contact Central Administration."
        )

    role = user.get("role", "nodal_officer")
    designation = (
        "MoSPI Registry Official" if role == "admin"
        else "Nodal Desk Officer" if role == "nodal_officer"
        else "Read-Only Auditor" if role == "auditor"
        else user.get("designation", "Project Monitoring Officer")
    )
    dept = user.get("department") or user.get("ministry") or "MoSPI Infrastructure Monitoring Division"
    initials = "".join([part[0] for part in user["full_name"].split()[:2]]).upper() or "GO"

    user_payload = {
        "id": str(user["id"]),
        "name": user["full_name"],
        "email": user["email"],
        "department": dept,
        "designation": designation,
        "ministry": dept,
        "role": role,
        "is_active": bool(user.get("is_active", 1)),
        "department_code": user.get("department_code", "MoSPI-IPMD"),
        "clearance_level": "Level-5 (Cabinet Secretariat)" if role == "admin" else ("Level-3 (Nodal Oversight)" if role == "nodal_officer" else "Level-2 (Auditor)"),
        "avatar": initials,
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
    target_role = "nodal_officer"
    if req.role in ("admin", "nodal_officer", "auditor"):
        target_role = req.role

    dept = req.ministry or "Ministry of Statistics and Programme Implementation"
    new_user = create_user(
        conn,
        {
            "full_name": req.full_name.strip(),
            "email": clean_email,
            "department": dept,
            "role": target_role,
        },
        hashed_pwd,
    )

    designation = (
        "MoSPI Registry Official" if target_role == "admin"
        else "Nodal Desk Officer" if target_role == "nodal_officer"
        else "Read-Only Auditor"
    )

    user_payload = {
        "id": str(new_user["id"]),
        "name": new_user["full_name"],
        "email": new_user["email"],
        "department": new_user["department"],
        "designation": designation,
        "ministry": new_user["department"],
        "role": new_user["role"],
        "is_active": bool(new_user.get("is_active", 1)),
        "department_code": req.employee_id or "MoSPI-IPMD",
        "clearance_level": "Level-3 (Nodal Oversight)",
        "avatar": initials,
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
