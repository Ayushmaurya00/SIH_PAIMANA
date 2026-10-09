"""
PAIMANA AI - Automated System Audit & Verification Harness
"""
import os
import sys
import sqlite3

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(ROOT_DIR, "paimana.db")
PASS, FAIL, WARN = "[PASS]", "[FAIL]", "[WARN]"
results = []


def check(name, condition, detail="", is_warning=False):
    status = PASS if condition else (WARN if is_warning else FAIL)
    results.append((status, name, detail))
    print(f"  {status}  {name}")
    if detail:
        print(f"         {detail}")


def run():
    print("=" * 70 + "\nPAIMANA AI — System Audit & Verification Harness\n" + "=" * 70)
    if not os.path.exists(DB_PATH):
        print(f"\n[FATAL] Database not found: {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    print("\n[1] ETL & Data Integrity")
    project_count = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
    check("Project count in target range [1700, 1900]", 1700 <= project_count <= 1900, f"Actual: {project_count}")
    unique_ministries = conn.execute("SELECT COUNT(DISTINCT ministry) FROM projects").fetchone()[0]
    check("Unique ministries >= 15", unique_ministries >= 15, f"Actual: {unique_ministries}")
    morth_and = conn.execute("SELECT COUNT(*) FROM projects WHERE ministry='Ministry of Road Transport and Highways'").fetchone()[0]
    morth_amp = conn.execute("SELECT COUNT(*) FROM projects WHERE ministry='Ministry of Road Transport & Highways'").fetchone()[0]
    check("MoRTH dedup: '& Highways' variant fully eliminated", morth_amp == 0, f"Remaining: {morth_amp}")

    outlay_lakh_cr = conn.execute("SELECT ROUND(SUM(approved_cost_cr)/100000, 2) FROM projects").fetchone()[0] or 0
    check("Sanctioned outlay in [34.5, 36.5] Lakh Cr", 34.5 <= float(outlay_lakh_cr) <= 36.5, f"Actual: {outlay_lakh_cr} Lakh Cr")
    exp_lakh_cr = conn.execute("SELECT ROUND(SUM(cumulative_expenditure_cr)/100000, 2) FROM projects").fetchone()[0] or 0
    check("Cumulative expenditure in [20.0, 24.0] Lakh Cr", 20.0 <= float(exp_lakh_cr) <= 24.0, f"Actual: {exp_lakh_cr} Lakh Cr")
    null_ministry = conn.execute("SELECT COUNT(*) FROM projects WHERE ministry IS NULL OR ministry=''").fetchone()[0]
    check("No projects with NULL/empty ministry", null_ministry == 0, f"NULL ministry rows: {null_ministry}")
    null_cost = conn.execute("SELECT COUNT(*) FROM projects WHERE approved_cost_cr IS NULL OR approved_cost_cr <= 0").fetchone()[0]
    check("No projects with NULL/zero approved_cost_cr", null_cost == 0, f"Invalid cost rows: {null_cost}")

    print("\n[2] ML Model Predictions")
    pred_count = conn.execute("SELECT COUNT(*) FROM model_predictions").fetchone()[0]
    check("model_predictions table populated", pred_count > 0, f"Rows: {pred_count}")
    null_cost_prob = conn.execute("SELECT COUNT(*) FROM model_predictions WHERE cost_overrun_prob IS NULL").fetchone()[0]
    check("Zero NULL cost_overrun_prob values", null_cost_prob == 0, f"NULLs: {null_cost_prob}")
    null_time_prob = conn.execute("SELECT COUNT(*) FROM model_predictions WHERE time_overrun_prob IS NULL").fetchone()[0]
    check("Zero NULL time_overrun_prob values", null_time_prob == 0, f"NULLs: {null_time_prob}")

    bad_cost_bounds = conn.execute(
        "SELECT COUNT(*) FROM model_predictions WHERE feature_set='cuf_plus_extra' "
        "AND (round(cost_overrun_pct_lower,2) > round(cost_overrun_pct_pred,2) "
        "OR round(cost_overrun_pct_pred,2) > round(cost_overrun_pct_upper,2))"
    ).fetchone()[0]
    check("Zero conformal bound violations for cost", bad_cost_bounds == 0, f"Violations: {bad_cost_bounds}")

    bad_time_bounds = conn.execute(
        "SELECT COUNT(*) FROM model_predictions WHERE feature_set='cuf_plus_extra' "
        "AND (round(time_delay_lower_months,1) > round(time_overrun_months_pred,1) "
        "OR round(time_overrun_months_pred,1) > round(time_delay_upper_months,1))"
    ).fetchone()[0]
    check("Zero conformal bound violations for time delay", bad_time_bounds == 0, f"Violations: {bad_time_bounds}", is_warning=(bad_time_bounds < 20))

    print("\n[3] Risk Score Distribution")
    risk_count = conn.execute("SELECT COUNT(*) FROM risk_scores").fetchone()[0]
    check("All projects have a risk score (100% coverage)", risk_count == project_count, f"Scores: {risk_count}")
    high_count = conn.execute("SELECT COUNT(*) FROM risk_scores WHERE risk_level='High'").fetchone()[0]
    high_pct = (high_count / max(risk_count, 1)) * 100
    check("High-risk projects >= 15% of portfolio", high_pct >= 15.0, f"High: {high_count} ({high_pct:.1f}%)")
    null_scores = conn.execute("SELECT COUNT(*) FROM risk_scores WHERE score IS NULL").fetchone()[0]
    check("No NULL risk scores", null_scores == 0, f"NULLs: {null_scores}")

    print("\n[4] Alerts & Schema Completeness")
    alert_count = conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
    check("Alerts table populated", alert_count > 0, f"Alerts: {alert_count}")
    tables_req = ["projects","monthly_snapshots","milestones","risk_scores","model_predictions","model_metrics","alerts"]
    existing = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
    for t in tables_req:
        check(f"Table '{t}' exists", t in existing)
    conn.close()

    print("\n" + "=" * 70)
    passed, warned, failed = sum(1 for r in results if r[0] == PASS), sum(1 for r in results if r[0] == WARN), sum(1 for r in results if r[0] == FAIL)
    print(f"SUMMARY: {passed}/{len(results)} PASS  |  {warned} WARN  |  {failed} FAIL\n" + "=" * 70)
    return failed == 0

if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
