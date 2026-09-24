"""
PAIMANA AI - Flash Report Ingestion Pipeline
"""

import os
import sys
import sqlite3
import logging
import argparse
import json

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("IngestPipeline")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

DB_PATH = os.path.join(ROOT_DIR, "paimana.db")
PDF_PATH = os.path.join(ROOT_DIR, "data", "raw", "FlashReport_June_2026.pdf")
SNAP_MONTH = "2026-06-01"
PURGE_TABLES = ["model_predictions", "risk_scores", "alerts", "milestones", "monthly_snapshots", "projects"]


def purge_tables(db_path: str) -> None:
    logger.info("Purging contaminated tables...")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = OFF")
    for tbl in PURGE_TABLES:
        cur.execute(f"DELETE FROM {tbl}")
    cur.execute("PRAGMA foreign_keys = ON")
    conn.commit()
    conn.close()
    logger.info("Purge complete.")


def run_pipeline(pdf_path: str, db_path: str, snap_month: str, purge: bool = True) -> bool:
    if purge:
        purge_tables(db_path)

    from src.etl.pdf_ingestion import ingest_pdf_file
    logger.info(f"Running PyMuPDF ingestion on: {pdf_path}")
    result = ingest_pdf_file(pdf_path, db_path, reference_month=snap_month)
    logger.info(f"Ingestion result: projects_upserted={result.get('projects_upserted')}")

    try:
        from src.models.train_and_evaluate import run_fast_inference
        run_fast_inference(db_path)
    except Exception as e:
        logger.warning(f"Inference warning: {e}")

    try:
        from src.risk_engine.scorer import calculate_risk_scores, load_project_data
        df_p, df_s, df_m, df_preds = load_project_data(db_path)
        scores, alerts_list = calculate_risk_scores(df_p, df_s, df_m, df_preds)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM risk_scores")
        cur.execute("DELETE FROM alerts")
        for s in scores:
            cur.execute("INSERT INTO risk_scores (project_id, score, risk_level, top_factors, prescriptive_actions, computed_at) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", (s['project_id'], s['score'], s['risk_level'], json.dumps(s['top_factors']), json.dumps(s['prescriptive_actions'])))
        for a in alerts_list:
            cur.execute("INSERT INTO alerts (project_id, trigger_reason, severity, status, prescriptive_action, lead_time_months, triggered_at) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", (a['project_id'], a['trigger_reason'], a['severity'], a['status'], a['prescriptive_action'], a['lead_time_months']))
        conn.commit()
        conn.close()
        logger.info(f"Risk scoring complete: {len(scores)} scores, {len(alerts_list)} alerts.")
    except Exception as e:
        logger.warning(f"Risk scoring warning: {e}")

    conn = sqlite3.connect(db_path)
    count = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
    conn.close()
    logger.info(f"Total projects in database: {count}")
    return count > 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest MoSPI Flash Report PDF")
    parser.add_argument("--pdf", default=PDF_PATH, help="Path to PDF")
    parser.add_argument("--db", default=DB_PATH, help="Path to SQLite DB")
    parser.add_argument("--month", default=SNAP_MONTH, help="Reference month")
    parser.add_argument("--no-purge", action="store_true", help="Skip table purge")
    args = parser.parse_args()
    ok = run_pipeline(args.pdf, args.db, args.month, purge=not args.no_purge)
    sys.exit(0 if ok else 1)
