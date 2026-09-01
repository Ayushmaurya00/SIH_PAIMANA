"""
PAIMANA AI - PDF Ingestion Re-export Shim for Backward Compatibility
"""

from src.etl.pdf.constants import (
    SECTOR_TO_MINISTRY_MAP, MINISTRY_CANONICAL_MAP, KNOWN_MINISTRIES
)
from src.etl.pdf.sanitizer import (
    canonicalise_ministry, infer_ministry_and_sector, is_skip_row,
    extract_project_code, clean_project_name, parse_float, clean_state,
    normalise_date, derive_status
)
from src.etl.pdf.row_parser import parse_table_row
from src.etl.pdf.engine import MoSPIIngestionEngine, ingest_pdf_file

__all__ = [
    "SECTOR_TO_MINISTRY_MAP",
    "MINISTRY_CANONICAL_MAP",
    "KNOWN_MINISTRIES",
    "canonicalise_ministry",
    "infer_ministry_and_sector",
    "is_skip_row",
    "extract_project_code",
    "clean_project_name",
    "parse_float",
    "clean_state",
    "normalise_date",
    "derive_status",
    "parse_table_row",
    "MoSPIIngestionEngine",
    "ingest_pdf_file",
]
