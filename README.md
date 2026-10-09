<div align="center">

# 🏛️ PAIMANA AI — MoSPI Central Sector Project Intelligence
### **Predictive Early Warning, SHAP Explainability & Prescriptive Decision-Support System**
*Aligned with the Infrastructure and Project Monitoring Division (IPMD), Ministry of Statistics and Programme Implementation (MoSPI), Government of India.*

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20v2.0-009688.svg?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Tailwind-61DAFB.svg?style=flat-square&logo=react)](https://reactjs.org)
[![XGBoost](https://img.shields.io/badge/ML%20Engine-XGBoost%20%2B%20TreeSHAP-FF6600.svg?style=flat-square)](https://xgboost.readthedocs.io)
[![System Audit](https://img.shields.io/badge/System%20Audit-25%2F25%20Passing-brightgreen.svg?style=flat-square)](scripts/system_audit.py)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

</div>

---

## 📌 Executive Summary

Historically, central sector infrastructure monitoring relies on retrospective monthly reporting after slippage has already compounded into major capital overruns. **PAIMANA AI** transforms statutory Common Unified Framework (CUF) monitoring data into a **proactive, calibrated early-warning intelligence platform**:

1. **Lead Time Acceleration**: Flags high-risk projects **11.0 months before official cost revision** using milestone trajectory and expenditure pacing ratios.
2. **Explainable AI (TreeSHAP)**: Decomposes predictions using **TreeSHAP attributions**, highlighting exact operational bottlenecks (e.g. Right-of-Way disputes, statutory clearance lag, financial burn distortion).
3. **Calibrated Conformal Bounds**: Quantile regressors generate **90% confidence bands** capturing future financial exposure rather than single-point estimates (guaranteed $\text{lower} \le \text{pred} \le \text{upper}$).
4. **Prescriptive Governance Playbooks**: Translates risk factors into concrete administrative escalations mapped directly to nodal statutory desks (e.g. State Revenue, MoEFCC, Railway Board).
5. **Grounded Administrative Copilot**: Hardened AI assistant (Google Gemini API free tier + automatic model failover & deterministic fallback) allowing natural-language inquiry without data leakage or hallucinations.
6. **Data Provenance & Sandbox**: Complete database backing from the official June 2026 MoSPI Flash Report (1,798 real projects, ₹35.38 Lakh Cr outlay) alongside a clearly isolated **Demo Telemetry Sandbox** for S-Curve and phase progression.

---

## 🎯 Direct Alignment with SIH Problem Statement Dimensions

| SIH Technical Dimension | Problem Statement Requirement | PAIMANA AI Implementation | Validated Metric |
|---|---|---|---|
| **Dimension (a)** | Combine conventional statistics with machine learning models | Baseline Ridge Regression & Logistic Regression vs. Non-linear Gradient Boosted Decision Trees (XGBoost) | **XGBoost outperforms baseline** across all metrics |
| **Dimension (b)** | Quantify the empirical performance gain of ML over conventional stats | Out-of-time chronological validation (800 historical train cohort vs. 200 out-of-time test cohort) | Classification Accuracy: **+17.5% lift** (77.5% $\rightarrow$ 95.0%); RMSE: **-27% error reduction** |
| **Dimension (c)** | Determine predictive value of CUF fields vs. auxiliary variables | Side-by-side training of `model_bundle_cuf_only.joblib` (10 In-CUF vars) vs. `model_bundle_cuf_plus_extra.joblib` (25 Multi-Factor vars) | Multi-factor layer boosts $R^2$ variance explained from **32.9% to 64.5%** (+96% lift) |

---

## 📋 Functional Requirements (FR) Status Matrix

| ID | Requirement | Status | Implementation Details |
|---|---|---|---|
| **FR1** | CUF Data Ingestion (MoSPI PDF Flash Reports, CSV & Real-time Ingestion) | **Fully Implemented** | `src/etl/pdf/engine.py`, `src/etl/csv_importer.py` (Multi-stage PyMuPDF & CSV parsing, 1,798 real projects across 17+ ministries). |
| **FR2** | Sovereign Ministry & Sector Resolution Engine | **Fully Implemented** | `src/etl/cuf/ministry_resolver.py` & `ministry_data.py` (50+ ministries, agencies, PSUs, and sector heuristics with 0 duplicate keys). |
| **FR3** | Cost Overrun Prediction (Classification + Regression + Conformal Bands) | **Fully Implemented** | `src/models/train_and_evaluate.py`, `src/models/inference.py` (95.0% Accuracy, 94.0% Conformal Coverage, 0 bound violations). |
| **FR4** | Schedule / Time Overrun Prediction (Probability + Delay Months + Lead Time) | **Fully Implemented** | `src/models/train_and_evaluate.py`, `src/models/inference.py` (Average advance warning lead time: 11.0 months). |
| **FR5** | Composite Risk Index (0–100 Delay & Escalation Index) | **Fully Implemented** | `src/risk_engine/scorer.py` + `scripts/recalibrate_scores.py` (High $\ge 58$, Medium $32-57$, Low $< 32$). |
| **FR6** | Early Warning Alert Triage (Red/Amber/Green Tiers + Prescriptive Playbooks) | **Fully Implemented** | `src/risk_engine/scorer.py`, `frontend/src/pages/AlertsPage.jsx` (Role-gated alert review, severity badges, and playbooks). |
| **FR7** | Interactive Executive Dashboard (Overview, Indian Notation ₹ L Cr, Milestone Timelines) | **Fully Implemented** | `frontend/src/pages/OverviewPage.jsx`, `ProjectDetailPage.jsx`, `ExplorerPage.jsx`. |
| **FR8** | Root-Cause Explainability (TreeSHAP Attributions per Project & Portfolio) | **Fully Implemented** | `src/models/train_and_evaluate.py`, rendered dynamically in `ProjectDetailPage.jsx`. |
| **FR9** | Statistical vs. ML Model Comparison & CUF Feature Ablation Tab | **Fully Implemented** | `frontend/src/pages/ModelComparisonPage.jsx` (Side-by-side cards + 4 dimension benchmark cards). |
| **FR10** | Grounded Administrative Assistant (Gemini API + Deterministic Fallback) | **Fully Implemented** | `src/api/rag_service.py`, `src/api/rag/gemini_client.py`, `frontend/src/components/AIAssistantDrawer.jsx`. |
| **FR11** | Multi-Dimensional Project Filtering & Search (Ministry/Sector/State/Outlay) | **Fully Implemented** | `src/api/main.py` (`/api/projects`, `/api/filters/options`), `frontend/src/pages/ExplorerPage.jsx`. |
| **FR12** | Demo Telemetry Sandbox (S-Curve & Project Phase Execution Tracker) | **Fully Implemented** | `ProjectDetailPage.jsx` (Dashed amber border, `FlaskConical` badge, transparent synthetic disclaimer). |
| **FR13** | Sovereign RBAC & MoSPI Registry Official Admin Console | **Fully Implemented** | `src/api/routers/admin.py`, `frontend/src/pages/AdminPage.jsx` (Two-role RBAC: `admin` & `employee`, personnel provisioning & status toggle). |
| **FR14** | High-Assurance Purge Protocol & Security Modal | **Fully Implemented** | `PurgeConfirmModal.jsx` (6-char dynamic captcha challenge), `StatusModal.jsx` (Portal-mounted sovereign alerts). |
| **FR15** | Comprehensive Test Suite & TestSprite Automated Harness | **Fully Implemented** | 48/48 Pytest tests passing (`tests/`) + 14/14 TestSprite E2E automated test cases passing (`testsprite_tests/`). |

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Data & ETL Layer
        PDF[MoSPI Flash Report PDF] --> IngestPDF[PyMuPDF Stateful Table 6 Engine]
        CSV[CUF CSV Ingestion] --> IngestCSV[Universal CSV Importer]
        IngestPDF & IngestCSV --> Resolver[Sovereign Ministry & Sector Resolver\n50+ Ministries, PSUs & Domain Precedence]
        Resolver --> DB[(SQLite: paimana.db\n1,798 Real Projects + WAL Mode)]
        DB --> FE[Feature Store\n10 In-CUF vs 25 Multi-Factor Matrices]
    end

    subgraph AI/ML Engine
        FE --> Split[Temporal Out-of-Time Split\n800 Train vs 200 Test Cohort]
        Split --> Baseline[Linear / Logistic / Ridge Baseline]
        Split --> XGB[XGBoost 3.4 Ensemble + Quantile Regressors]
        XGB --> SHAP[TreeExplainer SHAP Engine]
        XGB --> Conf[90% Conformal Prediction Intervals\nLower <= Pred <= Upper]
    end

    subgraph Risk & Prescriptive Engine
        XGB & Conf & SHAP --> Scorer[Hybrid Composite Risk Engine\n0-100 Delay Index]
        Scorer --> Playbooks[Prescriptive Action Mapper\nStatutory Authority Routing]
        Scorer --> Alerts[Early Warning Triage Pipeline\nRole-Gated Review Desks]
    end

    subgraph Secure Platform & Governance
        DB --> RBAC[Two-Role RBAC & User Store\nAdmin: Registry Official | Employee: Monitoring Officer]
        RBAC --> AdminConsole[Admin Management Console\nPersonnel Roster & Provisioning]
        DB --> Purge[High-Assurance Purge Protocol\n6-Character Captcha Safeguard]
    end

    subgraph Decision Support UI
        DB & Scorer & Alerts & RBAC --> API[FastAPI Secure REST API\nRate Limited, Cached Indexes, Security Headers]
        API --> RAG[Grounded Assistant RAG Engine\nGoogle Gemini API + Deterministic Fallback]
        API --> UI[React 18 Dashboard\nIn-Flight Request Deduplication, Portal Modals]
    end
```

---

## 🚀 Quick Start Guide (From Fresh Clone)

### Prerequisites
- Python 3.10+ (Python 3.11 / 3.12 / 3.14 supported)
- Node.js 18+ and npm
- *(Optional)* Free Google Gemini API Key from Google AI Studio (`GEMINI_API_KEY`) for conversational queries (system automatically defaults to Grounded Deterministic Fallback if unconfigured or offline).

---

### Method 1: Single-Command Launch (Recommended)

```bat
# Windows (Double-click or run in terminal):
start.bat

# PowerShell:
.\start.ps1

# Linux / macOS:
chmod +x start.sh && ./start.sh
```

---

### Method 2: Manual Step-by-Step Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..

# 2. Ingest real MoSPI Flash Report PDF → paimana.db (1,798 projects)
python scripts/ingest_flash_report.py

# 3. Normalize ministry names using sovereign resolver
python scripts/fix_ministry_names.py

# 4. Train models & compute conformal prediction bands
python src/models/train_and_evaluate.py

# 5. Recalibrate risk scores & verify conformal bounds
python scripts/recalibrate_scores.py

# 6. Run automated test suites (Pytest + Audit)
python -m pytest tests/ -v
python scripts/system_audit.py

# 7. Start backend & frontend
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
cd frontend && npm run dev
```

---

## 🌐 Application Endpoints & Portals

| Interface | URL | Purpose | Statutory Clearance |
|---|---|---|---|
| **Executive Portfolio Overview** | `http://localhost:5173` | Aggregate KPIs, sector outlays in ₹ Lakh Cr, ministry risk distribution | Public / Employee |
| **Central Sector Project Explorer** | `http://localhost:5173/explorer` | Multi-filter grid across central sector projects | Public / Employee |
| **Early Warning & Alert Hub** | `http://localhost:5173/alerts` | Triage of early warning alerts with prescriptive playbooks | Public (View) / Admin (Review) |
| **Model Comparison & SIH Ablation** | `http://localhost:5173/models` | Statistical vs ML benchmarking + CUF vs Multi-factor ablation | Public / Employee |
| **MoSPI Registry Admin Console** | `http://localhost:5173/admin` | Officer provisioning, personnel roster inspection, status toggle | `admin` (Registry Official) |
| **Officer Portal Login** | `http://localhost:5173/login` | Statutory officer authentication & 1-click credential demo | All Officers |
| **REST API Documentation** | `http://localhost:8000/docs` | Interactive Swagger API specification | Open |
| **System Health Check** | `http://localhost:8000/api/health` | Live database connectivity & model bundle verification | Open |

---

## 🔒 Security, Integrity & Data Governance Policy

- **Two-Role Statutory RBAC**: Strict separation between MoSPI Registry Officials (`admin`) and Monitoring Officers (`employee`), enforcing role checks on mutating routes (`/api/admin/*`, `/api/alerts/{id}/review`).
- **High-Assurance Purge Safeguard**: Bulk dataset purge requires solving a dynamic 6-character captcha challenge inside a Portal-mounted modal with touch and keyboard safeguards.
- **In-Flight Request Deduplication**: Frontend HTTP client caches concurrent inflight requests (`dedupeGet`), preventing redundant server loads during dashboard re-renders.
- **Zero Data Leakage**: All ML inference, feature engineering, and database transactions execute locally on the host machine.
- **Strict Data Provenance**: Real MoSPI database figures are clearly separated from illustrative demo curves (S-Curve & Phase Tracker) with explicit warning badges and disclaimers.
- **Hardened Copilot**: Prompt injection delimiters (`<|system|>`, `<|user|>`), input sanitization, and database schema abstraction protect the assistant interface.
- **Automated Verification**: **48/48 Pytest unit/integration tests** and **14/14 TestSprite E2E test cases** validate end-to-end reliability.
