"""
PAIMANA AI - Production Ingestion & Migration Service (ETL)
Provides idempotent ingestion and upsert operations for monthly CUF snapshot data
and infrastructure project master records.
"""

import os
import sys
import sqlite3
import datetime
import pandas as pd
from typing import Dict, Any, List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.data_gen.generate_data import Project, MonthlySnapshot, Milestone, Base


def get_db_session(db_path: str = "paimana.db"):
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def upsert_monthly_snapshot(
    project_id: str,
    snapshot_month: datetime.date,
    revised_cost_cr: float,
    cumulative_expenditure_cr: float,
    physical_progress_pct: float,
    status: str,
    db_path: str = "paimana.db"
) -> Dict[str, Any]:
    """
    Idempotently upserts a monthly snapshot record for a project.
    If a snapshot for (project_id, snapshot_month) exists, updates it; otherwise inserts.
    """
    session = get_db_session(db_path)
    try:
        # Check if project exists
        project = session.query(Project).filter_by(project_id=project_id).first()
        if not project:
            raise ValueError(f"Project ID '{project_id}' not found in master database.")

        existing = session.query(MonthlySnapshot).filter_by(
            project_id=project_id,
            snapshot_month=snapshot_month
        ).first()

        if existing:
            existing.revised_cost_cr = revised_cost_cr
            existing.cumulative_expenditure_cr = cumulative_expenditure_cr
            existing.physical_progress_pct = physical_progress_pct
            existing.status = status
            action = "updated"
            snapshot_id = existing.snapshot_id
        else:
            new_snap = MonthlySnapshot(
                project_id=project_id,
                snapshot_month=snapshot_month,
                revised_cost_cr=revised_cost_cr,
                cumulative_expenditure_cr=cumulative_expenditure_cr,
                physical_progress_pct=physical_progress_pct,
                status=status
            )
            session.add(new_snap)
            session.flush()
            action = "inserted"
            snapshot_id = new_snap.snapshot_id

        # Update latest telemetry on Project master
        project.revised_cost_cr = revised_cost_cr
        project.cumulative_expenditure_cr = cumulative_expenditure_cr
        project.physical_progress_pct = physical_progress_pct
        project.status = status
        project.updated_at = datetime.datetime.now(datetime.timezone.utc)

        session.commit()
        return {
            "status": "success",
            "action": action,
            "project_id": project_id,
            "snapshot_id": snapshot_id,
            "snapshot_month": str(snapshot_month)
        }
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def bulk_ingest_snapshots_csv(csv_path: str, db_path: str = "paimana.db") -> Dict[str, Any]:
    """
    Ingests monthly snapshots from a CSV file in bulk with transaction guarantees.
    """
    df = pd.read_csv(csv_path)
    required_cols = {'project_id', 'snapshot_month', 'revised_cost_cr', 'cumulative_expenditure_cr', 'physical_progress_pct', 'status'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV missing required columns. Must contain: {required_cols}")

    inserted = 0
    updated = 0

    session = get_db_session(db_path)
    try:
        for _, row in df.iterrows():
            s_date = datetime.datetime.strptime(str(row['snapshot_month'])[:10], '%Y-%m-%d').date()
            existing = session.query(MonthlySnapshot).filter_by(
                project_id=str(row['project_id']),
                snapshot_month=s_date
            ).first()

            if existing:
                existing.revised_cost_cr = float(row['revised_cost_cr'])
                existing.cumulative_expenditure_cr = float(row['cumulative_expenditure_cr'])
                existing.physical_progress_pct = float(row['physical_progress_pct'])
                existing.status = str(row['status'])
                updated += 1
            else:
                new_snap = MonthlySnapshot(
                    project_id=str(row['project_id']),
                    snapshot_month=s_date,
                    revised_cost_cr=float(row['revised_cost_cr']),
                    cumulative_expenditure_cr=float(row['cumulative_expenditure_cr']),
                    physical_progress_pct=float(row['physical_progress_pct']),
                    status=str(row['status'])
                )
                session.add(new_snap)
                inserted += 1

        session.commit()
        return {"status": "success", "inserted": inserted, "updated": updated, "total_processed": len(df)}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


if __name__ == "__main__":
    print("[ETL] Testing single idempotent snapshot upsert...")
    res = upsert_monthly_snapshot(
        project_id="PRJ-00001",
        snapshot_month=datetime.date(2026, 8, 1),
        revised_cost_cr=1250.0,
        cumulative_expenditure_cr=620.0,
        physical_progress_pct=52.0,
        status="On Track"
    )
    print("Result:", res)
