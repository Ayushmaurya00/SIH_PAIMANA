"""
Database storage & management for authenticated officers.
Provides persistent SQLite operations and seed data for official MoSPI accounts.
"""

import sqlite3
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger("PAIMANA_API.UserStore")

OFFICIAL_SEED_USERS = [
    {"email": "admin@mospi.gov.in", "full_name": "MoSPI Registry Official", "department": "MoSPI Infrastructure Monitoring Division", "role": "admin", "password": "Admin@MoSPI2026"},
    {"email": "nodal@mospi.gov.in", "full_name": "Dr. Rajesh Sharma, IAS", "department": "Ministry of Statistics and Programme Implementation", "role": "employee", "password": "Nodal@MoSPI2026"},
    {"email": "auditor@mospi.gov.in", "full_name": "CAG Statutory Auditor", "department": "Comptroller and Auditor General of India", "role": "employee", "password": "Auditor@MoSPI2026"},
    {"email": "employee@company.com", "full_name": "Project Operations Associate", "department": "Infrastructure Planning & Monitoring Division", "role": "employee", "password": "Employee@MoSPI2026"},
    {"email": "rajesh.sharma@mospi.gov.in", "full_name": "Dr. Rajesh Sharma, IAS", "department": "Ministry of Statistics and Programme Implementation", "role": "employee", "password": "Paimana@123"},
    {"email": "p.verma@nhai.gov.in", "full_name": "Pooja Verma, IDAS", "department": "Ministry of Road Transport and Highways", "role": "employee", "password": "Paimana@123"},
    {"email": "v.sengupta@railnet.gov.in", "full_name": "Vikramaditya Sengupta", "department": "Ministry of Railways", "role": "employee", "password": "Paimana@123"},
    {"email": "ananya.iyer@niti.gov.in", "full_name": "Dr. Ananya Iyer", "department": "NITI Aayog / Cabinet Secretariat", "role": "employee", "password": "Paimana@123"},
    {"email": "v.3@gmail.com", "full_name": "V.3 Analytical Evaluator", "department": "MoSPI / IPMD Analytical Sandbox", "role": "employee", "password": "Paimana@123"},
]

PRESET_OFFICERS = OFFICIAL_SEED_USERS

_CREATE_USERS_DDL = """
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        department TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'employee')),
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""


def _needs_role_migration(conn: sqlite3.Connection) -> bool:
    """True if users table uses the legacy 3-role CHECK constraint."""
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='users'"
    ).fetchone()
    sql = row[0] if row else ""
    return "'employee'" not in sql and "nodal_officer" in sql


def _migrate_table_constraint(conn: sqlite3.Connection) -> None:
    """Recreate users table with the two-role CHECK constraint, preserving all rows."""
    conn.execute("ALTER TABLE users RENAME TO _users_migration_tmp;")
    conn.execute(_CREATE_USERS_DDL)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
    for r in conn.execute("SELECT * FROM _users_migration_tmp").fetchall():
        d = dict(r)
        role = "admin" if d.get("role") == "admin" else "employee"
        conn.execute(
            "INSERT OR IGNORE INTO users "
            "(id, email, hashed_password, full_name, department, role, is_active, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (d["id"], d["email"], d["hashed_password"], d["full_name"],
             d["department"], role, d.get("is_active", 1), d.get("created_at")),
        )
    conn.execute("DROP TABLE _users_migration_tmp;")
    conn.commit()


def _drain_legacy_backup(conn: sqlite3.Connection, hash_func) -> None:
    """Copy rows from users_legacy backup into users, then drop backup."""
    for r in conn.execute("SELECT * FROM users_legacy").fetchall():
        d = dict(r)
        email = (d.get("email") or "").strip().lower()
        if not email:
            continue
        if conn.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email,)).fetchone():
            continue
        raw = d.get("role", "")
        role = "admin" if raw == "admin" or "admin" in email or raw == "Cabinet Review Authority" else "employee"
        pwd = d.get("password_hash") or hash_func("Admin@MoSPI2026" if role == "admin" else "Paimana@123")
        dept = d.get("ministry") or d.get("department_code") or "MoSPI"
        conn.execute(
            "INSERT INTO users (email, hashed_password, full_name, department, role, is_active) "
            "VALUES (?, ?, ?, ?, ?, 1)",
            (email, pwd, d.get("full_name", email), dept, role),
        )
    conn.execute("DROP TABLE users_legacy;")
    conn.commit()


def init_users_table(conn: sqlite3.Connection, hash_func) -> None:
    """Ensures users table exists with the two-role schema and seeds official accounts."""
    cols = [r[1] for r in conn.execute("PRAGMA table_info(users)").fetchall()]

    if cols and ("hashed_password" not in cols or "department" not in cols):
        conn.execute("ALTER TABLE users RENAME TO users_legacy;")
        cols = []

    if not cols:
        conn.execute(_CREATE_USERS_DDL)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
        conn.commit()
    elif _needs_role_migration(conn):
        _migrate_table_constraint(conn)

    if conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_legacy'").fetchone():
        _drain_legacy_backup(conn, hash_func)

    for officer in OFFICIAL_SEED_USERS:
        row = conn.execute("SELECT id FROM users WHERE LOWER(email) = ?", (officer["email"].lower(),)).fetchone()
        hashed = hash_func(officer["password"])
        if not row:
            conn.execute(
                "INSERT INTO users (email, hashed_password, full_name, department, role, is_active) VALUES (?, ?, ?, ?, ?, 1)",
                (officer["email"].lower(), hashed, officer["full_name"], officer["department"], officer["role"]),
            )
        else:
            conn.execute(
                "UPDATE users SET hashed_password=?, full_name=?, department=?, role=?, is_active=1 WHERE LOWER(email)=?",
                (hashed, officer["full_name"], officer["department"], officer["role"], officer["email"].lower()),
            )
    conn.commit()


def get_user_by_identifier(conn: sqlite3.Connection, identifier: str) -> Optional[Dict[str, Any]]:
    """Fetches user record by email or username prefix."""
    clean = identifier.strip().lower()
    row = conn.execute(
        "SELECT * FROM users WHERE LOWER(email) = ? OR LOWER(email) LIKE ? ORDER BY id ASC LIMIT 1",
        (clean, f"{clean}@%"),
    ).fetchone()
    return dict(row) if row else None


def get_user_by_id(conn: sqlite3.Connection, user_id: int) -> Optional[Dict[str, Any]]:
    """Fetches user record by integer ID."""
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return dict(row) if row else None


def list_all_users(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Returns roster of all personnel excluding hashed passwords."""
    rows = conn.execute(
        "SELECT id, email, full_name, department, role, is_active, created_at FROM users ORDER BY id ASC"
    ).fetchall()
    return [dict(r) for r in rows]


def create_user(conn: sqlite3.Connection, user_data: Dict[str, Any], hashed_pwd: str) -> Dict[str, Any]:
    """Inserts a newly registered officer into the database."""
    clean_email = user_data["email"].strip().lower()
    role = user_data.get("role", "employee")
    if role not in ("admin", "employee"):
        role = "employee"
    cursor = conn.execute(
        "INSERT INTO users (email, hashed_password, full_name, department, role, is_active) VALUES (?, ?, ?, ?, ?, ?)",
        (clean_email, hashed_pwd, user_data["full_name"].strip(),
         user_data.get("department", "Ministry of Statistics and Programme Implementation"), role, 1),
    )
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
