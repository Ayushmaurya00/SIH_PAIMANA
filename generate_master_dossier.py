"""
PAIMANA AI - Master Technical Dossier & Jury Defense PDF Generator
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.dossier.builder import generate_master_dossier_pdf

if __name__ == "__main__":
    out_file = os.path.join(ROOT_DIR, "PAIMANA_AI_MASTER_DOSSIER.pdf")
    generate_master_dossier_pdf(out_file)
