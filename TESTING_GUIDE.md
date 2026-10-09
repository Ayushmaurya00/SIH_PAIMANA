# PAIMANA AI Testing & Quality Assertion Harness
## Comprehensive Testing, System Audit & Quality Assurance Guide
*Last Updated: September 2026 | Status: Production-Ready (25/25 Audit Invariants Passing)*

---

## 1. Overview

This document specifies the test suites, automated integrity runners, and system audit harnesses ensuring reliability across data ingestion, ML models, conformal prediction bounds, risk scoring, and the REST API.

---

## 2. Automated Test Runners & Verification Commands

### 2.1 Full-System Audit Harness (Primary Production Verification)
Validates **25 system-wide invariants** covering database counts, canonical ministry keys, outlay totals, zero null ML predictions, conformal bounds ($\text{lower} \le \text{pred} \le \text{upper}$), calibrated risk distributions, and schema completeness:
```bash
python scripts/system_audit.py
```
*Expected Output:* `SUMMARY: 25/25 PASS | 0 WARN | 0 FAIL`

---

### 2.2 Backend Unit & Integration Tests (Pytest — 48/48 Passing)
Executes all automated unit and integration tests covering data sanitization, ETL ministry resolution, feature engineering, RBAC administration, risk scoring, and API contracts:
```bash
python -m pytest tests/ -v
```
*Test Matrix (48 Tests across 8 Modules):*
* **`tests/test_ministry_resolver.py` (12 tests):** Heuristic resolution, acronym mapping (NHAI, RVNL, IOCL), alias normalization, domain precedence (Solar $\rightarrow$ MNRE, Broadband $\rightarrow$ Communications), and word-boundary safety (`empowerment` $\ne$ `power`).
* **`tests/test_rbac_admin.py` (4 tests):** MoSPI Registry Official login, personnel roster RBAC gating, user provisioning, status toggling, and unauthorized mutation denial.
* **`tests/test_api_endpoints.py` (14 tests):** Health check, structured 404/422 error handlers, dashboard KPIs, paginated project grid, project details, alerts, model metrics, grounded RAG copilot, and CSV export.
* **`tests/test_csv_importer.py` (3 tests):** Universal CSV header mapping, numerical casting, and end-to-end dataset ingestion.
* **`tests/test_cuf_adapter.py` (4 tests):** CUF schema validation, idempotency, and data sanitization.
* **`tests/test_data_integrity.py` (4 tests):** Foreign key constraints, status consistency, and positive outlay invariants.
* **`tests/test_feature_engineering.py` (3 tests):** Temporal matrix shapes, expenditure pacing ratios, and classification/regression alignment.
* **`tests/test_risk_engine.py` (4 tests):** Deterministic reproducibility, score bounding $[0.0, 100.0]$, prescriptive action generation, and alert severity thresholds.

---

### 2.3 TestSprite MCP Automated E2E Regression Suite (14/14 Passing)
Automated end-to-end integration tests validating browser and API contracts against simulated officer workflows:
```bash
# Generated report and test traces:
testsprite_tests/testsprite-mcp-test-report.md
```
*Validated Test Cases:*
* `TC001`: View dashboard risk summary and drill down into a critical infrastructure project.
* `TC002`: Inspect project ML predictions, conformal confidence bands, and TreeSHAP explainability attributions.
* `TC003`: Acknowledge an active early-warning alert under administrative clearance.
* `TC004`: Review project progress, financial pacing, and milestone timeline context.
* `TC005`: Review dashboard sector breakdown and expenditure allocations.
* `TC006`: Search and multi-filter projects across sectors, ministries, and risk tiers in the explorer.
* `TC007`: Compare statistical baseline vs. ML model metrics and feature ablation results.
* `TC008`: Open project detail dossiers directly from the central explorer directory.
* `TC009`: Review alert severity ordering, timestamps, and statutory categories.
* `TC010`: Sort and paginate explorer grid results with seamless page size controls.
* `TC011`: Benchmark and identify the strongest forecasting model across accuracy, AUC, and RMSE.
* `TC012`: Verify graceful rendering of empty alert states under strict filter constraints.
* `TC013`: Verify structured 404 handling and navigation fallback for nonexistent project IDs.
* `TC014`: Handle unsupported model ablation filters with defensive schema defaults.

---

### 2.4 User Journey End-to-End Validation
Validates the complete vertical integration from database queries up through API response contracts:
```bash
python scripts/verify_user_journey.py
```

---

### 2.5 Data Extraction & PDF Parser Verification
Tests the layout-aware Table 6 PyMuPDF extraction engine with stateful ministry banner tracking against the June 2026 MoSPI Flash Report:
```bash
python scripts/ingest_flash_report.py
```

---

### 2.6 Score Recalibration & Conformal Bound Verification
Applies updated risk thresholds (High $\ge 58$, Med $\ge 32$) and guarantees mathematical bounds for confidence intervals:
```bash
python scripts/recalibrate_scores.py
```

---

## 3. System Audit Invariant Matrix (25 Checks)

| Category | Invariant Check | Pass Criterion | Verified Status |
|---|---|---|---|
| **ETL Integrity** | Project Count | $1700 \le N \le 1900$ | **1,798 Projects** (PASS) |
| **ETL Integrity** | Canonical Ministries | $\ge 15$ unique | **17 Ministries** (PASS) |
| **ETL Integrity** | MoRTH Name De-duplication | 0 variant rows | **0 `& Highways`, 966 Canonical** (PASS) |
| **ETL Integrity** | Sanctioned Outlay | $₹[34.5, 36.5]\text{ Lakh Cr}$ | **₹35.38 Lakh Cr** (PASS) |
| **ETL Integrity** | Cumulative Expenditure | $₹[20.0, 24.0]\text{ Lakh Cr}$ | **₹21.93 Lakh Cr** (PASS) |
| **ETL Integrity** | No NULL Ministry | Exactly 0 | **0 NULLs** (PASS) |
| **ETL Integrity** | No NULL/Zero Outlay | Exactly 0 | **0 NULLs** (PASS) |
| **ML Inference** | Model Predictions Table Populated | $> 0$ rows | **3,596 rows** (PASS) |
| **ML Inference** | No NULL Cost Overrun Prob | Exactly 0 | **0 NULLs** (PASS) |
| **ML Inference** | No NULL Time Overrun Prob | Exactly 0 | **0 NULLs** (PASS) |
| **ML Conformal** | Cost Conformal Validity | $\text{lower} \le \text{pred} \le \text{upper}$ | **0 Violations** (PASS) |
| **ML Conformal** | Time Conformal Validity | $\text{lower} \le \text{pred} \le \text{upper}$ | **0 Violations** (PASS) |
| **Risk Engine** | 100% Risk Score Coverage | Scores = Projects | **1,798 / 1,798** (PASS) |
| **Risk Engine** | High Risk Proportion | $\ge 15.0\%$ | **42.3% (761)** (PASS) |
| **Risk Engine** | Low Risk Proportion | $< 70.0\%$ | **30.0% (539)** (PASS) |
| **Risk Engine** | No NULL Risk Scores | Exactly 0 | **0 NULLs** (PASS) |
| **Alert Engine** | Alerts Table Populated | $> 0$ alerts | **371 Active Alerts** (PASS) |
| **Alert Engine** | Prescriptive Action Quality | 0 generic boilerplate | **0 generic rows** (PASS) |
| **Schema Integrity**| Table `projects` Exists | Present | **PASS** |
| **Schema Integrity**| Table `monthly_snapshots` Exists | Present | **PASS** |
| **Schema Integrity**| Table `milestones` Exists | Present | **PASS** |
| **Schema Integrity**| Table `risk_scores` Exists | Present | **PASS** |
| **Schema Integrity**| Table `model_predictions` Exists | Present | **PASS** |
| **Schema Integrity**| Table `model_metrics` Exists | Present | **PASS** |
| **Schema Integrity**| Table `alerts` Exists | Present | **PASS** |

---

## 4. Frontend & Visual Quality Assertions

1. **Indian Financial Numbering**: Verify on Overview and Project Detail pages that sums $\ge ₹1\text{ Lakh Cr}$ format as `₹X.XX Lakh Cr` and chart axes render `₹X.X L Cr`.
2. **Demo Telemetry Sandbox Transparency**: Confirm that the S-Curve and Phase Tracker sections display with a dashed amber border, `FlaskConical` icon, and explicit synthetic data badges.
3. **Print Dossier Layout**: Open any Project Detail page and invoke `window.print()` / Ctrl+P to verify that interactive navigation elements are suppressed and the official MoSPI Executive Cabinet Briefing header is rendered cleanly.
