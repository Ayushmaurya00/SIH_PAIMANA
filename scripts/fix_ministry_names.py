"""
PAIMANA AI - One-Time Ministry Name De-Duplication Script
==========================================================
Consolidates all '& Highways' / '& Natural Gas' / etc. variants to their
canonical 'and' spelling across every table in paimana.db.

Run once after pulling this patch:
    py scripts/fix_ministry_names.py
"""
import os
import sys
import sqlite3

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH  = os.path.join(ROOT_DIR, "paimana.db")

# (old_name, canonical_name)
RENAME_PAIRS = [
    ("Ministry of Road Transport & Highways",
     "Ministry of Road Transport and Highways"),
    ("Ministry of Road Transport and Highways (MoRTH)",
     "Ministry of Road Transport and Highways"),
    ("Ministry of Petroleum & Natural Gas",
     "Ministry of Petroleum and Natural Gas"),
    ("Ministry of Petroleum and Natural Gas (MoPNG)",
     "Ministry of Petroleum and Natural Gas"),
    ("Ministry of Housing & Urban Affairs",
     "Ministry of Housing and Urban Affairs"),
    ("Ministry of Housing and Urban Affairs (MoHUA)",
     "Ministry of Housing and Urban Affairs"),
    ("Ministry of Health & Family Welfare",
     "Ministry of Health and Family Welfare"),
    ("Department of Water Resources, River Development & GR",
     "Department of Water Resources, River Development and GR"),
    ("Department for Promotion of Industry & Internal Trade",
     "Department for Promotion of Industry and Internal Trade"),
    ("Ministry of Power (MoP)",
     "Ministry of Power"),
    ("Ministry of Railways (MoR)",
     "Ministry of Railways"),
    ("Ministry of Ports, Shipping and Waterways (MoPSW)",
     "Ministry of Ports, Shipping and Waterways"),
    ("Ministry of Civil Aviation (MoCA)",
     "Ministry of Civil Aviation"),
    ("Ministry of Communications",
     "Department of Telecommunications"),
]

TABLES_WITH_MINISTRY = ["projects"]

def run():
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database not found: {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    total_updated = 0

    print("=" * 60)
    print("PAIMANA AI — Ministry Name De-Duplication")
    print("=" * 60)

    for old, canonical in RENAME_PAIRS:
        # Check how many rows need updating
        count_row = cur.execute(
            "SELECT COUNT(*) FROM projects WHERE ministry = ?", (old,)
        ).fetchone()[0]
        if count_row == 0:
            continue

        cur.execute(
            "UPDATE projects SET ministry = ? WHERE ministry = ?",
            (canonical, old)
        )
        updated = cur.rowcount
        total_updated += updated
        print(f"  [OK] [{old}] -> [{canonical}]  ({updated} rows)")

    conn.commit()

    print()
    print(f"Total rows updated: {total_updated}")
    print()
    print("Ministry distribution after fix:")
    for row in cur.execute(
        "SELECT ministry, COUNT(*) as c FROM projects GROUP BY ministry ORDER BY 2 DESC"
    ).fetchall():
        print(f"  {row[0]}: {row[1]}")

    conn.close()
    print()
    print("[DONE] Ministry names are now fully normalised.")
    print("Re-run risk scoring to regenerate ministry-grouped analytics:")
    print("  py scripts/ingest_flash_report.py   (or just restart the backend)")

if __name__ == "__main__":
    run()
