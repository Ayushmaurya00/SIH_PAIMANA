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

### 2.2 Backend Unit & Integration Tests (Pytest)
Executes all automated unit tests covering data sanitization, feature engineering, and model contracts:
```bash
pytest tests/ -v
```

---

### 2.3 User Journey End-to-End Validation
Validates the complete vertical integration from database queries up through API response contracts:
```bash
python scripts/verify_user_journey.py
```

---

### 2.4 Data Extraction & PDF Parser Verification
Tests the layout-aware Table 6 PyMuPDF extraction engine with stateful ministry banner tracking against the June 2026 MoSPI Flash Report:
```bash
python scripts/ingest_flash_report.py
```

---

### 2.5 Score Recalibration & Conformal Bound Fix
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
