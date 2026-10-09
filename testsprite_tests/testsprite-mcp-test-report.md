# TestSprite AI Testing Report (MCP)

---

## 1️⃣ Document Metadata
- **Project Name:** PAIMANA AI (Web-based-PM)
- **Target URL:** `http://localhost:5173/`
- **Execution Date:** 2026-09-25
- **Prepared by:** TestSprite AI QA Pipeline & Antigravity IDE
- **Execution Mode:** Local Cloud Tunnel (`serverMode: development`)

---

## 2️⃣ Requirement Validation Summary

### Requirement 1: Overview Dashboard
*Provides high-level KPIs, portfolio risk distribution, sector breakdown, and early warning summaries.*

#### Test TC001: View dashboard risk summary and open a risky project
- **Test Code:** [`TC001_View_dashboard_risk_summary_and_open_a_risky_project.py`](./TC001_View_dashboard_risk_summary_and_open_a_risky_project.py)
- **Result:** [TestSprite Dashboard Run](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/4b719760-b2c9-4425-bf65-8cb2ae277163)
- **Status:** ✅ Passed
- **Analysis / Findings:** Overview dashboard accurately loads decision metrics, sovereign KPI totals, early-warning distribution, and allows drilling directly into highlighted projects.

#### Test TC005: Review dashboard sector breakdown
- **Test Code:** [`TC005_Review_dashboard_sector_breakdown.py`](./TC005_Review_dashboard_sector_breakdown.py)
- **Result:** [TestSprite Dashboard Run](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/ba562b87-a9ab-4aa7-8f1c-29da58a5fdae)
- **Status:** ✅ Passed
- **Analysis / Findings:** Sector distribution cards and budget outlay breakdowns render with complete sovereign sector classifications.

---

### Requirement 2: Project Detail & Deep Dive
*Delivers calibrated forecasting ranges, timeline gantt charts, and predictive telemetry.*

#### Test TC002: Inspect project predictions and explainability
- **Test Code:** [`TC002_Inspect_project_predictions_and_explainability.py`](./TC002_Inspect_project_predictions_and_explainability.py)
- **Status:** ⚠️ Blocked (Test Harness Target ID)
- **Analysis / Findings:** Test script navigated to synthetic hardcoded URL `/projects/1`. In PAIMANA, sovereign project IDs follow canonical schemes (e.g. `PRJ-00001`, `PRJ-705728`). The application correctly responded with a graceful 404 Empty State.

#### Test TC004: Review project progress and milestone context
- **Test Code:** [`TC004_Review_project_progress_and_milestone_context.py`](./TC004_Review_project_progress_and_milestone_context.py)
- **Status:** ⚠️ Blocked (Test Harness Target ID)
- **Analysis / Findings:** Test script requested non-canonical ID `/projects/1`. Application correctly handled missing project gracefully.

#### Test TC013: Handle a project detail page for a nonexistent project
- **Test Code:** [`TC013_Handle_a_project_detail_page_for_a_nonexistent_project.py`](./TC013_Handle_a_project_detail_page_for_a_nonexistent_project.py)
- **Result:** [TestSprite Dashboard Run](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/90b5918c-80df-49df-b833-3a86befe374d)
- **Status:** ✅ Passed
- **Analysis / Findings:** Graceful error boundary verified: invalid project IDs correctly trigger the "Project Not Found" EmptyState with a "Back to Project Directory" recovery action.

---

### Requirement 3: Early Warning Alerts
*Surfaces real-time threshold escalations, severity levels, and acknowledgment workflows.*

#### Test TC003: Acknowledge an active alert
- **Test Code:** [`TC003_Acknowledge_an_active_alert.py`](./TC003_Acknowledge_an_active_alert.py)
- **Status:** ⚠️ Blocked (Prerequisite Data Seed)
- **Analysis / Findings:** No active alerts matched the initial default filter state during the run, showing the "No Active Escalation Alerts" empty view.

#### Test TC009: Review alert ordering and categories
- **Test Code:** [`TC009_Review_alert_ordering_and_categories.py`](./TC009_Review_alert_ordering_and_categories.py)
- **Status:** ❌ Failed (Zero Alerts in Current View)
- **Analysis / Findings:** Filters for Critical/Watchlist and Status were verified present, but absence of unacknowledged alerts prevented verifying category order.

#### Test TC012: Show an empty alert state
- **Test Code:** [`TC012_Show_an_empty_alert_state.py`](./TC012_Show_an_empty_alert_state.py)
- **Status:** ⚠️ Blocked (Auth Seed)
- **Analysis / Findings:** Test script attempted authentication with unseeded credentials (`Account not found`).

---

### Requirement 4: Project Explorer & Directory
*Provides multi-dimensional search, sovereign ministry/sector filtering, sorting, and pagination.*

#### Test TC006: Search and filter projects in the explorer
- **Test Code:** [`TC006_Search_and_filter_projects_in_the_explorer.py`](./TC006_Search_and_filter_projects_in_the_explorer.py)
- **Status:** ❌ Failed (State Filter Control Missing)
- **Analysis / Findings:** Filter toolbar contains Search, Ministry, Sector, and Risk Level dropdowns. The test specifically sought a separate standalone `<select>` dropdown for "State", whereas State is currently displayed in the directory table column.

#### Test TC008: Open project details from the explorer
- **Test Code:** [`TC008_Open_project_details_from_the_explorer.py`](./TC008_Open_project_details_from_the_explorer.py)
- **Result:** [TestSprite Dashboard Run](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/9ccfa920-02a5-4fb2-aa70-0071bf967ad8)
- **Status:** ✅ Passed
- **Analysis / Findings:** Clicking a project row in the directory smoothly navigates to the detailed telemetry view.

#### Test TC010: Sort and paginate explorer results
- **Test Code:** [`TC010_Sort_and_paginate_explorer_results.py`](./TC010_Sort_and_paginate_explorer_results.py)
- **Result:** [TestSprite Dashboard Run](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/47160e3d-6b62-4af2-b4ef-8c04805c245a)
- **Status:** ✅ Passed
- **Analysis / Findings:** Pagination controls, page size shifts, and risk/cost sorting function properly with instantaneous updates.

---

### Requirement 5: Model Comparison & Benchmark Analytics
*Evaluates early warning models, XGBoost/RandomForest predictive metrics, and ablation studies.*

#### Test TC007: Compare model metrics and ablation results
- **Test Code:** [`TC007_Compare_model_metrics_and_ablation_results.py`](./TC007_Compare_model_metrics_and_ablation_results.py)
- **Result:** [TestSprite Dashboard Run](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/2ad200b4-5de0-4329-bdcf-72525f66fc63)
- **Status:** ✅ Passed
- **Analysis / Findings:** Model benchmark comparisons (AUC-ROC, F1, RMSE) and CUF ablation delta displays render reliably.

#### Test TC011: Identify the strongest forecasting model
- **Test Code:** [`TC011_Identify_the_strongest_forecasting_model.py`](./TC011_Identify_the_strongest_forecasting_model.py)
- **Result:** [TestSprite Dashboard Run](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/5e67376e-944b-4ca0-bd97-1b2ebdefaa8b)
- **Status:** ✅ Passed
- **Analysis / Findings:** Primary model indicators accurately highlight the sovereign benchmark winner (XGBoost + CUF).

#### Test TC014: Handle unsupported model ablation filters
- **Test Code:** [`TC014_Handle_unsupported_model_ablation_filters.py`](./TC014_Handle_unsupported_model_ablation_filters.py)
- **Result:** [TestSprite Dashboard Run](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/9fc0a42d-67c6-4b7c-aff6-06b338e3f6a0)
- **Status:** ✅ Passed
- **Analysis / Findings:** Resilient client handling verified for model feature toggles.

---

## 3️⃣ Coverage & Matching Metrics

- **Total Test Cases Executed:** 14
- **Passed:** 8 (57.14%)
- **Blocked / Failed:** 6 (42.86%)

| Requirement Module | Total Tests | ✅ Passed | ❌ Failed / ⚠️ Blocked | Pass Rate |
| :--- | :---: | :---: | :---: | :---: |
| **1. Overview Dashboard** | 2 | 2 | 0 | **100%** |
| **2. Project Detail & Deep Dive** | 3 | 1 | 2 (Blocked on test ID `/1`) | **33.3%** |
| **3. Early Warning Alerts** | 3 | 0 | 3 (Blocked on empty alert seed) | **0%** |
| **4. Project Explorer & Directory** | 3 | 2 | 1 (Missing State `<select>`) | **66.7%** |
| **5. Model Comparison & Analytics** | 3 | 3 | 0 | **100%** |
| **Overall** | **14** | **8** | **6** | **57.14%** |

---

## 4️⃣ Key Gaps / Risks

1. **Test Harness vs. Canonical Project IDs (TC002, TC004)**:
   - *Gap*: Automated Playwright scripts attempted to navigate to `http://localhost:5173/projects/1`. In production, sovereign projects use UUID/CUF codes like `PRJ-00001` or `MOSPI-00306`.
   - *Risk*: Low / False Positive. The app correctly serves a 404 EmptyState when an invalid ID is requested. Updating test step targets to query dynamic project IDs from the Explorer resolves this.

2. **Missing Standalone State Filter Dropdown (TC006)**:
   - *Gap*: In [`ExplorerFilters.jsx`](file:///c:/Users/ayush/OneDrive/Desktop/Web-based-PM/frontend/src/components/explorer/ExplorerFilters.jsx), filters exist for `Search`, `Ministry`, `Sector`, and `Risk Level`. The backend `/api/filters/options` already returns `states: [...]`, but there is no dedicated `State` dropdown in the UI.
   - *Remediation*: Adding an "All States" `<select>` in `ExplorerFilters.jsx` will satisfy TC006.

3. **Escalation Alerts Seed Data (TC003, TC009)**:
   - *Gap*: The test database currently had 0 unreviewed high-severity alerts, displaying the "No Active Alerts" empty state and preventing acknowledgment flow tests.
   - *Remediation*: Ensure synthetic seed alerts are initialized during test harness bootstrap.
