"""
Unit and integration tests for MoSPI Registry Official Admin Router and RBAC dependencies.
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_primary_admin_login():
    """Verify primary MoSPI Registry Official account credentials and role."""
    res = client.post("/api/auth/login", json={
        "email": "admin@mospi.gov.in",
        "password": "Admin@MoSPI2026"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["role"] == "admin"
    assert data["designation"] == "MoSPI Registry Official"
    assert "token" in data


def test_admin_users_roster_rbac():
    """Verify GET /api/admin/users is restricted strictly to admin role."""
    # 1. Admin access
    admin_login = client.post("/api/auth/login", json={
        "email": "admin@mospi.gov.in",
        "password": "Admin@MoSPI2026"
    }).json()
    admin_token = admin_login["token"]

    res_admin = client.get("/api/admin/users", headers={"Authorization": f"Bearer {admin_token}"})
    assert res_admin.status_code == 200
    roster = res_admin.json()
    assert isinstance(roster, list)
    assert len(roster) > 0
    # Ensure password hashes are not leaked
    assert all("hashed_password" not in u and "password_hash" not in u for u in roster)

    # 2. Auditor access rejected with 403
    auditor_login = client.post("/api/auth/login", json={
        "email": "auditor@mospi.gov.in",
        "password": "Auditor@MoSPI2026"
    }).json()
    aud_token = auditor_login["token"]

    res_aud = client.get("/api/admin/users", headers={"Authorization": f"Bearer {aud_token}"})
    assert res_aud.status_code == 403
    assert "Statutory clearance error" in res_aud.json()["message"]


def test_provision_officer_and_toggle_status():
    """Test provisioning new officer credentials and status toggle via Admin API."""
    admin_login = client.post("/api/auth/login", json={
        "email": "admin@mospi.gov.in",
        "password": "Admin@MoSPI2026"
    }).json()
    admin_token = admin_login["token"]

    # Provision officer
    test_email = "test.nodal.officer@railnet.gov.in"
    res_post = client.post(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "full_name": "Test Nodal Officer",
            "email": test_email,
            "department": "Ministry of Railways",
            "role": "nodal_officer",
            "temporary_password": "TempPassword@2026",
        }
    )
    assert res_post.status_code in (201, 409)
    if res_post.status_code == 201:
        user_id = res_post.json()["user"]["id"]
        # Toggle status to suspended
        res_patch = client.patch(
            f"/api/admin/users/{user_id}/status",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"is_active": False}
        )
        assert res_patch.status_code == 200
        assert res_patch.json()["is_active"] is False


def test_auditor_restricted_from_mutation_actions():
    """Verify that an auditor cannot trigger alert review mutations."""
    auditor_login = client.post("/api/auth/login", json={
        "email": "auditor@mospi.gov.in",
        "password": "Auditor@MoSPI2026"
    }).json()
    aud_token = auditor_login["token"]

    res_rev = client.post(
        "/api/alerts/1/review",
        headers={"Authorization": f"Bearer {aud_token}"}
    )
    assert res_rev.status_code == 403
    assert "Statutory clearance error" in res_rev.json()["message"]
