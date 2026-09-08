"""
Unit & Integration Tests: CUFAdapter Real-World Data Ingestion & Validation
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

from src.etl.cuf_adapter import CUFAdapter


@pytest.fixture
def temp_cuf_csv():
    """Creates a temporary sample real-world CUF CSV file."""
    data = [
        {
            "Project Code": "REAL-001",
            "Project Title": "NH-48 6-Lane Expressway (Vadodara-Surat)",
            "Ministry / Department": "Ministry of Road Transport and Highways",
            "Sector Name": "Roads and Highways",
            "Executing Agency": "NHAI",
            "Location": "Gujarat",
            "Approved Cost (₹ Cr)": 2850.5,
            "Latest Revised Cost": 3120.0,
            "Cumulative Expenditure": 1420.0,
            "Date of Sanction": "2021-03-15",
            "Actual / Scheduled Start": "2021-06-01",
            "Original Completion Date": "2025-12-31",
            "Anticipated Completion Date": "2026-06-30",
            "Physical Progress (%)": 48.5,
            "Monitoring Status": "Delayed"
        },
        {
            "Project Code": "REAL-002",
            "Project Title": "Solar Mega Park 1000MW",
            "Ministry / Department": "Ministry of New and Renewable Energy",
            "Sector Name": "Renewable Energy",
            "Executing Agency": "SECI",
            "Location": "Rajasthan",
            "Approved Cost (₹ Cr)": 4500.0,
            "Latest Revised Cost": 4500.0,
            "Cumulative Expenditure": 2100.0,
            "Date of Sanction": "2022-01-10",
            "Actual / Scheduled Start": "2022-04-01",
            "Original Completion Date": "2026-03-31",
            "Anticipated Completion Date": "",
            "Physical Progress (%)": 52.0,
            "Monitoring Status": "On Track"
        }
    ]
    df = pd.DataFrame(data)
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w", newline="", encoding="utf-8") as f:
        df.to_csv(f.name, index=False)
        temp_path = f.name
    yield temp_path
    try:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    except Exception:
        pass


@pytest.fixture
def temp_dirty_csv():
    """Creates a CUF CSV with common data quality anomalies."""
    data = [
        {
            "Project ID": "DIRTY-001",
            "Project Name": "Deep Water Port Terminal",
            "Ministry": "Ministry of Ports, Shipping and Waterways",
            "Sector": "Ports and Shipping",
            "Implementing Agency": "JNPT",
            "State": "Maharashtra",
            "Approved Cost (Cr)": -500.0,  # Negative outlay
            "Revised Cost (Cr)": 1800.0,
            "Cumulative Expenditure (Cr)": -50.0,  # Negative expenditure
            "Approval Date": "invalid-date",
            "Scheduled Start": "2020-01-01",
            "Scheduled Completion": "2024-01-01",
            "Physical Progress (%)": 150.0,  # > 100% progress
            "Status": "UNKNOWN_CUSTOM_STATUS"
        }
    ]
    df = pd.DataFrame(data)
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w", newline="", encoding="utf-8") as f:
        df.to_csv(f.name, index=False)
        temp_path = f.name
    yield temp_path
    try:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    except Exception:
        pass


@pytest.fixture
def temp_db():
    """Creates a temporary SQLite database."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        temp_path = f.name
    yield temp_path
    try:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    except Exception:
        pass


def test_cuf_adapter_ingestion_success(temp_cuf_csv, temp_db):
    """Test successful ingestion of varied CUF column naming formats."""
    adapter = CUFAdapter()
    report = adapter.validate_and_ingest(csv_path=temp_cuf_csv, db_path=temp_db)

    assert report["status"] == "completed"
    assert report["inserted_projects"] == 2
    assert report["failed_rows_count"] == 0

    conn = sqlite3.connect(temp_db)
    df = pd.read_sql("SELECT * FROM projects", conn)
    conn.close()

    assert len(df) == 2
    assert "REAL-001" in df["project_id"].values
    assert "REAL-002" in df["project_id"].values


def test_cuf_adapter_idempotency(temp_cuf_csv, temp_db):
    """Test running ingestion twice performs updates without duplicating rows."""
    adapter = CUFAdapter()
    rep1 = adapter.validate_and_ingest(csv_path=temp_cuf_csv, db_path=temp_db)
    assert rep1["inserted_projects"] == 2

    # Second run should update, not re-insert
    rep2 = adapter.validate_and_ingest(csv_path=temp_cuf_csv, db_path=temp_db)
    assert rep2["inserted_projects"] == 0
    assert rep2["updated_projects"] == 2

    conn = sqlite3.connect(temp_db)
    count = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
    conn.close()
    assert count == 2, "Row count must remain 2 after re-ingestion"


def test_cuf_adapter_data_quality_sanitization(temp_dirty_csv, temp_db):
    """Test automatic sanitization of negative costs, progress bounds, and bad statuses."""
    adapter = CUFAdapter()
    report = adapter.validate_and_ingest(csv_path=temp_dirty_csv, db_path=temp_db)

    assert report["status"] == "completed"
    assert report["inserted_projects"] == 1
    assert report["warnings_count"] > 0

    conn = sqlite3.connect(temp_db)
    row = conn.execute("SELECT approved_cost_cr, physical_progress_pct, status FROM projects WHERE project_id = 'DIRTY-001'").fetchone()
    conn.close()

    approved_cost, progress, status = row
    assert approved_cost >= 150.0, "Negative cost must be sanitized to positive threshold"
    assert progress <= 100.0, "Progress >100% must be clipped"
    assert status in {"On Track", "Delayed", "Stalled", "Completed"}, "Status must be normalized"


def test_cuf_adapter_missing_required_columns(temp_db):
    """Test error raising when essential columns cannot be mapped."""
    bad_df = pd.DataFrame([{"Arbitrary Header": "123"}])
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w", newline="") as f:
        bad_df.to_csv(f.name, index=False)
        bad_csv = f.name

    adapter = CUFAdapter()
    with pytest.raises(ValueError) as exc:
        adapter.validate_and_ingest(csv_path=bad_csv, db_path=temp_db)
    assert "missing required columns" in str(exc.value).lower()
    os.remove(bad_csv)
