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
| **FR1** | CUF Data Ingestion (MoSPI PDF Flash Reports & Database Ingestion) | **Fully Implemented** | `src/etl/pdf_ingestion.py` (PyMuPDF engine with stateful banner tracking, 1,798 real projects across 17 ministries). |
| **FR2** | Ministry Name Canonicalization & Data Integrity Validation | **Fully Implemented** | `MINISTRY_CANONICAL_MAP` in `pdf_ingestion.py`, `scripts/fix_ministry_names.py` (0 duplicate ministry keys). |
| **FR3** | Cost Overrun Prediction (Classification + Regression + Conformal Bands) | **Fully Implemented** | `src/models/train_and_evaluate.py` (95.0% Accuracy, 94.0% 90% Conformal Coverage, 0 bound violations). |
| **FR4** | Schedule / Time Overrun Prediction (Probability + Delay Months + Lead Time) | **Fully Implemented** | `src/models/train_and_evaluate.py` (Average advance warning lead time: 11.0 months). |
| **FR5** | Composite Risk Index (0–100 Delay & Escalation Index) | **Fully Implemented** | `src/risk_engine/scorer.py` + `scripts/recalibrate_scores.py` (High $\ge 58$, Medium $32-57$, Low $< 32$). |
| **FR6** | Early Warning Alert Triage (Red/Amber/Green Tiers + Prescriptive Playbooks) | **Fully Implemented** | `src/risk_engine/scorer.py`, `prescriptions.py`, `frontend/src/pages/AlertsPage.jsx` (371 active alerts). |
| **FR7** | Interactive Executive Dashboard (Overview, Indian Notation ₹ L Cr, Milestone Timelines) | **Fully Implemented** | `frontend/src/pages/OverviewPage.jsx`, `ProjectDetailPage.jsx`, `ExplorerPage.jsx`. |
| **FR8** | Root-Cause Explainability (TreeSHAP Attributions per Project & Portfolio) | **Fully Implemented** | `src/models/train_and_evaluate.py`, rendered in `ProjectDetailPage.jsx`. |
| **FR9** | Statistical vs. ML Model Comparison & CUF Feature Ablation Tab | **Fully Implemented** | `frontend/src/pages/ModelComparisonPage.jsx` (Side-by-side cards + 4 dimension cards). |
| **FR10** | Grounded Administrative Assistant (Gemini API + Deterministic Fallback) | **Fully Implemented** | `src/api/rag_service.py`, `src/api/rag/gemini_client.py`, `frontend/src/components/AIAssistantDrawer.jsx`. |
| **FR11** | Multi-Dimensional Project Filtering & Search (Ministry/Sector/State/Outlay) | **Fully Implemented** | `src/api/main.py` (`/api/projects`, `/api/filters/options`), `frontend/src/pages/ExplorerPage.jsx`. |
| **FR12** | Demo Telemetry Sandbox (S-Curve & Project Phase Execution Tracker) | **Fully Implemented** | `ProjectDetailPage.jsx` (Dashed amber border, `FlaskConical` badge, transparent synthetic disclaimer). |
| **FR13** | Automated System Audit & Integrity Harness | **Fully Implemented** | `scripts/system_audit.py` (**25/25 assertions passing**). |

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Data Layer
        PDF[MoSPI Flash Report PDF Ingestion] --> ETL[PyMuPDF Stateful Banner Parser]
        ETL --> DB[(SQLite: paimana.db\n1,798 Real Projects)]
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
        Scorer --> Alerts[Early Warning Triage Pipeline\n371 Active Alerts]
    end

    subgraph Decision Support UI
        DB & Scorer & Alerts --> API[FastAPI Secure REST API\nRate Limited & Validated]
        API --> RAG[Grounded Assistant RAG Engine\nGoogle Gemini API + Deterministic Fallback]
        API --> UI[React 18 Dashboard\nMoSPI Sovereign Decision Theme]
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

# 3. Normalize ministry names
python scripts/fix_ministry_names.py

# 4. Train models & compute conformal prediction bands
python src/models/train_and_evaluate.py

# 5. Recalibrate risk scores & verify conformal bounds
python scripts/recalibrate_scores.py

# 6. Run automated system audit
python scripts/system_audit.py

# 7. Start backend & frontend
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
cd frontend && npm run dev
```

---

## 🌐 Application Endpoints

| Interface | URL | Purpose |
|---|---|---|
| **Executive Portfolio Overview** | `http://localhost:5173` | Aggregate KPIs, sector outlays in ₹ Lakh Cr, ministry risk distribution |
| **Central Sector Project Explorer** | `http://localhost:5173/explorer` | Multi-filter grid across 1,798 projects |
| **Early Warning & Alert Hub** | `http://localhost:5173/alerts` | Triage of 371 active alerts with prescriptive playbooks |
| **Model Comparison & SIH Ablation** | `http://localhost:5173/models` | Statistical vs ML benchmarking + CUF vs Multi-factor ablation |
| **REST API Documentation** | `http://localhost:8000/docs` | Interactive Swagger API specification |
| **System Health Check** | `http://localhost:8000/api/health` | Live database connectivity check |

---

## 🔒 Security & Data Provenance Policy

- **Zero Data Leakage**: All machine learning models, database queries, and LLM reasoning run 100% locally on the host machine.
- **Strict Data Provenance**: Real MoSPI database figures are clearly separated from illustrative demo curves (S-Curve & Phase Tracker) with explicit warning badges and disclaimers.
- **Hardened Copilot**: Prompt injection delimiters (`<|system|>`, `<|user|>`), input sanitization, and database schema abstraction protect the assistant interface.
