"""
PAIMANA AI - Synthetic Infrastructure Project Monitoring Data Generator
"""

import os
import sys
import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.data_gen.models import (
    Base, Project, MonthlySnapshot, Milestone, ModelPrediction, RiskScore, Alert, ModelMetric
)
from src.data_gen.constants import (
    MINISTRY_SECTOR_MAP, SECTOR_AGENCY_MAP, STATES_LIST
)
from src.data_gen.naming import (
    SECTOR_RISK_MODIFIER, AGENCY_RISK_MODIFIER, STATE_TERRAIN_MODIFIER,
    INDIAN_STATES, MILESTONE_TEMPLATES, generate_realistic_project_name
)
from src.data_gen.seeder import generate_synthetic_cuf_dataset

__all__ = [
    "Base", "Project", "MonthlySnapshot", "Milestone", "ModelPrediction",
    "RiskScore", "Alert", "ModelMetric", "MINISTRY_SECTOR_MAP",
    "SECTOR_AGENCY_MAP", "STATES_LIST", "SECTOR_RISK_MODIFIER",
    "AGENCY_RISK_MODIFIER", "STATE_TERRAIN_MODIFIER", "INDIAN_STATES",
    "MILESTONE_TEMPLATES", "generate_realistic_project_name",
    "generate_synthetic_cuf_dataset"
]

if __name__ == "__main__":
    db_file = os.path.join(ROOT_DIR, "paimana.db")
    generate_synthetic_cuf_dataset(n_projects=100, db_path=db_file)
