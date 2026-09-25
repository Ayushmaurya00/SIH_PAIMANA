"""
MoSPI Registry Official Admin Router
Provides sovereign administrative console endpoints for officer provisioning,
personnel roster inspection, and account suspension/activation.
"""

import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel, EmailStr, Field

from src.api.db import get_db
from src.api.auth import require_role, hash_password
from src.api.user_store import (
    list_all_users,
    create_user,
    get_user_by_id,
    get_user_by_identifier,
    toggle_user_status,
)

logger = logging.getLogger("PAIMANA_API.Admin")

router = APIRouter(prefix="/api/admin", tags=["MoSPI Registry Administration"])


class ProvisionUserRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150, description="Full Name and Official Rank")
    email: EmailStr = Field(..., description="Official Government Email")
    department: str = Field(..., min_length=2, max_length=200, description="Ministry or Department Sector")
    role: str = Field(..., pattern="^(admin|employee|nodal_officer|auditor)$", description="Role clearance")
    temporary_password: str = Field(..., min_length=8, description="Initial One-Time Temporary Password")


class StatusToggleRequest(BaseModel):
    is_active: Optional[bool] = None


@router.get("/users", response_model=List[Dict[str, Any]])
async def get_personnel_roster(
    current_admin: Dict[str, Any] = Depends(require_role(["admin"]))
):
    """
    Returns complete roster of registered personnel excluding password hashes.
    Statutory clearance: MoSPI Registry Official ('admin') only.
    """
    conn = get_db()
    users = list_all_users(conn)
    roster = []
    for u in users:
        raw_role = u.get("role", "employee")
        role = "admin" if raw_role == "admin" else "employee"
        designation = (
            "MoSPI Registry Official" if role == "admin"
            else "Operations Employee"
        )
        roster.append({
            "id": u["id"],
            "email": u["email"],
            "full_name": u["full_name"],
            "department": u["department"],
            "role": role,
            "designation": designation,
            "is_active": bool(u.get("is_active", 1)),
            "created_at": u.get("created_at"),
        })
    return roster


@router.post("/users", status_code=201)
async def provision_officer_credentials(
    req: ProvisionUserRequest,
    current_admin: Dict[str, Any] = Depends(require_role(["admin"]))
):
    """
    Provisions new officer credentials with hashed password.
    Statutory clearance: MoSPI Registry Official ('admin') only.
    """
    conn = get_db()
    clean_email = req.email.strip().lower()

    existing = get_user_by_identifier(conn, clean_email)
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"An officer account with email '{clean_email}' already exists in the MoSPI Registry."
        )

    hashed_pwd = hash_password(req.temporary_password)
    target_role = "admin" if req.role == "admin" else "employee"
    new_user = create_user(
        conn,
        {
            "full_name": req.full_name.strip(),
            "email": clean_email,
            "department": req.department.strip(),
            "role": target_role,
        },
        hashed_pwd,
    )

    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to persist newly provisioned officer record.")

    role = "admin" if new_user.get("role") == "admin" else "employee"
    return {
        "status": "success",
        "message": f"Officer credentials provisioned for {clean_email}.",
        "user": {
            "id": new_user["id"],
            "email": new_user["email"],
            "full_name": new_user["full_name"],
            "department": new_user["department"],
            "role": role,
            "designation": (
                "MoSPI Registry Official" if role == "admin"
                else "Operations Employee"
            ),
            "is_active": bool(new_user.get("is_active", 1)),
            "created_at": new_user.get("created_at"),
        }
    }


@router.patch("/users/{user_id}/status")
async def toggle_personnel_status(
    user_id: int,
    req: Optional[StatusToggleRequest] = Body(None),
    current_admin: Dict[str, Any] = Depends(require_role(["admin"]))
):
    """
    Toggles or sets active/suspended status for a registered officer.
    Statutory clearance: MoSPI Registry Official ('admin') only.
    """
    conn = get_db()
    existing = get_user_by_id(conn, user_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Officer with Registry ID #{user_id} not found.")

    # Guard: prevent admin from accidentally suspending themselves
    if str(existing.get("email")).lower() == str(current_admin.get("email")).lower():
        if req and req.is_active is False:
            raise HTTPException(
                status_code=400,
                detail="Statutory safeguard: A MoSPI Registry Official cannot suspend their own active credential."
            )

    new_active_val = req.is_active if req else None
    updated = toggle_user_status(conn, user_id, new_active_val)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update officer statutory status.")

    return {
        "status": "success",
        "user_id": user_id,
        "is_active": bool(updated.get("is_active")),
        "message": f"Officer {updated['email']} status updated to {'Active' if updated.get('is_active') else 'Suspended'}."
    }
