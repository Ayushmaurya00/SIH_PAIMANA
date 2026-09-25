"""
Database storage & management for authenticated officers.
Provides persistent SQLite operations and seed data for official MoSPI accounts.
"""

import sqlite3
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger("PAIMANA_API.UserStore")

OFFICIAL_SEED_USERS = [
    {
        "email": "admin@mospi.gov.in",
        "full_name": "MoSPI Registry Official",
        "department": "MoSPI Infrastructure Monitoring Division",
        "role": "admin",
        "password": "Admin@MoSPI2026",
    },
    {
        "email": "nodal@mospi.gov.in",
        "full_name": "Dr. Rajesh Sharma, IAS",
        "department": "Ministry of Statistics and Programme Implementation",
        "role": "nodal_officer",
        "password": "Nodal@MoSPI2026",
    },
    {
        "email": "auditor@mospi.gov.in",
        "full_name": "CAG Statutory Auditor",
        "department": "Comptroller and Auditor General of India",
        "role": "auditor",
        "password": "Auditor@MoSPI2026",
    },
    {
        "email": "employee@company.com",
        "full_name": "Project Operations Associate",
        "department": "Infrastructure Planning & Monitoring Division",
        "role": "nodal_officer",
        "password": "Employee@123",
    },
]

PRESET_OFFICERS = OFFICIAL_SEED_USERS


def init_users_table(conn: sqlite3.Connection, hash_func) -> None:
    """Ensures users table exists with statutory schema and seeds official accounts."""
    cols = [r[1] for r in conn.execute("PRAGMA table_info(users)").fetchall()]
    if cols and ("hashed_password" not in cols or "department" not in cols):
        conn.execute("ALTER TABLE users RENAME TO users_legacy;")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            department TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'nodal_officer', 'auditor')),
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")

    # Migrate legacy rows if present
    legacy_exists = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users_legacy'"
    ).fetchone()
    if legacy_exists:
        legacy_rows = conn.execute("SELECT * FROM users_legacy").fetchall()
        for r in legacy_rows:
            d = dict(r)
            email = d.get("email", "").strip().lower()
            if not email:
                continue
            exists = conn.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email,)).fetchone()
            if not exists:
                role = "admin" if ("admin" in email or d.get("role") == "Cabinet Review Authority") else "nodal_officer"
                pwd_hash = d.get("password_hash") or hash_func("Admin@MoSPI2026" if role == "admin" else "Paimana@123")
                dept = d.get("ministry") or d.get("department_code") or "MoSPI"
                conn.execute("""
                    INSERT INTO users (email, hashed_password, full_name, department, role, is_active)
                    VALUES (?, ?, ?, ?, ?, 1)
                """, (email, pwd_hash, d.get("full_name", email), dept, role))
        conn.execute("DROP TABLE users_legacy;")
        conn.commit()

    # Seed official statutory accounts
    for officer in OFFICIAL_SEED_USERS:
        row = conn.execute(
            "SELECT id FROM users WHERE LOWER(email) = ?",
            (officer["email"].lower(),)
        ).fetchone()
        if not row:
            hashed = hash_func(officer["password"])
            conn.execute("""
                INSERT INTO users (email, hashed_password, full_name, department, role, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (
                officer["email"].lower(),
                hashed,
                officer["full_name"],
                officer["department"],
                officer["role"],
            ))
    conn.commit()


def get_user_by_identifier(conn: sqlite3.Connection, identifier: str) -> Optional[Dict[str, Any]]:
    """Fetches user record by email or username prefix."""
    clean = identifier.strip().lower()
    cursor = conn.execute("""
        SELECT * FROM users
        WHERE LOWER(email) = ? OR LOWER(email) LIKE ?
        ORDER BY id ASC LIMIT 1
    """, (clean, f"{clean}@%"))
    row = cursor.fetchone()
    return dict(row) if row else None


def get_user_by_id(conn: sqlite3.Connection, user_id: int) -> Optional[Dict[str, Any]]:
    """Fetches user record by integer ID."""
    cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    return dict(row) if row else None


def list_all_users(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Returns roster of all personnel excluding hashed passwords."""
    cursor = conn.execute("""
        SELECT id, email, full_name, department, role, is_active, created_at
        FROM users
        ORDER BY id ASC
    """)
    return [dict(r) for r in cursor.fetchall()]


def create_user(conn: sqlite3.Connection, user_data: Dict[str, Any], hashed_pwd: str) -> Dict[str, Any]:
    """Inserts a newly registered officer into the database."""
    clean_email = user_data["email"].strip().lower()
    role = user_data.get("role", "nodal_officer")
    if role not in ("admin", "nodal_officer", "auditor"):
        role = "nodal_officer"

    cursor = conn.execute("""
        INSERT INTO users (email, hashed_password, full_name, department, role, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        clean_email,
        hashed_pwd,
        user_data["full_name"].strip(),
        user_data.get("department", "Ministry of Statistics and Programme Implementation"),
        role,
        1
    ))
    conn.commit()
    return get_user_by_id(conn, cursor.lastrowid)


def toggle_user_status(conn: sqlite3.Connection, user_id: int, new_status: Optional[bool] = None) -> Optional[Dict[str, Any]]:
    """Toggles or sets active state of a user."""
    user = get_user_by_id(conn, user_id)
    if not user:
        return None
    target_active = (not bool(user["is_active"])) if new_status is None else bool(new_status)
    conn.execute("UPDATE users SET is_active = ? WHERE id = ?", (1 if target_active else 0, user_id))
    conn.commit()
    return get_user_by_id(conn, user_id)
