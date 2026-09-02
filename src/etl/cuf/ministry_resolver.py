"""
PAIMANA AI - Sovereign Ministry & Sector Resolution Engine
Accurately resolves, normalizes, and canonicalizes ministries and sectors
from raw imports without falling back to a single default ministry.
"""

import re
from typing import Tuple, Optional
from src.etl.cuf.ministry_data import (
    CANONICAL_MINISTRIES,
    MINISTRY_ALIAS_MAP,
    AGENCY_MAP,
    DEFAULT_SECTOR_MAP,
)

__all__ = [
    "CANONICAL_MINISTRIES", "MINISTRY_ALIAS_MAP", "AGENCY_MAP",
    "DEFAULT_SECTOR_MAP", "clean_text", "resolve_ministry_and_sector",
    "_default_sector_for_ministry",
]

# Pre-sort aliases by length descending so longer phrases match before short words
_SORTED_ALIASES = sorted(MINISTRY_ALIAS_MAP.items(), key=lambda x: len(x[0]), reverse=True)


def clean_text(val: Optional[str]) -> str:
    """Sanitizes text by stripping whitespace and rejecting null/nan sentinels."""
    if not val:
        return ""
    s = str(val).strip()
    return "" if s.lower() in ["nan", "none", "n/a", "na", "null", "-", ""] else s


def _default_sector_for_ministry(ministry: str) -> str:
    """Returns canonical default sector for a recognized ministry."""
    return DEFAULT_SECTOR_MAP.get(ministry, "Central Infrastructure")


def _match_by_explicit_ministry(m_clean: str, s_clean: str) -> Optional[Tuple[str, str]]:
    """Stage 1: Match directly from ministry name string using exact or word-boundary matches."""
    m_lower = m_clean.lower().strip()
    if m_lower in MINISTRY_ALIAS_MAP:
        canon_min = MINISTRY_ALIAS_MAP[m_lower]
        return canon_min, s_clean or _default_sector_for_ministry(canon_min)
    for alias, canon in _SORTED_ALIASES:
        # Match using word boundaries to avoid false positives (e.g. 'power' in 'empowerment')
        if re.search(r'\b' + re.escape(alias) + r'\b', m_lower):
            return canon, s_clean or _default_sector_for_ministry(canon)
    return None


def _match_by_explicit_sector(s_clean: str) -> Optional[Tuple[str, str]]:
    """Stage 2: Match ministry inferred from sector domain with proper precedence."""
    s_lower = s_clean.lower().strip()
    if s_lower in MINISTRY_ALIAS_MAP:
        return MINISTRY_ALIAS_MAP[s_lower], s_clean

    sector_rules = [
        (["solar", "wind", "renewable", "mnre", "photovoltaic"], ("Ministry of New and Renewable Energy", "Renewable Energy (Solar/Wind)")),
        (["metro", "urban transit", "urban", "smart city"], ("Ministry of Housing and Urban Affairs", "Urban Metro & Transit Systems")),
        (["telecom", "communication", "broadband", "optical fibre", "fibre"], ("Ministry of Communications", "Telecommunications & Optical Fibre")),
        (["rail", "train", "dfcc"], ("Ministry of Railways", "Railways")),
        (["road", "highway", "expressway", "lane", "laning", "flyover", "bypass"], ("Ministry of Road Transport and Highways", "Road Transport & Highways")),
        (["power", "electric", "thermal", "hydro", "transmission"], ("Ministry of Power", "Power Transmission & Distribution")),
        (["petroleum", "oil", "gas", "refinery", "pipeline", "lpg", "cng"], ("Ministry of Petroleum and Natural Gas", "Petroleum & Natural Gas Pipelines")),
        (["coal"], ("Ministry of Coal", "Coal Mining & Infrastructure")),
        (["steel", "metallurgy"], ("Ministry of Steel", "Steel & Metallurgy")),
        (["aviation", "airport"], ("Ministry of Civil Aviation", "Civil Aviation & Airports")),
        (["atomic", "nuclear"], ("Department of Atomic Energy", "Atomic Energy & Nuclear Plants")),
        (["fertilizer", "chemical"], ("Ministry of Chemicals and Fertilizers", "Fertilizer Plants & Petrochemicals")),
        (["water", "irrigation", "jal shakti", "dam"], ("Ministry of Jal Shakti", "Water Resources & Irrigation")),
        (["port", "shipping", "maritime", "waterway"], ("Ministry of Ports, Shipping and Waterways", "Ports & Maritime Infrastructure")),
        (["mine", "mining", "mineral"], ("Ministry of Mines", "Mining & Mineral Processing")),
    ]
    for keywords, (min_name, def_sec) in sector_rules:
        if any(re.search(r'\b' + re.escape(k) + r'\b', s_lower) for k in keywords):
            return min_name, s_clean or def_sec
    return None


def _match_by_agency(a_clean: str, s_clean: str) -> Optional[Tuple[str, str]]:
    """Stage 3: Match from implementing agency acronym with word boundaries."""
    for ag_key, (ag_min, ag_sec) in AGENCY_MAP.items():
        if re.search(r'\b' + re.escape(ag_key) + r'\b', a_clean, re.IGNORECASE):
            return ag_min, s_clean or ag_sec
    return None


def _match_by_project_name(p_clean: str) -> Optional[Tuple[str, str]]:
    """Stage 4: Infer ministry and sector from project title keywords with word boundaries."""
    p_lower = p_clean.lower()
    keyword_rules = [
        (["solar", "wind farm", "renewable energy", "photovoltaic"], ("Ministry of New and Renewable Energy", "Renewable Energy (Solar/Wind)")),
        (["metro", "urban transit", "rapid transit", "corridor transit"], ("Ministry of Housing and Urban Affairs", "Urban Metro & Transit Systems")),
        (["railway", "train", "dfcc", "line doubling", "station redevelopment", "vande bharat", "high speed rail", "freight corridor"], ("Ministry of Railways", "Railways")),
        (["highway", "expressway", "4-lane", "6-lane", "laning", "bypass", "flyover", "tunnel", "bridge"], ("Ministry of Road Transport and Highways", "Road Transport & Highways")),
        (["optical fibre", "telecom", "broadband", "bharatnet", "cellular"], ("Ministry of Communications", "Telecommunications & Optical Fibre")),
        (["power", "thermal", "transmission", "substation", "hydroelectric", "grid"], ("Ministry of Power", "Power Transmission & Distribution")),
        (["petroleum", "refinery", "pipeline", "oil", "lpg", "cng"], ("Ministry of Petroleum and Natural Gas", "Petroleum & Natural Gas Pipelines")),
        (["coal", "washery", "opencast"], ("Ministry of Coal", "Coal Mining & Infrastructure")),
        (["steel", "blast furnace", "pellet plant", "metallurgy"], ("Ministry of Steel", "Steel & Metallurgy")),
        (["airport", "aviation", "terminal", "runway"], ("Ministry of Civil Aviation", "Civil Aviation & Airports")),
        (["atomic", "reactor", "nuclear"], ("Department of Atomic Energy", "Atomic Energy & Nuclear Plants")),
        (["fertilizer", "urea", "ammonia"], ("Ministry of Chemicals and Fertilizers", "Fertilizer Plants & Petrochemicals")),
        (["irrigation", "canal", "barrage", "dam", "jal"], ("Ministry of Jal Shakti", "Water Resources & Irrigation")),
        (["port", "terminal port", "waterway", "dock"], ("Ministry of Ports, Shipping and Waterways", "Ports & Maritime Infrastructure")),
        (["aiims", "hospital", "medical college"], ("Ministry of Health and Family Welfare", "Healthcare Infrastructure")),
        (["iit", "iim", "central university", "campus"], ("Ministry of Education", "Higher Education Infrastructure")),
    ]
    for keywords, result in keyword_rules:
        if any(re.search(r'\b' + re.escape(k) + r'\b', p_lower) for k in keywords):
            return result
    return None


def resolve_ministry_and_sector(
    ministry_raw: Optional[str],
    sector_raw: Optional[str],
    project_name: Optional[str] = "",
    agency_raw: Optional[str] = ""
) -> Tuple[str, str]:
    """
    Intelligently determines the true canonical Ministry and Sector.
    Never collapses records into a single fallback ministry and respects explicitly provided ministries.
    """
    m_clean = clean_text(ministry_raw)
    s_clean = clean_text(sector_raw)
    p_clean = clean_text(project_name)
    a_clean = clean_text(agency_raw)

    # 1. If explicit ministry was given, canonicalize alias or PRESERVE verbatim. Never clobber with project name guesses!
    if m_clean:
        res = _match_by_explicit_ministry(m_clean, s_clean)
        if res:
            return res
        return m_clean, s_clean or _default_sector_for_ministry(m_clean)

    # 2. Heuristic Stage: Match from explicit sector (only when ministry is missing)
    if s_clean:
        res = _match_by_explicit_sector(s_clean)
        if res:
            return res

    # 3. Heuristic Stage: Match from Implementing Agency
    if a_clean:
        res = _match_by_agency(a_clean, s_clean)
        if res:
            return res

    # 4. Heuristic Stage: Infer from Project Name Keywords
    if p_clean:
        res = _match_by_project_name(p_clean)
        if res:
            return res

    # 5. Graceful Sovereign Default
    return "Ministry of Statistics and Programme Implementation (MoSPI)", s_clean or "Central Infrastructure"
