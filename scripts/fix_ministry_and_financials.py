"""
PAIMANA AI - Database Data Integrity & Ministry Mapping Fixer
"""

import os
import sys
import json
import sqlite3

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.etl.cuf.schema import SECTOR_TO_MINISTRY_MAP

DB_PATH = os.path.join(ROOT_DIR, "paimana.db")

SECTOR_TO_AGENCY_MAP = {
    "Road Transport & Highways": "NHAI", "Railways": "RVNL", "Power Transmission & Distribution": "PGCIL",
    "Thermal Power Generation": "NTPC", "Hydroelectric Power": "NHPC", "Petroleum & Natural Gas Pipelines": "GAIL",
    "Oil Refineries & Petrochemicals": "IOCL", "Coal Mining & Infrastructure": "Coal India (CIL)",
    "Steel & Metallurgy": "SAIL", "Urban Metro & Transit Systems": "DMRC", "Civil Aviation & Airports": "AAI",
    "Ports & Maritime Infrastructure": "JNPA", "Telecommunications & Optical Fibre": "BSNL / BBNL"
}


def fix_data_integrity(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("DELETE FROM projects WHERE project_id LIKE 'PRJ-TOTAL%' OR project_id LIKE 'PRJ-SUMMARY%' OR LOWER(project_name) LIKE '%total%' OR LOWER(project_name) LIKE '%summary%'")
    cur.execute("DELETE FROM monthly_snapshots WHERE project_id NOT IN (SELECT project_id FROM projects)")
    cur.execute("DELETE FROM milestones WHERE project_id NOT IN (SELECT project_id FROM projects)")

    rows = cur.execute("SELECT project_id, sector, implementing_agency, approved_cost_cr, revised_cost_cr, cumulative_expenditure_cr, physical_progress_pct, status FROM projects").fetchall()
    print(f"Auditing and standardizing {len(rows)} projects...")

    for pid, sec, agency, app_cost, rev_cost, cum_exp, prog, st in rows:
        correct_min = SECTOR_TO_MINISTRY_MAP.get(sec, "Ministry of Road Transport and Highways (MoRTH)")
        correct_agency = agency
        if not agency or agency in ["Central PSU", "Unknown", "N/A", "Central Agency SPV"]:
            correct_agency = SECTOR_TO_AGENCY_MAP.get(sec, "Central Agency SPV")

        app_c = max(10.0, float(app_cost or 100.0))
        rev_c = max(app_c, float(rev_cost or app_c))
        exp_c = min(rev_c * 1.2, max(0.0, float(cum_exp or 0.0)))
        prog_p = min(100.0, max(0.0, float(prog or 0.0)))

        cur.execute("""
            UPDATE projects SET
                ministry = ?, implementing_agency = ?, approved_cost_cr = ?,
                revised_cost_cr = ?, cumulative_expenditure_cr = ?,
                physical_progress_pct = ?
            WHERE project_id = ?
        """, (correct_min, correct_agency, app_c, rev_c, exp_c, prog_p, pid))

    conn.commit()
    conn.close()
    print("Data integrity fix completed successfully.")


if __name__ == "__main__":
    fix_data_integrity()
