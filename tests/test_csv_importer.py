"""
Unit Tests: CSV Importer & Data Ingestion
"""

import os
import sys
import tempfile
import sqlite3
import pytest
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.etl.csv_importer import ingest_csv_file, clean_string_field, parse_float_field


def test_clean_string_field():
    assert clean_string_field(None, "default") == "default"
    assert clean_string_field("nan", "default") == "default"
    assert clean_string_field("None", "default") == "default"
    assert clean_string_field("  Railways  ") == "Railways"
    assert clean_string_field("N/A", "Unknown") == "Unknown"


def test_parse_float_field():
    assert parse_float_field("1,250.50") == 1250.50
    assert parse_float_field(None, 10.0) == 10.0
    assert parse_float_field("invalid", 5.0) == 5.0
    assert parse_float_field(100.5) == 100.5


def test_csv_importer_ingestion(tmp_path):
    # Create temporary database
    db_file = str(tmp_path / "test_paimana.db")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE projects (
            project_id TEXT PRIMARY KEY,
            project_name TEXT NOT NULL,
            ministry TEXT,
            sector TEXT,
            implementing_agency TEXT,
            state TEXT,
            approved_cost_cr REAL,
            revised_cost_cr REAL,
            cumulative_expenditure_cr REAL,
            physical_progress_pct REAL,
            status TEXT,
            approval_date TEXT,
            scheduled_start TEXT,
            scheduled_completion TEXT,
            revised_completion TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cur.execute("""
        CREATE TABLE monthly_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT,
            snapshot_month TEXT,
            revised_cost_cr REAL,
            cumulative_expenditure_cr REAL,
            physical_progress_pct REAL,
            status TEXT
        )
    """)
    
    cur.execute("""
        CREATE TABLE milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT,
            milestone_name TEXT,
            planned_date TEXT,
            achieved_date TEXT,
            is_delayed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

    # Create temporary CSV
    csv_file = str(tmp_path / "test_projects.csv")
    csv_data = """project_id,project_name,ministry,sector,implementing_agency,state,approved_cost_cr,revised_cost_cr,cumulative_expenditure_cr,physical_progress_pct,status
TEST-001,Test High Speed Rail,Ministry of Railways,Railways,NHSRCL,Gujarat,10000.0,12000.0,4500.0,40.0,Delayed
TEST-002,Test Highway Expansion,Ministry of Road Transport,Roads,NHAI,Maharashtra,3500.0,3500.0,3000.0,85.0,On Track
"""
    with open(csv_file, "w", encoding="utf-8") as f:
        f.write(csv_data)

    res = ingest_csv_file(csv_file, db_file, reference_month="2026-08-01")
    assert res["status"] == "success"
    assert res["projects_upserted"] == 2
    assert res["snapshots_inserted"] == 2

    # Verify records in database
    conn = sqlite3.connect(db_file)
    df_proj = pd.read_sql("SELECT * FROM projects", conn)
    assert len(df_proj) == 2
    assert "TEST-001" in df_proj["project_id"].values
    assert "TEST-002" in df_proj["project_id"].values

    df_snap = pd.read_sql("SELECT * FROM monthly_snapshots", conn)
    assert len(df_snap) == 2

    df_miles = pd.read_sql("SELECT * FROM milestones", conn)
    assert len(df_miles) == 10  # 5 default milestones per project
    conn.close()
