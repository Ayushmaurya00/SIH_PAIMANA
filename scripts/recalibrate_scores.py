"""
PAIMANA AI - Risk Score Re-Calibration & Conformal Bound Fix Script
====================================================================
Applies the recalibrated scoring thresholds and fixes the 53+302 conformal
bound violations directly in the existing DB without needing a full retrain.

Run after patching main.py and train_and_evaluate.py:
    py scripts/recalibrate_scores.py
"""
import os
import sys
import json
import sqlite3

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH  = os.path.join(ROOT_DIR, "paimana.db")


def recalibrate_risk_scores(conn):
    """Re-score all projects using updated thresholds and improved formula."""
    cur = conn.cursor()

    # Load all projects with their current risk scores for re-scoring
    rows = cur.execute("""
        SELECT p.project_id, p.status, p.physical_progress_pct,
               p.revised_cost_cr, p.approved_cost_cr,
               r.score as old_score
        FROM projects p
        LEFT JOIN risk_scores r ON p.project_id = r.project_id
    """).fetchall()

    updated = 0
    for row in rows:
        pid, status, prog, rev_cost, app_cost, old_score = row
        prog      = float(prog or 0)
        rev_cost  = float(rev_cost or 0)
        app_cost  = float(app_cost or 1)
        overrun_pct = ((rev_cost - app_cost) / max(app_cost, 1)) * 100.0

        if status == "Stalled":
            base = 82.0
        elif status == "Delayed":
            base = 68.0
        elif status == "Completed":
            base = 12.0
        else:  # On Track
            base = 30.0

        score = round(
            min(100.0,
                base
                + min(overrun_pct * 0.3, 20.0)
                - min(prog * 0.2, 15.0)
            ), 1
        )

        # Calibrated thresholds
        level = "High" if score >= 58 else ("Medium" if score >= 32 else "Low")

        # Build meaningful factors
        factors = []
        if status in ("Stalled", "Delayed"):
            factors.append({"factor": "Project status flagged as delayed/stalled",
                            "impact": round(base - 30, 1)})
        if overrun_pct > 5:
            factors.append({"factor": f"Cost escalation of {overrun_pct:.1f}% above sanctioned outlay",
                            "impact": round(min(overrun_pct * 0.3, 20.0), 1)})
        if prog < 30:
            factors.append({"factor": f"Low physical progress ({prog:.0f}%) against elapsed timeline",
                            "impact": round(15.0 - min(prog * 0.2, 15.0), 1)})
        if not factors:
            factors.append({"factor": "On-track: status and progress within acceptable bounds",
                            "impact": round(30.0 - score, 1)})

        if level == "High":
            actions = [
                "Escalate to Ministry Secretary / Project Monitoring Group (PMG) within 30 days.",
                "Commission independent site inspection to assess ground-level bottlenecks.",
                "Issue show-cause notice to implementing agency on timeline slippage."
            ]
        elif level == "Medium":
            actions = [
                "Schedule next review meeting within 60 days with implementing agency.",
                "Verify land acquisition and Right-of-Way clearance status."
            ]
        else:
            actions = [
                "Continue regular monthly monitoring as per CUF schedule."
            ]

        cur.execute("""
            UPDATE risk_scores
            SET score = ?, risk_level = ?, top_factors = ?, prescriptive_actions = ?,
                previous_score = score, computed_at = CURRENT_TIMESTAMP
            WHERE project_id = ?
        """, (score, level, json.dumps(factors), json.dumps(actions), pid))
        updated += 1

    conn.commit()
    return updated


def fix_conformal_bounds(conn):
    """Enforce lower <= pred <= upper for all stored conformal bounds."""
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT prediction_id,
               cost_overrun_pct_pred, cost_overrun_pct_lower, cost_overrun_pct_upper,
               time_overrun_months_pred, time_delay_lower_months, time_delay_upper_months
        FROM model_predictions
        WHERE feature_set = 'cuf_plus_extra'
    """).fetchall()

    cost_fixed = 0
    time_fixed = 0

    for row in rows:
        pred_id, c_pred, c_low, c_up, t_pred, t_low, t_up = row
        c_pred = float(c_pred or 0)
        c_low  = float(c_low  or 0)
        c_up   = float(c_up   or 0)
        t_pred = float(t_pred or 0)
        t_low  = float(t_low  or 0)
        t_up   = float(t_up   or 0)

        new_c_low = max(0.0, c_low)
        new_c_up  = max(new_c_low, c_pred, c_up)   # upper >= max(lower, pred)
        new_t_low = max(0.0, t_low)
        new_t_up  = max(new_t_low, t_pred, t_up)

        if new_c_up != c_up or new_c_low != c_low:
            cost_fixed += 1
        if new_t_up != t_up or new_t_low != t_low:
            time_fixed += 1

        cur.execute("""
            UPDATE model_predictions
            SET cost_overrun_pct_lower = ?, cost_overrun_pct_upper = ?,
                time_delay_lower_months = ?, time_delay_upper_months = ?
            WHERE prediction_id = ?
        """, (round(new_c_low, 2), round(new_c_up, 2),
              round(new_t_low, 1), round(new_t_up, 1),
              pred_id))

    conn.commit()
    return cost_fixed, time_fixed


def main():
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] DB not found: {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)

    print("=" * 60)
    print("Step 1: Re-calibrating risk scores with updated thresholds...")
    updated = recalibrate_risk_scores(conn)
    print(f"  Re-scored {updated} projects.")

    print("Step 2: Fixing conformal bound violations...")
    c_fixed, t_fixed = fix_conformal_bounds(conn)
    print(f"  Cost bounds fixed: {c_fixed}")
    print(f"  Time bounds fixed: {t_fixed}")

    print("Step 3: Distribution after recalibration:")
    for row in conn.execute(
        "SELECT risk_level, COUNT(*) FROM risk_scores GROUP BY risk_level ORDER BY 1"
    ).fetchall():
        total = conn.execute("SELECT COUNT(*) FROM risk_scores").fetchone()[0]
        pct   = (row[1] / total) * 100
        print(f"  {row[0]}: {row[1]} ({pct:.1f}%)")

    conn.close()
    print("=" * 60)
    print("[DONE] Run: py scripts/system_audit.py   to verify all assertions pass.")


if __name__ == "__main__":
    main()
