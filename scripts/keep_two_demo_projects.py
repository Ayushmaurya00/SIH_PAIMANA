"""
PAIMANA AI - Two Demo Projects Retainment Utility
"""

import os
import sqlite3
import json

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "paimana.db"))

DEMO_PROJECTS = [
    {
        "project": ("PRJ-00001", "Dedicated Freight Corridor (Eastern Sector) - Sahnewal to Dankuni", "Ministry of Railways", "Railways", "DFCCIL", "Uttar Pradesh", 81459.0, 95200.0, 78400.0, "2021-03-15", "2021-06-01", "2025-12-31", "2027-08-31", 68.5, "Delayed"),
        "snapshots": [("2025-09-01", 90100.0, 61200.0, 52.0, "Delayed"), ("2026-08-01", 95200.0, 78400.0, 68.5, "Delayed")],
        "milestones": [("Land Acquisition Handover", "2021-12-31", "2023-04-15", 1), ("Civil Foundation Works", "2024-06-30", "2025-01-20", 1), ("CRS Safety Inspection", "2025-12-31", None, 1)],
        "prediction": ("PRJ-00001", "xgboost_ensemble", "v2.1", "cuf_plus_extra", 0.942, 16.87, 12.5, 21.2, 0.985, 20.0, 15.0, 25.0),
        "score": ("PRJ-00001", 78.4, "High", [{"factor": "Milestone Slippage", "contribution": 32.5}], [{"title": "Expedite Track Package", "authority": "Railway Board", "statutory_timeline_days": 30, "recommended_action": "Double-shift EPC execution."}], 74.2),
        "alert": ("PRJ-00001", "Execution gap and 20-month COD delay.", "High", "New", "Convene Joint Review Meeting with DFCCIL MD.", 5.5)
    },
    {
        "project": ("PRJ-00002", "Delhi-Mumbai Expressway Package 14 - Vadodara to Kim Section", "Ministry of Road Transport and Highways", "Road Transport & Highways", "NHAI", "Gujarat", 8711.0, 8711.0, 8100.0, "2022-01-10", "2022-04-01", "2026-11-30", "2026-11-30", 92.4, "On Track"),
        "snapshots": [("2025-09-01", 8711.0, 6500.0, 74.0, "On Track"), ("2026-08-01", 8711.0, 8100.0, 92.4, "On Track")],
        "milestones": [("Land Possession & 3D Clearance", "2022-06-30", "2022-06-15", 0), ("Bituminous Pavement Laying", "2025-12-31", "2025-12-20", 0), ("Final Safety Audit & COD", "2026-11-30", None, 0)],
        "prediction": ("PRJ-00002", "xgboost_ensemble", "v2.1", "cuf_plus_extra", 0.085, 0.0, -1.5, 2.0, 0.052, 0.0, -0.5, 1.0),
        "score": ("PRJ-00002", 18.2, "Low", [{"factor": "Optimal Milestone Completion", "contribution": 8.0}], [{"title": "Pre-COD Safety Audit", "authority": "NHAI Project Director", "statutory_timeline_days": 20, "recommended_action": "Finalize toll plaza testing."}], 19.5),
        "alert": None
    }
]


def keep_two_demo_projects(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    target_pids = ["PRJ-00001", "PRJ-00002"]

    for tbl in ["alerts", "risk_scores", "model_predictions", "milestones", "monthly_snapshots", "projects"]:
        cur.execute(f"DELETE FROM {tbl} WHERE project_id NOT IN (?, ?)", (target_pids[0], target_pids[1]))

    for dp in DEMO_PROJECTS:
        pid = dp["project"][0]
        cur.execute("""
            INSERT INTO projects (
                project_id, project_name, ministry, sector, implementing_agency, state,
                approved_cost_cr, revised_cost_cr, cumulative_expenditure_cr,
                approval_date, scheduled_start, scheduled_completion, revised_completion,
                physical_progress_pct, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ON CONFLICT(project_id) DO UPDATE SET
                project_name=excluded.project_name, physical_progress_pct=excluded.physical_progress_pct, status=excluded.status
        """, dp["project"])

        cur.execute("DELETE FROM monthly_snapshots WHERE project_id = ?", (pid,))
        for month, rev_cost, exp, prog, st in dp["snapshots"]:
            cur.execute("INSERT INTO monthly_snapshots (project_id, snapshot_month, revised_cost_cr, cumulative_expenditure_cr, physical_progress_pct, status) VALUES (?, ?, ?, ?, ?, ?)", (pid, month, rev_cost, exp, prog, st))

        cur.execute("DELETE FROM milestones WHERE project_id = ?", (pid,))
        for m_name, planned, achieved, is_d in dp["milestones"]:
            cur.execute("INSERT INTO milestones (project_id, milestone_name, planned_date, achieved_date, is_delayed) VALUES (?, ?, ?, ?, ?)", (pid, m_name, planned, achieved, is_d))

        cur.execute("DELETE FROM model_predictions WHERE project_id = ?", (pid,))
        cur.execute("INSERT INTO model_predictions (project_id, model_name, model_version, feature_set, cost_overrun_prob, cost_overrun_pct_pred, cost_overrun_pct_lower, cost_overrun_pct_upper, time_overrun_prob, time_overrun_months_pred, time_delay_lower_months, time_delay_upper_months, predicted_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", dp["prediction"])

        cur.execute("DELETE FROM risk_scores WHERE project_id = ?", (pid,))
        p_id, sc, lvl, facts, acts, prev = dp["score"]
        cur.execute("INSERT INTO risk_scores (project_id, score, risk_level, top_factors, prescriptive_actions, previous_score, computed_at) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", (p_id, sc, lvl, json.dumps(facts), json.dumps(acts), prev))

        cur.execute("DELETE FROM alerts WHERE project_id = ?", (pid,))
        if dp["alert"]:
            a_pid, rsn, sev, st, act, lt = dp["alert"]
            cur.execute("INSERT INTO alerts (project_id, trigger_reason, severity, status, prescriptive_action, lead_time_months, triggered_at) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", (a_pid, rsn, sev, st, act, lt))

    conn.commit()
    conn.close()
    print("Database cleaned. Exactly 2 demo projects configured successfully.")


if __name__ == "__main__":
    keep_two_demo_projects()
