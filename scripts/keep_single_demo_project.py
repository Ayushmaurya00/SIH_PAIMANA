"""
PAIMANA AI - Single Project Retainment Utility
"""

import os
import sqlite3
import json

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "paimana.db"))


def keep_only_one_project(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    target_pid = "PRJ-00001"

    for tbl in ["alerts", "risk_scores", "model_predictions", "milestones", "monthly_snapshots", "projects"]:
        cur.execute(f"DELETE FROM {tbl} WHERE project_id != ?", (target_pid,))

    cur.execute("""
        INSERT INTO projects (
            project_id, project_name, ministry, sector, implementing_agency, state,
            approved_cost_cr, revised_cost_cr, cumulative_expenditure_cr,
            approval_date, scheduled_start, scheduled_completion, revised_completion,
            physical_progress_pct, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ON CONFLICT(project_id) DO UPDATE SET
            project_name=excluded.project_name, revised_cost_cr=excluded.revised_cost_cr,
            cumulative_expenditure_cr=excluded.cumulative_expenditure_cr,
            physical_progress_pct=excluded.physical_progress_pct, status=excluded.status
    """, (
        target_pid, "Dedicated Freight Corridor (Eastern Sector) - Sahnewal to Dankuni",
        "Ministry of Railways", "Railways", "DFCCIL", "Uttar Pradesh", 81459.0, 95200.0,
        78400.0, "2021-03-15", "2021-06-01", "2025-12-31", "2027-08-31", 68.5, "Delayed"
    ))

    cur.execute("DELETE FROM monthly_snapshots WHERE project_id = ?", (target_pid,))
    snapshots = [
        ("2025-09-01", 90100.0, 61200.0, 52.0, "Delayed"), ("2025-10-01", 90100.0, 62800.0, 53.5, "Delayed"),
        ("2025-11-01", 91500.0, 64500.0, 55.0, "Delayed"), ("2025-12-01", 91500.0, 66100.0, 56.5, "Delayed"),
        ("2026-01-01", 92800.0, 68000.0, 58.0, "Delayed"), ("2026-02-01", 92800.0, 69800.0, 60.0, "Delayed"),
        ("2026-03-01", 94000.0, 71500.0, 61.8, "Delayed"), ("2026-04-01", 94000.0, 73200.0, 63.5, "Delayed"),
        ("2026-05-01", 94800.0, 75000.0, 65.2, "Delayed"), ("2026-06-01", 94800.0, 76200.0, 66.8, "Delayed"),
        ("2026-07-01", 95200.0, 77500.0, 67.8, "Delayed"), ("2026-08-01", 95200.0, 78400.0, 68.5, "Delayed")
    ]
    for month, rev_cost, exp, prog, st in snapshots:
        cur.execute("INSERT INTO monthly_snapshots (project_id, snapshot_month, revised_cost_cr, cumulative_expenditure_cr, physical_progress_pct, status) VALUES (?, ?, ?, ?, ?, ?)", (target_pid, month, rev_cost, exp, prog, st))

    cur.execute("DELETE FROM milestones WHERE project_id = ?", (target_pid,))
    milestones = [
        ("Land Acquisition & Right-of-Way Handover", "2021-12-31", "2023-04-15", 1),
        ("Statutory Environmental & Forest Clearances", "2022-06-30", "2022-08-20", 0),
        ("Detailed Engineering, Track & Bridge Design", "2022-12-31", "2022-12-31", 0),
        ("Civil Foundation, Embankment & Earthworks", "2024-06-30", "2025-01-20", 1),
        ("Track Laying, 25kV OHE & Signalling Systems", "2025-06-30", None, 1),
        ("CRS Safety Inspection, Trials & Final COD", "2025-12-31", None, 1)
    ]
    for m_name, planned, achieved, is_d in milestones:
        cur.execute("INSERT INTO milestones (project_id, milestone_name, planned_date, achieved_date, is_delayed) VALUES (?, ?, ?, ?, ?)", (target_pid, m_name, planned, achieved, is_d))

    cur.execute("DELETE FROM model_predictions WHERE project_id = ?", (target_pid,))
    cur.execute("""
        INSERT INTO model_predictions (
            project_id, model_name, model_version, feature_set, cost_overrun_prob,
            cost_overrun_pct_pred, cost_overrun_pct_lower, cost_overrun_pct_upper,
            time_overrun_prob, time_overrun_months_pred, time_delay_lower_months,
            time_delay_upper_months, predicted_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (target_pid, "xgboost_ensemble", "v2.1", "cuf_plus_extra", 0.942, 16.87, 12.5, 21.2, 0.985, 20.0, 15.0, 25.0))

    cur.execute("DELETE FROM risk_scores WHERE project_id = ?", (target_pid,))
    factors = [
        {"factor": "Critical Milestone Slippage", "contribution": 32.5, "detail": "Delayed Right-of-Way Handover & Civil Foundation phases"},
        {"factor": "Financial Burn vs Physical Execution Gap", "contribution": 26.8, "detail": "Cumulative spend (₹78,400 Cr) outpaces physical progress (68.5%)"},
        {"factor": "Megaproject Scale Volatility", "contribution": 18.2, "detail": "Capital outlay > ₹80,000 Cr exhibits non-linear execution friction"}
    ]
    actions = [
        {"title": "Expedite Track Laying & OHE Contract Package", "authority": "Railway Board & DFCCIL MD", "statutory_timeline_days": 30, "recommended_action": "Issue high-level directive to EPC contractors for double-shift execution on Sahnewal-Dankuni stretch."},
        {"title": "Inter-Ministerial Right-of-Way Coordination", "authority": "Cabinet Secretariat & Ministry of Railways", "statutory_timeline_days": 15, "recommended_action": "Resolve lingering boundary disputes with state district administrations."}
    ]
    cur.execute("INSERT INTO risk_scores (project_id, score, risk_level, top_factors, prescriptive_actions, previous_score, computed_at) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", (target_pid, 78.4, "High", json.dumps(factors), json.dumps(actions), 74.2))

    cur.execute("DELETE FROM alerts WHERE project_id = ?", (target_pid,))
    cur.execute("INSERT INTO alerts (project_id, trigger_reason, severity, status, prescriptive_action, lead_time_months, triggered_at) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", (target_pid, "Physical execution gap (68.5% progress vs 96.2% financial outlay) and 20-month anticipated COD delay.", "High", "New", "Convene Joint Review Meeting with DFCCIL Managing Director and State Chief Secretaries.", 5.5))

    conn.commit()
    conn.close()
    print("Database cleaned. 1 comprehensive demo project configured successfully.")


if __name__ == "__main__":
    keep_only_one_project()
