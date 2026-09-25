"""
Database storage & management for authenticated officers.
Provides persistent SQLite operations and seed data for official MoSPI accounts.
"""

import time
import sqlite3
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger("PAIMANA_API.UserStore")

PRESET_OFFICERS = [
    {
        "id": "usr-admin-01",
        "email": "admin@mospi.gov.in",
        "username": "admin",
        "password": "Admin@MoSPI2026!",
        "full_name": "Chief Project Controller (MoSPI)",
        "designation": "Central Nodal Officer",
        "ministry": "Ministry of Statistics and Programme Implementation",
        "role": "Cabinet Review Authority",
        "department_code": "MoSPI-IPMD-HQ",
        "clearance_level": "Level-5 (Cabinet Secretariat)",
        "avatar": "CP",
    },
    {
        "id": "off-001",
        "email": "rajesh.sharma@mospi.gov.in",
        "username": "rajesh.sharma",
        "password": "Paimana@123",
        "full_name": "Dr. Rajesh Sharma, IAS",
        "designation": "Joint Secretary (IPMD)",
        "ministry": "Ministry of Statistics and Programme Implementation",
        "role": "Cabinet Review Authority",
        "department_code": "MoSPI-IPMD-01",
        "clearance_level": "Level-5 (Cabinet Secretariat)",
        "avatar": "RS",
    },
    {
        "id": "off-002",
        "email": "officer@mospi.gov.in",
        "username": "officer",
        "password": "Paimana@123",
        "full_name": "MoSPI Infrastructure Monitoring Officer",
        "designation": "Executive Monitoring Officer",
        "ministry": "Ministry of Statistics and Programme Implementation",
        "role": "Review Authority",
        "department_code": "MoSPI-CENTRAL",
        "clearance_level": "Level-3 (General Access)",
        "avatar": "OF",
    },
    {
        "id": "off-003",
        "email": "p.verma@nhai.gov.in",
        "username": "p.verma",
        "password": "Paimana@123",
        "full_name": "Pooja Verma, IDAS",
        "designation": "Chief General Manager (Coordination)",
        "ministry": "Ministry of Road Transport and Highways",
        "role": "Implementing Authority",
        "department_code": "MoRTH-NHAI-HQ",
        "clearance_level": "Level-3 (Nodal Project Oversight)",
        "avatar": "PV",
    },
    {
        "id": "off-004",
        "email": "v.sengupta@railnet.gov.in",
        "username": "v.sengupta",
        "password": "Paimana@123",
        "full_name": "Vikramaditya Sengupta",
        "designation": "Executive Director (Works)",
        "ministry": "Ministry of Railways",
        "role": "Implementing Authority",
        "department_code": "MoR-RB-WORKS",
        "clearance_level": "Level-4 (Zonal Infrastructure)",
        "avatar": "VS",
    },
    {
        "id": "off-v3",
        "email": "v.3@gmail.com",
        "username": "v.3",
        "password": "Paimana@123",
        "full_name": "V.3 Analytical Evaluator",
        "designation": "Demonstration & Simulation Sandbox",
        "ministry": "MoSPI / IPMD Analytical Sandbox",
        "role": "Demo Mode Evaluator",
        "department_code": "V3-SANDBOX-LAB",
        "clearance_level": "Level-Special (Simulation)",
        "avatar": "V3",
    },
    {
        "id": "emp-001",
        "email": "employee@company.com",
        "username": "employee_id",
        "password": "Employee@123",
        "full_name": "Project Operations Associate",
        "designation": "Project Operations Employee",
        "ministry": "Infrastructure Planning & Monitoring Division",
        "role": "Review Authority",
        "department_code": "PMO-OPERATIONS",
        "clearance_level": "Level-3 (General Access)",
        "avatar": "EM",
    },
]


def init_users_table(conn: sqlite3.Connection, hash_func) -> None:
    """Ensures users table exists and seeds official accounts."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            designation TEXT NOT NULL,
            ministry TEXT NOT NULL,
            role TEXT NOT NULL,
            department_code TEXT,
            clearance_level TEXT,
            avatar TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);")

    # Seed preset officers if table is empty or missing them
    for officer in PRESET_OFFICERS:
        row = conn.execute(
            "SELECT id FROM users WHERE LOWER(email) = LOWER(?)",
            (officer["email"],)
        ).fetchone()
        if not row:
            hashed = hash_func(officer["password"])
            conn.execute("""
                INSERT INTO users (
                    id, email, username, password_hash, full_name,
                    designation, ministry, role, department_code, clearance_level, avatar
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                officer["id"],
                officer["email"].lower(),
                officer["username"].lower(),
                hashed,
                officer["full_name"],
                officer["designation"],
                officer["ministry"],
                officer["role"],
                officer["department_code"],
                officer["clearance_level"],
                officer["avatar"]
            ))
    conn.commit()


def get_user_by_identifier(conn: sqlite3.Connection, identifier: str) -> Optional[Dict[str, Any]]:
    """Fetches user record by email or username."""
    clean = identifier.strip().lower()
    cursor = conn.execute("""
        SELECT * FROM users
        WHERE LOWER(email) = ? OR LOWER(username) = ?
    """, (clean, clean))
    row = cursor.fetchone()
    return dict(row) if row else None


def create_user(conn: sqlite3.Connection, user_data: Dict[str, Any], hashed_pwd: str) -> Dict[str, Any]:
    """Inserts a newly registered officer into the database."""
    user_id = f"off-{int(time.time())}"
    clean_email = user_data["email"].strip().lower()
    clean_username = user_data.get("username", clean_email.split("@")[0]).strip().lower()

    conn.execute("""
        INSERT INTO users (
            id, email, username, password_hash, full_name,
            designation, ministry, role, department_code, clearance_level, avatar
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        clean_email,
        clean_username,
        hashed_pwd,
        user_data["full_name"].strip(),
        user_data.get("designation", "Project Monitoring Officer"),
        user_data.get("ministry", "Ministry of Statistics and Programme Implementation"),
        user_data.get("role", "Review Authority"),
        user_data.get("department_code", "MoSPI-IPMD"),
        user_data.get("clearance_level", "Level-3 (Nodal Oversight)"),
        user_data.get("avatar", "GO")
    ))
    conn.commit()

    return get_user_by_identifier(conn, clean_email)
