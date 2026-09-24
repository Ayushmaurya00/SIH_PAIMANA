"""
MoSPI PDF Ingestion Engine & Database Upsert Routine
"""

import os
import sqlite3
import datetime
import logging
from typing import Dict, Any, List, Optional
from src.etl.pdf.row_parser import parse_table_row

logger = logging.getLogger("PAIMANA_PDF_INGEST")


class MoSPIIngestionEngine:
    def __init__(self, db_path: str = "paimana.db"):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def ingest(self, pdf_path: str, reference_month: Optional[str] = None) -> Dict[str, Any]:
        """Parses MoSPI Flash Report PDF and upserts projects into SQLite."""
        try:
            import fitz
        except ImportError:
            raise ImportError("PyMuPDF (fitz) is required for PDF ingestion. Run: pip install pymupdf")

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

        import re
        from src.etl.pdf.constants import MINISTRY_CANONICAL_MAP, SECTOR_TO_MINISTRY_MAP

        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        current_ministry = "Ministry of Road Transport and Highways"
        current_sector = "Road Transport & Highways"
        extracted_projects: Dict[str, Dict[str, Any]] = {}
        warnings: List[str] = []

        ministry_header_re = re.compile(r"^\s*(Ministry of [A-Za-z &()\-]+|Department of [A-Za-z &()\-]+)", re.IGNORECASE)

        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text()
            # Detect ministry header on page and update current context
            for line in text.splitlines()[:15]:
                m = ministry_header_re.search(line.strip())
                if m:
                    raw_min = m.group(1).strip()
                    canon = MINISTRY_CANONICAL_MAP.get(raw_min, raw_min)
                    current_ministry = canon
                    # try to infer sector from map reverse
                    for sec, mini in SECTOR_TO_MINISTRY_MAP.items():
                        if mini.lower() in canon.lower() or canon.lower() in mini.lower():
                            current_sector = sec
                            break
                    break
            if "Table 6" not in text and "Annex" not in text and page_num < 5:
                # Only skip early pages if no table; scan all after page 5
                if page_num < 10 and "Table" not in text:
                    continue

            try:
                tabs = page.find_tables()
            except Exception as e:
                warnings.append(f"Page {page_num + 1}: Table extraction warning: {e}")
                continue

            for tab in tabs:
                for row_cells in tab.extract():
                    p_dict = parse_table_row(row_cells, current_ministry, current_sector)
                    if p_dict:
                        extracted_projects[p_dict["project_id"]] = p_dict

        doc.close()
        # Use reference_month if provided, else env REFERENCE_DATE, else today
        import os
        ref_date = reference_month or os.getenv("REFERENCE_DATE", datetime.date.today().isoformat())
        # Validate ref_date
        try:
            datetime.date.fromisoformat(ref_date)
        except Exception:
            ref_date = datetime.date.today().isoformat()
        upserted_count, snapshots_count = self._persist_records(list(extracted_projects.values()), ref_date)

        return {
            "status": "success",
            "pdf_path": pdf_path,
            "total_pages_scanned": total_pages - start_page,
            "projects_upserted": upserted_count,
            "snapshots_inserted": snapshots_count,
            "warnings": warnings,
        }

    def _persist_records(self, projects: List[Dict[str, Any]], ref_date: str) -> tuple:
        if not projects:
            return 0, 0
        conn = self._get_connection()
        cur = conn.cursor()
        upserted = 0
        snapshots = 0

        for p in projects:
            cur.execute("""
                INSERT INTO projects (
                    project_id, project_name, ministry, sector, implementing_agency,
                    state, approved_cost_cr, revised_cost_cr, cumulative_expenditure_cr,
                    approval_date, scheduled_start, scheduled_completion, revised_completion,
                    physical_progress_pct, status, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(project_id) DO UPDATE SET
                    project_name=excluded.project_name, ministry=excluded.ministry,
                    sector=excluded.sector, revised_cost_cr=excluded.revised_cost_cr,
                    cumulative_expenditure_cr=excluded.cumulative_expenditure_cr,
                    physical_progress_pct=excluded.physical_progress_pct,
                    status=excluded.status, updated_at=CURRENT_TIMESTAMP
            """, (
                p['project_id'], p['project_name'], p['ministry'], p['sector'],
                p['implementing_agency'], p['state'], p['approved_cost_cr'],
                p['revised_cost_cr'], p['cumulative_expenditure_cr'],
                p['approval_date'], p['scheduled_start'], p['scheduled_completion'],
                p['revised_completion'], p['physical_progress_pct'], p['status']
            ))
            upserted += 1

            cur.execute("""
                INSERT OR REPLACE INTO monthly_snapshots (
                    project_id, snapshot_month, revised_cost_cr,
                    cumulative_expenditure_cr, physical_progress_pct, status
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                p['project_id'], ref_date, p['revised_cost_cr'],
                p['cumulative_expenditure_cr'], p['physical_progress_pct'], p['status']
            ))
            snapshots += 1

        conn.commit()
        conn.close()
        return upserted, snapshots


def ingest_pdf_file(pdf_path: str, db_path: str = "paimana.db", reference_month: Optional[str] = None) -> Dict[str, Any]:
    engine = MoSPIIngestionEngine(db_path=db_path)
    return engine.ingest(pdf_path, reference_month=reference_month)
