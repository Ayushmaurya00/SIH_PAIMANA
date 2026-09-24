"""
Integration Tests: FastAPI REST Endpoints, Pydantic Schema Contracts & RAG Copilot
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.api.main import app
from src.api.auth import create_access_token

client = TestClient(app)

def _auth_headers():
    token = create_access_token({"email": "rajesh.sharma@mospi.gov.in", "clearance_level": "Level-5 (Cabinet Secretariat)", "id": "off-001", "name": "Dr. Rajesh Sharma"})
    return {"Authorization": f"Bearer {token}"}


def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] in ["healthy", "degraded"]
    assert "dependencies" in data
    assert "database" in data["dependencies"]
    assert data["dependencies"]["database"]["status"] == "connected"
    assert "ollama_llm" in data["dependencies"]
    assert "ml_models" in data["dependencies"]


def test_structured_404_error_handling():
    res = client.get("/api/projects/NON_EXISTENT_PROJECT_9999")
    assert res.status_code == 404
    body = res.json()
    assert body["status"] == "error"
    assert "message" in body
    assert body["code"] in [404, "PROJECT_NOT_FOUND"]


def test_structured_validation_error_handling():
    # Invalid query parameters (e.g. limit is string or outside range)
    res = client.get("/api/projects?limit=-5")
    assert res.status_code == 422
    body = res.json()
    assert body["status"] == "error"
    assert body["code"] == "VALIDATION_ERROR"
    assert "details" in body


def test_dashboard_summary_endpoint():
    res = client.get("/api/dashboard/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["total_projects"] >= 1
    assert data["total_approved_cost_cr"] > 0
    assert len(data["sector_distribution"]) > 0
    assert len(data["state_distribution"]) > 0
    assert len(data["top_at_risk_projects"]) <= 10


def test_project_explorer_endpoint():
    res = client.get("/api/projects?limit=10&risk_level=High")
    assert res.status_code == 200
    data = res.json()
    assert len(data["projects"]) >= 1
    assert data["total"] > 0
    for p in data["projects"]:
        assert p["risk_level"] == "High"


def test_project_detail_endpoint():
    # Fetch first project
    list_res = client.get("/api/projects?limit=1")
    pid = list_res.json()["projects"][0]["project_id"]

    res = client.get(f"/api/projects/{pid}")
    assert res.status_code == 200
    detail = res.json()
    assert detail["project_id"] == pid
    assert isinstance(detail["snapshots"], list) and len(detail["snapshots"]) >= 1
    assert isinstance(detail["milestones"], list)
    assert "top_factors" in detail


def test_early_warning_alerts_endpoint():
    res = client.get("/api/alerts?severity=High")
    assert res.status_code == 200
    alerts = res.json()
    assert len(alerts) > 0 and alerts[0]["severity"] == "High"
    c_res = client.get("/api/alerts/count?severity=High")
    assert c_res.status_code == 200 and c_res.json()["count"] == len(alerts)


def test_model_metrics_endpoint():
    res = client.get("/api/models/metrics")
    assert res.status_code == 200
    metrics = res.json()
    assert len(metrics) > 0
    fsets = {m["feature_set"] for m in metrics}
    assert "cuf_only" in fsets and "cuf_plus_extra" in fsets


def test_ai_copilot_rag_query():
    res = client.post("/api/assistant/query", json={"question": "Which sectors have highest cost overruns?"})
    assert res.status_code == 200
    body = res.json()
    assert len(body["answer"]) > 50
    assert body["confidence"] > 0.80
    assert body["grounded_verified"] is True
    assert "fallback_mode" in body
    assert isinstance(body["fallback_mode"], bool)
    assert "mode" in body
    assert body["mode"] in ["llm", "fallback"]


def test_import_report_endpoint():
    # Test CSV upload import
    csv_content = """project_id,project_name,ministry,sector,implementing_agency,state,approved_cost_cr,revised_cost_cr,cumulative_expenditure_cr,physical_progress_pct,status
PRJ-99999,Test Upload Project,Ministry of Railways,Railways,DFCCIL,Delhi,500.0,550.0,300.0,60.0,Delayed"""
    
    files = {
        'file': ('test_cuf.csv', csv_content, 'text/csv')
    }
    data = {'reference_month': '2026-08-01'}
    try:
        res = client.post("/api/import/report", files=files, data=data, headers=_auth_headers())
        assert res.status_code == 200
        body = res.json()
        assert body["status"] == "success"
        assert body["projects_processed"] >= 1
        assert body["files_processed"] >= 1
    finally:
        import sqlite3
        conn = sqlite3.connect("paimana.db", timeout=10)
        conn.execute("DELETE FROM projects WHERE project_id = 'PRJ-99999'")
        conn.execute("DELETE FROM monthly_snapshots WHERE project_id = 'PRJ-99999'")
        conn.execute("DELETE FROM milestones WHERE project_id = 'PRJ-99999'")
        conn.execute("DELETE FROM risk_scores WHERE project_id = 'PRJ-99999'")
        conn.execute("DELETE FROM alerts WHERE project_id = 'PRJ-99999'")
        conn.execute("DELETE FROM model_predictions WHERE project_id = 'PRJ-99999'")
        conn.commit()
        conn.close()


def test_ai_copilot_rag_single_project_fallback():
    """Verify single project drilldown returns 200 with telemetry even if Ollama is unreachable."""
    res = client.post("/api/assistant/query", json={"question": "Explain delay drivers for PRJ-00004", "context_project_id": "PRJ-00004"})
    assert res.status_code == 200
    body = res.json()
    assert "PRJ-00004" in body["answer"]
    assert len(body["sources"]) > 0
    assert body["sources"][0]["project_id"] == "PRJ-00004"
    assert body["confidence"] >= 0.90


def test_ai_copilot_rag_general_search_fallback():
    """Verify general project search returns top retrieved project matches without 500 error."""
    res = client.post("/api/assistant/query", json={"question": "highway railway infrastructure"})
    assert res.status_code == 200
    body = res.json()
    assert len(body["answer"]) > 50
    assert "sources" in body
    assert len(body["sources"]) > 0
    assert body["confidence"] >= 0.80


def test_export_risk_report_csv():
    """Verify CSV export endpoint generates valid CSV with correct headers."""
    res = client.get("/api/export/risk-report", headers=_auth_headers())
    assert res.status_code == 200
    assert "text/csv" in res.headers.get("content-type", "")
    assert "MoSPI_Portfolio_Risk_Report" in res.headers.get("content-disposition", "")
    content = res.text
    lines = content.strip().split("\n")
    assert len(lines) >= 2  # Header + at least 1 project row
    header = lines[0]
    assert "Project ID" in header
    assert "Sanctioned Outlay (Cr)" in header
    assert "Risk Score (0-100)" in header


def test_filter_options_endpoint():
    """Verify filter options returns lists of ministries and sectors."""
    res = client.get("/api/filters/options")
    assert res.status_code == 200
    data = res.json()
    assert "ministries" in data
    assert "sectors" in data
    assert len(data["ministries"]) > 0
    assert len(data["sectors"]) > 0


