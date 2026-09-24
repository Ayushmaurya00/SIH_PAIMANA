"""
PDF Data Cleaning & Sanitization Utilities
"""

import re
import datetime
from typing import Any, Optional
from src.etl.pdf.constants import (
    _SKIP_KEYWORDS, _CODE_RE, MINISTRY_CANONICAL_MAP
)


def canonicalise_ministry(name: str) -> str:
    """Return the single authoritative name for any ministry variant spelling."""
    return MINISTRY_CANONICAL_MAP.get(name, name)


def infer_ministry_and_sector(project_name: str, current_min: str, current_sec: str) -> tuple:
    name_lower = project_name.lower()
    if any(k in name_lower for k in ["railway", "nfr", "ecr", "scr", "wr", "dfccil", "ircon", "rvnl"]):
        return "Ministry of Railways", "Railways"
    if any(k in name_lower for k in ["road", "highway", "nhai", "nhidcl", "bypass", "4-lane", "6-lane", "bridge"]):
        return "Ministry of Road Transport and Highways", "Road Transport & Highways"
    if any(k in name_lower for k in ["power", "ntpc", "nhpc", "transmission", "electricity"]):
        return "Ministry of Power", "Power Generation & Transmission"
    if any(k in name_lower for k in ["coal", "mining", "ccl", "bccl", "ncl", "wcl"]):
        return "Ministry of Coal", "Coal"
    if any(k in name_lower for k in ["petroleum", "gas", "pipeline", "iocl", "bpcl", "hpcl", "ongc"]):
        return "Ministry of Petroleum and Natural Gas", "Petroleum & Natural Gas"
    if any(k in name_lower for k in ["steel", "sail", "rinl"]):
        return "Ministry of Steel", "Steel"
    if any(k in name_lower for k in ["metro", "urban transit", "mrtc"]):
        return "Ministry of Housing and Urban Affairs", "Urban Metro & Transit Systems"
    if any(k in name_lower for k in ["airport", "aviation", "aai"]):
        return "Ministry of Civil Aviation", "Civil Aviation & Airports"
    return current_min, current_sec


def is_skip_row(text: str) -> bool:
    t = text.lower().strip()
    return any(kw in t for kw in _SKIP_KEYWORDS)


def extract_project_code(text: str) -> Optional[str]:
    m = _CODE_RE.search(text)
    return f"PRJ-{m.group(1)}" if m else None


def clean_project_name(raw: str) -> str:
    name = re.sub(r'[\(\[]\s*\d{5,8}\s*[\)\]]', '', str(raw)).strip()
    name = re.sub(r'\s*\([^\)]*\)\s*\(-\)\s*\(-\)\s*$', '', name)
    name = re.sub(r'\s*\(-\)\s*\(-\)\s*$', '', name)
    name = re.sub(r'\s*\n\s*', ' ', name)
    name = re.sub(r'\s{2,}', ' ', name)
    return name.strip() or "Unnamed Project"


def parse_float(val: Any, default: float = 0.0) -> float:
    if val is None:
        return default
    s = str(val).strip()
    if not s or s in ('-', '\u2014', 'N/A', 'NA', 'nil', 'Nil'):
        return default
    cleaned = re.sub(r'[^\d.]', '', s.replace(',', ''))
    try:
        return float(cleaned) if cleaned else default
    except (ValueError, TypeError):
        return default


def clean_state(val: Any) -> str:
    if val is None:
        return "National"
    s = str(val).strip()
    if not s or s.lower() in ('-', '\u2014', 'na', 'n/a', 'national', 'nil'):
        return "National"
    return s


def normalise_date(raw: str) -> Optional[str]:
    if not raw:
        return None
    raw = raw.strip()
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', raw):
        return raw
    m = re.fullmatch(r'(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})', raw)
    if m:
        return f"{m.group(3)}-{m.group(2).zfill(2)}-{m.group(1).zfill(2)}"
    m2 = re.fullmatch(r'(\d{1,2})[/\-](\d{4})', raw)
    if m2:
        return f"{m2.group(2)}-{m2.group(1).zfill(2)}-01"
    return None


def derive_status(progress: float, revised_completion: str, ref_date: datetime.date | str | None = None) -> str:
    if progress >= 99.0:
        return "Completed"
    if progress < 60.0:
        return "Delayed"
    # Use ref_date for deterministic status (avoid today() at parse time)
    if ref_date is None:
        import os
        ref_date = os.getenv("REFERENCE_DATE", "2026-08-01")
    if isinstance(ref_date, str):
        try:
            ref_date_obj = datetime.date.fromisoformat(ref_date)
        except Exception:
            ref_date_obj = datetime.date.today()
    else:
        ref_date_obj = ref_date
    try:
        rc_date = datetime.date.fromisoformat(revised_completion) if isinstance(revised_completion, str) else revised_completion
        if isinstance(rc_date, datetime.datetime):
            rc_date = rc_date.date()
        if rc_date and rc_date < ref_date_obj:
            return "Delayed"
    except (ValueError, TypeError):
        pass
    return "On Track"
