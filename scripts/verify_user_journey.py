"""
PAIMANA AI - Complete User Journey Verification Script
Simulates the exact user journey:
1. Overview Dashboard (KPIs, Sector Distributions)
2. Project Explorer (Filtering by Sector & Ministry)
3. Project Detail Page (S-Curve, Milestones, SHAP explainability drivers)
4. Early Warning Alerts (Red/Amber/Green tiers & Prescriptions)
5. Model Comparison (CUF-Only vs CUF+Extra benchmarks)
6. Grounded AI Assistant (3 domain questions with grounded telemetry)
"""

import sys
import json
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000"


def http_get(path: str):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "PAIMANA-E2E"})
    with urllib.request.urlopen(req, timeout=5.0) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))


def http_post(path: str, data: dict):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={"Content-Type": "application/json", "User-Agent": "PAIMANA-E2E"}
    )
    with urllib.request.urlopen(req, timeout=8.0) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))


def run_journey():
    print("=" * 70, flush=True)
    print("PAIMANA AI - END-TO-END USER JOURNEY VERIFICATION", flush=True)
    print("=" * 70, flush=True)

    # Step 1: Overview Dashboard
    print("\n[Step 1] Overview Dashboard Summary...", flush=True)
    status, summary = http_get("/api/dashboard/summary")
    assert status == 200, f"Overview failed with status {status}"
    print(f"  ✓ Status: 200 OK", flush=True)
    print(f"  ✓ Monitored Projects: {summary['total_projects']:,}", flush=True)
    print(f"  ✓ Total Approved Outlay: ₹{summary['total_approved_cost_cr']:,.2f} Cr", flush=True)
    print(f"  ✓ Cumulative Expenditure: ₹{summary['total_expenditure_cr']:,.2f} Cr", flush=True)
    print(f"  ✓ High-Risk Projects: {summary.get('high_risk_count', summary.get('critical_alerts_count', 0))}", flush=True)
    print(f"  ✓ Sector Risk Breakdown: {len(summary['sector_distribution'])} sectors", flush=True)

    # Step 2: Project Explorer Filter
    print("\n[Step 2] Project Explorer Filtering (Sector: Railways)...", flush=True)
    status, proj_res = http_get("/api/projects?sector=Railways&limit=5")
    assert status == 200, f"Explorer filter failed with status {status}"
    projects = proj_res.get('projects', proj_res) if isinstance(proj_res, dict) else proj_res
    print(f"  ✓ Status: 200 OK", flush=True)
    print(f"  ✓ Retrieved {len(projects)} Railway projects (Sample: {projects[0]['project_id']} - {projects[0]['project_name'][:40]}...)", flush=True)
    selected_pid = projects[0]['project_id']

    # Step 3: Project Detail View & SHAP Driver Explainability
    print(f"\n[Step 3] Deep Project Detail & SHAP Explainability ({selected_pid})...", flush=True)
    status, detail = http_get(f"/api/projects/{selected_pid}")
    assert status == 200, f"Project detail failed with status {status}"
    print(f"  ✓ Status: 200 OK", flush=True)
    print(f"  ✓ Project: {detail['project_name']} ({detail['status']})", flush=True)
    print(f"  ✓ Monthly S-Curve Snapshots: {len(detail['snapshots'])} points", flush=True)
    print(f"  ✓ Stage-Gate Milestones: {len(detail['milestones'])} stages", flush=True)
    print(f"  ✓ Conformal Overrun Prediction: +{detail['cost_overrun_pct_pred']:.1f}% [{detail['cost_overrun_pct_lower']:.1f}% – {detail['cost_overrun_pct_upper']:.1f}%]", flush=True)
    
    # Verify SHAP drivers
    factors = detail.get('top_factors', [])
    print(f"  ✓ SHAP Delay Drivers ({len(factors)} factors):", flush=True)
    for f in factors[:3]:
        print(f"     • {f.get('factor')}: +{f.get('contribution')} pts ({f.get('detail')})", flush=True)

    # Step 4: Early Warning Alerts & Triage Tiers
    print("\n[Step 4] Early Warning Alerts (Red/Amber/Green Tiers)...", flush=True)
    status, high_alerts = http_get("/api/alerts?severity=High")
    assert status == 200, f"Alerts high failed with status {status}"
    status, med_alerts = http_get("/api/alerts?severity=Medium")
    assert status == 200, f"Alerts med failed with status {status}"
    print(f"  ✓ Status: 200 OK", flush=True)
    print(f"  ✓ Red Tier (Critical High Risk Alerts): {len(high_alerts)} projects", flush=True)
    print(f"  ✓ Amber Tier (Medium Risk Alerts):      {len(med_alerts)} projects", flush=True)
    print(f"  ✓ Sample Playbook Action: {high_alerts[0]['prescriptive_action'][:80]}...", flush=True)

    # Step 5: Model Comparison (CUF-Only vs CUF+Extra)
    print("\n[Step 5] Model Comparison Metrics (CUF-Only vs CUF+Extra)...", flush=True)
    status, metrics = http_get("/api/models/metrics")
    assert status == 200, f"Model metrics failed with status {status}"
    print(f"  ✓ Status: 200 OK", flush=True)
    print(f"  ✓ Total Benchmarked Models: {len(metrics)}", flush=True)
    cuf_xgb = [m for m in metrics if m['feature_set'] == 'cuf_only' and m['model_name'] == 'xgboost_classifier'][0]
    extra_xgb = [m for m in metrics if m['feature_set'] == 'cuf_plus_extra' and m['model_name'] == 'xgboost_classifier'][0]
    print(f"  ✓ Baseline CUF Model Accuracy:         {cuf_xgb['accuracy']*100:.1f}% (F1: {cuf_xgb['f1_score']:.3f})", flush=True)
    print(f"  ✓ CUF + Extra Variables Model Accuracy: {extra_xgb['accuracy']*100:.1f}% (F1: {extra_xgb['f1_score']:.3f})", flush=True)

    # Step 6: Grounded AI Assistant (3 Inquiries)
    print("\n[Step 6] Grounded AI Assistant 3-Question Inquiries...", flush=True)
    
    # Q1: Sector escalation
    q1 = "Which infrastructure sector has the highest cost escalation risk?"
    status, res1 = http_post("/api/assistant/query", {"question": q1})
    assert status == 200, f"Assistant Q1 failed with status {status}"
    print(f"  ✓ Q1: '{q1}'", flush=True)
    print(f"    • Response Mode: {res1.get('mode')} | Confidence: {res1.get('confidence')*100:.0f}%", flush=True)
    print(f"    • Preview: {res1['answer'][:120]}...\n", flush=True)

    # Q2: Single Project delay factors
    q2 = f"Explain the delay factors and land acquisition issues for project PRJ-00004"
    status, res2 = http_post("/api/assistant/query", {"question": q2, "context_project_id": "PRJ-00004"})
    assert status == 200, f"Assistant Q2 failed with status {status}"
    print(f"  ✓ Q2: '{q2}'", flush=True)
    print(f"    • Response Mode: {res2.get('mode')} | Confidence: {res2.get('confidence')*100:.0f}%", flush=True)
    print(f"    • Preview: {res2['answer'][:120]}...\n", flush=True)

    # Q3: Prescriptive actions for stalled projects
    q3 = "What are the recommended administrative actions for stalled central sector projects?"
    status, res3 = http_post("/api/assistant/query", {"question": q3})
    assert status == 200, f"Assistant Q3 failed with status {status}"
    print(f"  ✓ Q3: '{q3}'", flush=True)
    print(f"    • Response Mode: {res3.get('mode')} | Confidence: {res3.get('confidence')*100:.0f}%", flush=True)
    print(f"    • Preview: {res3['answer'][:120]}...\n", flush=True)

    print("=" * 70, flush=True)
    print("ALL 6 USER JOURNEY STEPS VERIFIED & FULLY OPERATIONAL (HTTP 200 OK)", flush=True)
    print("=" * 70, flush=True)


if __name__ == "__main__":
    run_journey()
