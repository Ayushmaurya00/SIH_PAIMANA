# TestSprite AI Testing Report (MCP)

---

## 1️⃣ Document Metadata
- **Project Name:** Web-based-PM (PAIMANA AI)
- **Date:** 2026-09-01
- **Testing Scope:** Fullstack Frontend & Local API Integration
- **Prepared by:** TestSprite AI Testing Suite

---

## 2️⃣ Requirement Validation Summary

### Feature: Overview Dashboard & KPI Summary
#### Test TC001: View dashboard risk summary and open a risky project
- **Test Code:** [`TC001_View_dashboard_risk_summary_and_open_a_risky_project.py`](./TC001_View_dashboard_risk_summary_and_open_a_risky_project.py)
- **Visualization:** [Test Result Dashboard](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/4b719760-b2c9-4425-bf65-8cb2ae277163)
- **Status:** ✅ Passed
- **Analysis:** Overview KPI cards (Total Projects, Capital Outlay, Overrun Projects, Average Risk Score) correctly computed and rendered with interactive risk distribution charts.

#### Test TC005: Review dashboard sector breakdown
- **Test Code:** [`TC005_Review_dashboard_sector_breakdown.py`](./TC005_Review_dashboard_sector_breakdown.py)
- **Visualization:** [Test Result Dashboard](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/ba562b87-a9ab-4aa7-8f1c-29da58a5fdae)
- **Status:** ✅ Passed
- **Analysis:** Sector risk heatmap and allocation breakdowns rendered accurately based on SQLite portfolio aggregate queries.

---

### Feature: Project Explorer & Pagination
#### Test TC006: Search and filter projects in the explorer
- **Test Code:** [`TC006_Search_and_filter_projects_in_the_explorer.py`](./TC006_Search_and_filter_projects_in_the_explorer.py)
- **Visualization:** [Test Result Dashboard](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/a92f4bed-0139-4f7e-bdf4-f9463164e7f2)
- **Status:** ✅ Passed
- **Analysis:** Multi-attribute filtering (Sector, Risk Tier, Budget, State) and instant text search dynamically update table results without crashing.

#### Test TC008: Open project details from the explorer
- **Test Code:** [`TC008_Open_project_details_from_the_explorer.py`](./TC008_Open_project_details_from_the_explorer.py)
- **Visualization:** [Test Result Dashboard](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/9ccfa920-02a5-4fb2-aa70-0071bf967ad8)
- **Status:** ❌ Failed
- **Analysis:** Clicking a table row or project ID (e.g., `PRJ-00022`) in ExplorerPage did not trigger client-side navigation to `/projects/:id`. Explorer requires explicit clickable row or anchor links to route to the Project Detail view.

#### Test TC010: Sort and paginate explorer results
- **Test Code:** [`TC010_Sort_and_paginate_explorer_results.py`](./TC010_Sort_and_paginate_explorer_results.py)
- **Visualization:** [Test Result Dashboard](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/47160e3d-6b62-4af2-b4ef-8c04805c245a)
- **Status:** ✅ Passed
- **Analysis:** Column sorting on cost, overrun %, and risk score work smoothly alongside page navigation controls.

---

### Feature: Project Detail & Deep Dive
#### Test TC002: Inspect project predictions and explainability
- **Test Code:** [`TC002_Inspect_project_predictions_and_explainability.py`](./TC002_Inspect_project_predictions_and_explainability.py)
- **Visualization:** [Test Result Dashboard](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/f481e304-15b3-41c3-9f7f-f0480fbd5303)
- **Status:** ✅ Passed
- **Analysis:** XGBoost predictive forecasts, confidence bounds, and SHAP top delay drivers load and render correctly for existing projects.

#### Test TC004: Review project progress and milestone context
- **Test Code:** [`TC004_Review_project_progress_and_milestone_context.py`](./TC004_Review_project_progress_and_milestone_context.py)
- **Visualization:** [Test Result Dashboard](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/6e123948-ebfc-4b7f-9bd5-6f70c9ab29fd)
- **Status:** ✅ Passed
- **Analysis:** Physical vs financial S-curve progress and Milestone Gantt timeline render accurately.

#### Test TC013: Handle a project detail page for a nonexistent project
- **Test Code:** [`TC013_Handle_a_project_detail_page_for_a_nonexistent_project.py`](./TC013_Handle_a_project_detail_page_for_a_nonexistent_project.py)
- **Visualization:** [Test Result Dashboard](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/90b5918c-80df-49df-b833-3a86befe374d)
- **Status:** ❌ Failed
- **Analysis:** Navigating to an invalid/missing project ID (e.g. `/projects/999999`) silently redirects to the dashboard or blank view instead of displaying a clear 404 / "Project Not Found" state with a return button.

---

### Feature: Early Warning Alerts
#### Test TC003: Acknowledge an active alert
- **Test Code:** [`TC003_Acknowledge_an_active_alert.py`](./TC003_Acknowledge_an_active_alert.py)
- **Visualization:** [Test Result Dashboard](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/9182d48b-e0d9-40f0-a7d4-95592e438a92)
- **Status:** ✅ Passed
- **Analysis:** Acknowledging an active alert sends the update payload and updates badge counters in real-time.

#### Test TC009: Review alert ordering and categories
- **Test Code:** [`TC009_Review_alert_ordering_and_categories.py`](./TC009_Review_alert_ordering_and_categories.py)
- **Visualization:** [Test Result Dashboard](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/9e476dc9-f797-4d3e-993f-2ae3832bf1d9)
- **Status:** ✅ Passed
- **Analysis:** Alert severity categorization (Critical, Warning, Advisory) and chronological sorting function properly.

#### Test TC012: Show an empty alert state
- **Test Code:** [`TC012_Show_an_empty_alert_state.py`](./TC012_Show_an_empty_alert_state.py)
- **Visualization:** [Test Result Dashboard](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/8fddc619-34c9-4b7f-9e26-cfdb32ae623b)
- **Status:** ✅ Passed
- **Analysis:** Filtering by a category with 0 alerts cleanly displays the empty state placeholder illustration and text.

---

### Feature: Model Comparison & Analytics
#### Test TC007: Compare model metrics and ablation results
- **Test Code:** [`TC007_Compare_model_metrics_and_ablation_results.py`](./TC007_Compare_model_metrics_and_ablation_results.py)
- **Visualization:** [Test Result Dashboard](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/2ad200b4-5de0-4329-bdcf-72525f66fc63)
- **Status:** ✅ Passed
- **Analysis:** Classical statistical vs ML benchmark tables (MAE, RMSE, R²) and CUF feature ablation metrics render clearly.

#### Test TC011: Identify the strongest forecasting model
- **Test Code:** [`TC011_Identify_the_strongest_forecasting_model.py`](./TC011_Identify_the_strongest_forecasting_model.py)
- **Visualization:** [Test Result Dashboard](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/5e67376e-944b-4ca0-bd97-1b2ebdefaa8b)
- **Status:** ✅ Passed
- **Analysis:** Highlighting the leading model card with best performance metrics works seamlessly.

#### Test TC014: Handle unsupported model ablation filters
- **Test Code:** [`TC014_Handle_unsupported_model_ablation_filters.py`](./TC014_Handle_unsupported_model_ablation_filters.py)
- **Visualization:** [Test Result Dashboard](https://www.testsprite.com/dashboard/mcp/tests/2251f2bf-3f9b-5ee5-a423-c02576dade29/test/9fc0a42d-67c6-4b7c-aff6-06b338e3f6a0)
- **Status:** ✅ Passed
- **Analysis:** Gracefully handles edge cases and filter combinations on the model comparison page.

---

## 3️⃣ Coverage & Matching Metrics

- **Pass Rate:** **85.71%** (12 / 14 Tests Passed)

| Requirement / Feature Module | Total Tests | ✅ Passed | ❌ Failed | Pass Rate |
| :--- | :---: | :---: | :---: | :---: |
| **Overview Dashboard** | 2 | 2 | 0 | 100% |
| **Project Explorer** | 3 | 2 | 1 | 66.7% |
| **Project Detail & Deep Dive** | 3 | 2 | 1 | 66.7% |
| **Early Warning Alerts** | 3 | 3 | 0 | 100% |
| **Model Comparison & Analytics** | 3 | 3 | 0 | 100% |
| **Total** | **14** | **12** | **2** | **85.71%** |

---

## 4️⃣ Key Gaps / Risks

1. **Explorer Row Navigation (TC008):**
   - *Issue:* Clicking a project item/row in `ExplorerPage.jsx` does not navigate the user to `/projects/:id`.
   - *Fix:* Ensure project rows/links have `onClick={() => navigate('/projects/' + project.id)}` or a `<Link to={'/projects/' + project.id}>` on the Project ID / Action column.

2. **Project Detail 404 / Not Found State (TC013):**
   - *Issue:* When navigating directly to a non-existent project (e.g. `/projects/999999`), the page does not render an explicit 404 / "Project Not Found" UI.
   - *Fix:* In `ProjectDetailPage.jsx`, when the API returns 404 or null project data, display a dedicated empty/error card informing the user that the project was not found with a button to return to the Explorer.
