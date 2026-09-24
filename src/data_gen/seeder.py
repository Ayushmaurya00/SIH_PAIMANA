"""
Database Schema Initializer & Seeding Orchestrator
"""

import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.data_gen.models import (
    Base, Project, MonthlySnapshot, Milestone, ModelPrediction, RiskScore, Alert, ModelMetric
)
from src.data_gen.project_gen import generate_single_project
from src.data_gen.snapshot_gen import generate_snapshots_for_project
from src.data_gen.milestone_gen import generate_milestones_for_project


def generate_synthetic_cuf_dataset(
    n_projects: int = 100,
    db_path: str = "paimana.db",
    reference_date: datetime.date = datetime.date(2026, 8, 1)
):
    """Generates synthetic CUF projects, snapshots, and milestones into SQLite."""
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Milestone).delete()
    session.query(MonthlySnapshot).delete()
    session.query(ModelPrediction).delete()
    session.query(RiskScore).delete()
    session.query(Alert).delete()
    session.query(ModelMetric).delete()
    session.query(Project).delete()
    session.commit()

    projects_list = []
    snapshots_list = []
    milestones_list = []

    for i in range(1, n_projects + 1):
        proj, has_overrun = generate_single_project(i, reference_date)
        projects_list.append(proj)
        snaps = generate_snapshots_for_project(proj, has_overrun, reference_date)
        snapshots_list.extend(snaps)
        miles = generate_milestones_for_project(proj, has_overrun)
        milestones_list.extend(miles)

    session.bulk_save_objects(projects_list)
    session.bulk_save_objects(snapshots_list)
    session.bulk_save_objects(milestones_list)
    session.commit()
    session.close()
    print(f"[PAIMANA DataGen] Successfully generated and committed {len(projects_list)} projects, {len(snapshots_list)} snapshots, and {len(milestones_list)} milestones to {db_path}.")
