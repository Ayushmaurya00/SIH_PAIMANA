# REST API Reference & Developer Contract
## PAIMANA AI — Backend Service Interface Specification
**Ministry of Statistics and Programme Implementation (MoSPI) — Infrastructure and Project Monitoring Division (IPMD)**
*Smart India Hackathon (SIH) 2024 — Verified Technical Specification (v3.0)*
*Base URL: `http://localhost:8000` | OpenAPI Swagger: `http://localhost:8000/docs`*

---

## 1. Overview & General Standards

The **PAIMANA AI REST API** is built on **FastAPI 0.141** and follows standard RESTful conventions. 

### Request & Response Protocols:
* **Protocol:** HTTP/1.1 over JSON
* **Content-Type:** `application/json; charset=utf-8`
* **Authentication (Dev/Demo):** Open / Optional Bearer Token
* **Rate Limiting:** 100 requests / minute per client IP
* **CORS:** Pre-configured for Vite frontend (`http://localhost:5173`) and configurable via `.env`.

---

## 2. Global Error Handling Contract

All error responses adhere to standard HTTP status codes and return a structured JSON error body:

```json
{
  "detail": "Descriptive human-readable error message explaining the failure condition."
}
```

| HTTP Status Code | Description | Typical Trigger |
|---|---|---|
| `200 OK` | Request succeeded | Standard response for valid GET/POST calls |
| `400 Bad Request` | Invalid parameters or payload | Malformed JSON body or invalid query parameters |
| `404 Not Found` | Resource does not exist | Invalid `project_id` (e.g. `PRJ-999999`) |
| `429 Too Many Requests` | Rate limit exceeded | Client exceeded 100 requests in a 60-second window |
| `500 Internal Server Error`| Server processing exception | Database lock or unexpected computational failure |

---

## 3. Complete Endpoint Directory & Specifications

```
========================================================================================
PAIMANA AI — ENDPOINT TAXONOMY
========================================================================================
  [ Health & Monitoring ]
  GET    /api/health                       ── Health check & DB status

  [ Executive Dashboard & Aggregates ]
  GET    /api/dashboard/summary            ── Portfolio-level KPIs & risk totals
  GET    /api/dashboard/sector-breakdown   ── Sectoral outlays & project distribution
  GET    /api/dashboard/ministry-breakdown ── Ministry risk allocation & outlays

  [ Project Directory & Explorer ]
  GET    /api/filters/options              ── Distinct filter values (Ministries, Sectors)
  GET    /api/projects                     ── Filterable, paginated project grid
  GET    /api/projects/{id}                ── Exhaustive project detail dossier
  DELETE /api/projects/{id}                ── Permanent project deletion endpoint
  GET    /api/projects/{id}/risk           ── Isolated risk score & TreeSHAP factors

  [ Officer Authentication & Identity ]
  POST   /api/auth/login                   ── Authenticate officer or return session
  POST   /api/auth/register                ── Register new officer credentials
  GET    /api/auth/me                      ── List available preset demo profiles

  [ Early Warning & Alerts Hub ]
  GET    /api/alerts                       ── Active early warning alert list
  POST   /api/alerts/{id}/review           ── Acknowledge / mark alert as reviewed

  [ ML Models & Benchmarks ]
  GET    /api/models/metrics               ── Statistical vs ML comparative benchmarks

  [ AI Copilot & Data Export ]
  POST   /api/assistant/query              ── Grounded RAG natural language query
  POST   /api/import/report                ── Ingest new MoSPI Flash Report PDF
  GET    /api/export/risk-report           ── Streamed CSV export of at-risk portfolio
========================================================================================
```

---

### 3.1 `GET /api/health`
Checks backend service health, database connectivity, and loaded model bundles.

* **Response (200 OK):**
```json
{
  "status": "ok",
  "database": "connected",
  "total_projects": 1798,
  "ml_engine": "active",
  "models_loaded": ["cuf_only", "cuf_plus_extra"],
  "timestamp": "2026-09-02T01:00:00.000Z"
}
```

---

### 3.2 `GET /api/dashboard/summary`
Returns macro-level portfolio totals in Indian Crores for the executive dashboard.

* **Response (200 OK):**
```json
{
  "total_projects": 1798,
  "total_sanctioned_cost_cr": 3538492.5,
  "total_revised_cost_cr": 3812040.2,
  "total_expenditure_cr": 2193410.8,
  "high_risk_projects": 761,
  "medium_risk_projects": 498,
  "low_risk_projects": 539,
  "delayed_projects_count": 1228,
  "on_track_projects_count": 408,
  "completed_projects_count": 162
}
```

---

### 3.3 `GET /api/projects`
Retrieves a paginated list of projects with multi-dimensional filtering.

* **Query Parameters:**
  - `search` (string): Search text matching project name or ID.
  - `ministry` (string): Canonical ministry name filter.
  - `sector` (string): Sector filter.
  - `status` (string): `Delayed`, `On Track`, `Completed`, `Stalled`.
  - `risk_level` (string): `High`, `Medium`, `Low`.
  - `limit` (integer, default: 50, max: 500).
  - `offset` (integer, default: 0).

* **Example Request:**
```bash
curl -X GET "http://localhost:8000/api/projects?ministry=Ministry%20of%20Railways&risk_level=High&limit=5"
```

* **Response (200 OK):**
```json
[
  {
    "project_id": "PRJ-618417",
    "project_name": "Mumbai - Ahmedabad High Speed Rail Corridor",
    "ministry": "Ministry of Railways",
    "sector": "Railways",
    "state": "Gujarat / Maharashtra",
    "approved_cost_cr": 108000.0,
    "revised_cost_cr": 165000.0,
    "cumulative_expenditure_cr": 62400.0,
    "physical_progress_pct": 38.5,
    "status": "Delayed",
    "risk_score": 84.0,
    "risk_level": "High"
  }
]
```

---

### 3.4 `GET /api/projects/{id}`
Returns the comprehensive single-project dossier, including SHAP drivers, conformal prediction bounds, and milestones.

* **Example Request:**
```bash
curl -X GET "http://localhost:8000/api/projects/PRJ-618417"
```

* **Response (200 OK):**
```json
{
  "project_id": "PRJ-618417",
  "project_name": "Mumbai - Ahmedabad High Speed Rail Corridor",
  "ministry": "Ministry of Railways",
  "sector": "Railways",
  "implementing_agency": "NHSRCL",
  "state": "Gujarat / Maharashtra",
  "approved_cost_cr": 108000.0,
  "revised_cost_cr": 165000.0,
  "cumulative_expenditure_cr": 62400.0,
  "scheduled_start": "2017-09-14",
  "scheduled_completion": "2023-12-31",
  "revised_completion": "2028-12-31",
  "physical_progress_pct": 38.5,
  "status": "Delayed",
  "risk_score": 84.0,
  "risk_level": "High",
  "top_factors": [
    { "factor": "Forest & Coastal Regulation Zone (CRZ) Clearance Lags", "contribution": 18.4, "detail": "Environmental stage-gate delay exceeding 18 months." },
    { "factor": "State Right-of-Way Handover Resistance (Palghar)", "contribution": 12.1, "detail": "Land acquisition pacing below 40% threshold." }
  ],
  "prescriptive_actions": [
    "Escalate to Ministry Secretary / Project Monitoring Group (PMG) within 30 days.",
    "Commission independent site inspection to assess ground-level bottlenecks.",
    "Issue show-cause notice to implementing agency on timeline slippage."
  ],
  "cost_overrun_pct_pred": 52.8,
  "cost_overrun_pct_lower": 45.0,
  "cost_overrun_pct_upper": 58.2,
  "time_delay_lower_months": 36.0,
  "time_delay_upper_months": 48.0,
  "milestones": [
    { "milestone_name": "Commissioning & Commercial Operations", "planned_date": "2023-12-31", "achieved_date": null, "is_delayed": true }
  ]
}
```

---

### 3.5 `POST /api/assistant/query`
Executes grounded RAG retrieval and Google Gemini AI reasoning (with automatic failover and deterministic fallback).

* **Example Request:**
```bash
curl -X POST "http://localhost:8000/api/assistant/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the total expenditure in the Power sector and which project has the highest risk?", "context_project_id": null}'
```

* **Response (200 OK):**
```json
{
  "answer": "In the Power Generation & Transmission sector, the cumulative expenditure stands at ₹3,12,450 Cr across 103 monitored projects. The project exhibiting the highest risk is [PRJ-709856] (Subansiri Lower Hydroelectric Project, Risk Score: 88.2, +92.4% cost escalation) primarily driven by geological tunneling challenges and monsoon flood damage.",
  "sources": [{"project_id": "PRJ-709856", "project_name": "Subansiri Lower Hydroelectric Project", "score": 88.2}],
  "confidence": 0.98,
  "grounded_verified": true,
  "fallback_mode": false,
  "mode": "llm",
  "model_used": "gemini-3.6-flash"
}
```

---

### 3.6 `POST /api/auth/login`
Authenticates a government monitoring officer or activates a demo session profile.

* **Request Body:**
```json
{
  "email": "rajesh.sharma@mospi.gov.in",
  "password": "SecurePassword@2026"
}
```

* **Response (200 OK):**
```json
{
  "id": "off-001",
  "name": "Dr. Rajesh Sharma, IAS",
  "email": "rajesh.sharma@mospi.gov.in",
  "designation": "Joint Secretary (IPMD)",
  "ministry": "Ministry of Statistics and Programme Implementation",
  "role": "Cabinet Review Authority",
  "department_code": "MoSPI-IPMD-01",
  "clearance_level": "Level-5 (Cabinet Secretariat)",
  "token": "jwt-off-001-1788269000",
  "avatar": "RS"
}
```

---

### 3.7 `GET /api/export/risk-report`
Streams the entire at-risk portfolio as a standardized CSV file for administrative distribution.

* **Example Request:**
```bash
curl -X GET "http://localhost:8000/api/export/risk-report" -o MoSPI_Risk_Report_June2026.csv
```

