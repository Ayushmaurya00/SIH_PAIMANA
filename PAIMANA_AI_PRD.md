# Product Requirements Document
## AI-Powered Predictive Analytics & Early Warning System for Infrastructure Project Monitoring (PAIMANA)

**Theme:** AI for Infrastructure Monitoring
**Context:** Smart India Hackathon — Ministry of Statistics and Programme Implementation (MoSPI) / IPMD

---

## 1. Problem Statement Summary

MoSPI's IPMD monitors ~1,981 Central Sector Infrastructure Projects (≥₹150 crore) across 17 Ministries and 22 sectors through the PAIMANA portal. Despite rich historical data (from OCMS since 2006, now PAIMANA), monitoring remains largely *descriptive*. The goal is to move to *predictive and prescriptive* monitoring — flagging cost overruns, time overruns, and implementation risk **before** they materialize.

## 2. Objectives

1. Predict cost overruns and time overruns for ongoing infrastructure projects.
2. Generate a project-level risk score and early-warning alerts.
3. Compare classical statistical methods vs AI/ML methods on prediction accuracy — quantify the actual gain from ML.
4. Determine how much predictive power comes from existing Common Upload Form (CUF) fields vs additional variables not currently captured.
5. Deliver actionable, explainable outputs for policymakers and project administrators — not just a black-box number.

## 3. Target Users

| User | Need |
|---|---|
| Policymakers (MoSPI/IPMD) | Portfolio-level risk visibility, prioritization for intervention |
| Project/Ministry administrators | Early warning on their own projects, driver-level explanations |
| Monitoring agency analysts | Drill-down analytics, benchmarking across sectors/agencies |

## 4. Scope

### In scope (hackathon MVP)
- Data ingestion & cleaning pipeline for CUF-style project data
- Baseline statistical models (regression/ARIMA-class) for overrun trends
- ML models (gradient-boosted trees) for cost & time overrun prediction
- Explainability module (feature/driver importance)
- Composite project risk scoring framework
- Early warning alert logic (threshold- or model-based)
- Interactive dashboard (filter by sector/ministry/agency, drill into a project)
- Statistical-vs-ML comparison report (accuracy, lead time, interpretability)
- CUF-only vs CUF+extra-variables ablation analysis

### Stretch goals
- LLM-based natural-language project intelligence assistant (RAG over project data)
- Benchmarking/comparative analytics module across sectors
- Deployable API layer (FastAPI) behind the dashboard

### Out of scope
- Direct integration with live PAIMANA/OCMS production systems
- Any closed-source/paid tooling (brief requires open-source only)

## 5. Data & Schema (based on CUF fields referenced in the PS)

Core fields expected per project record:
- Project ID, Name, Ministry/Department, Sector, Implementing Agency
- Approved cost, Revised cost, Cumulative expenditure
- Approval date, Scheduled completion date, Revised completion date, Actual/current status
- Physical progress %, Milestones (planned vs achieved, with dates)
- Geography/state, Project category/type
- Reasons for delay/cost revision (if captured as free text — candidate for LLM/NLP feature extraction)

**Deliverable of dimension (c):** a documented feature-importance comparison between a model trained only on CUF fields vs one enriched with derived/external variables (e.g., inflation indices, monsoon/seasonal delay patterns, agency track record computed from historical data, sector-level benchmarks).

## 6. Functional Requirements

| ID | Requirement |
|---|---|
| FR1 | System ingests structured project data (CSV/DB) and validates/cleans it |
| FR2 | System computes baseline statistical forecasts (regression/time-series) for cost & time overrun |
| FR3 | System trains ML model(s) for cost overrun prediction with accuracy/error metrics reported |
| FR4 | System trains ML model(s) for time/schedule overrun prediction |
| FR5 | System outputs a 0–100 (or High/Med/Low) risk score per project, combining cost & time risk |
| FR6 | System flags "early warning" projects before overrun is realized, with lead-time metric |
| FR7 | System explains top drivers per prediction (SHAP or equivalent) at project and portfolio level |
| FR8 | Dashboard shows portfolio view (by sector/ministry) and project-level drill-down |
| FR9 | System documents statistical-vs-ML comparison with quantified metrics |
| FR10 (stretch) | Natural-language assistant answers questions like "which Transport projects are highest risk this quarter" |

## 7. Non-Functional Requirements

- **Open-source only** — every library/tool must be free/OSS (explicit brief requirement)
- Reasonable inference latency for dashboard interactivity (<2s per query)
- Reproducible pipeline (versioned data → features → model → dashboard)
- Explainability over raw accuracy where the two trade off — judges/policymakers need to trust and act on outputs
- Clear documentation of assumptions (especially if using a proxy dataset instead of live PAIMANA data)

## 8. Success Metrics / Evaluation

- **Cost overrun model:** MAE/RMSE on held-out projects, vs statistical baseline
- **Time overrun model:** MAE (in months) on held-out projects, vs statistical baseline
- **Early warning lead time:** average months of advance notice before an overrun is officially recorded
- **Ablation result:** performance delta between CUF-only and CUF+extra-variable models
- **Explainability quality:** does the driver analysis match known domain intuition (e.g., land acquisition delays, monsoon impact)?

## 9. Proposed Tech Stack (all open-source)

| Layer | Tools |
|---|---|
| Data wrangling | pandas, numpy |
| Baseline stats models | statsmodels, scikit-learn (linear/logistic regression, ARIMA) |
| ML models | XGBoost / LightGBM |
| Explainability | SHAP |
| Dashboard | Streamlit + Plotly (fastest path) or Dash |
| API layer (optional) | FastAPI |
| Storage | SQLite or PostgreSQL |
| LLM assistant (stretch) | Google Gemini API (free tier) / Grounded RAG with deterministic fallback |
| Dev tooling | Git, Claude Code / Cursor for AI-assisted ("vibe") coding |

## 10. Suggested Hackathon Timeline

| Phase | Time | Focus |
|---|---|---|
| 1 | Hours 0–4 | Data sourcing, cleaning, EDA |
| 2 | Hours 4–10 | Baseline statistical models + first ML models |
| 3 | Hours 10–16 | Risk scoring, early warning logic, SHAP driver analysis |
| 4 | Hours 16–24 | Dashboard build (Streamlit) |
| 5 | Hours 24–30 | Stat-vs-ML comparison writeup, CUF ablation analysis |
| 6 | Hours 30–36 | LLM assistant (if time permits) |
| 7 | Final hours | Documentation, deck, deployment polish |

## 11. Deliverables for Submission

1. Working dashboard (deployed or local demo)
2. Trained models + evaluation report (stat baseline vs ML, with numbers)
3. CUF-only vs CUF+extra-variable ablation writeup
4. Source code repo with README (setup + architecture)
5. Presentation deck summarizing approach, results, and impact
