"""
Unit Tests: Ministry & Sector Resolver
Verifies robust heuristic resolution, word boundaries, and explicit preservation.
"""

import pytest
from src.etl.cuf.ministry_resolver import resolve_ministry_and_sector, clean_text


def test_clean_text():
    assert clean_text(None) == ""
    assert clean_text("") == ""
    assert clean_text("nan") == ""
    assert clean_text("None") == ""
    assert clean_text("null") == ""
    assert clean_text("N/A") == ""
    assert clean_text("  Valid Text  ") == "Valid Text"


def test_resolve_exact_ministry():
    min_name, sector = resolve_ministry_and_sector("Ministry of Railways", None)
    assert min_name == "Ministry of Railways"
    assert sector == "Railways"


def test_resolve_ministry_alias():
    min_name, sector = resolve_ministry_and_sector("morth", None)
    assert min_name == "Ministry of Road Transport and Highways"
    assert sector == "Road Transport & Highways"

    min_name2, sector2 = resolve_ministry_and_sector("mohua", None)
    assert min_name2 == "Ministry of Housing and Urban Affairs"
    assert sector2 == "Urban Metro & Transit Systems"


def test_resolve_by_sector():
    min_name, sector = resolve_ministry_and_sector(None, "Coal Mining")
    assert min_name == "Ministry of Coal"
    assert "Coal" in sector


def test_resolve_by_agency():
    min_name, sector = resolve_ministry_and_sector(None, None, agency_raw="NHAI")
    assert min_name == "Ministry of Road Transport and Highways"

    min_name2, _ = resolve_ministry_and_sector(None, None, agency_raw="RVNL")
    assert min_name2 == "Ministry of Railways"

    min_name3, _ = resolve_ministry_and_sector(None, None, agency_raw="IOCL")
    assert min_name3 == "Ministry of Petroleum and Natural Gas"


def test_resolve_by_project_name_keywords():
    min_name, _ = resolve_ministry_and_sector(None, None, project_name="Vande Bharat Train Maintenance Shed")
    assert min_name == "Ministry of Railways"

    min_name2, _ = resolve_ministry_and_sector(None, None, project_name="National Expressway 4-Laning Package 1")
    assert min_name2 == "Ministry of Road Transport and Highways"


def test_fallback_graceful():
    min_name, sector = resolve_ministry_and_sector(None, None, project_name="Random Mystery Gizmo")
    assert "Ministry of Statistics and Programme Implementation" in min_name
    assert sector == "Central Infrastructure"


def test_no_overwrite_custom_ministry():
    # Explicit custom ministries must never be overwritten by heuristic guesses
    min_name, _ = resolve_ministry_and_sector("Ministry of Ayush", None, project_name="Power Grid Substation Facility")
    assert min_name == "Ministry of Ayush"


def test_word_boundary_empowerment():
    # 'empowerment' must not false-match 'power'
    min_name, _ = resolve_ministry_and_sector("Ministry of Social Justice and Empowerment", None)
    assert min_name == "Ministry of Social Justice and Empowerment"
    assert min_name != "Ministry of Power"


def test_word_boundary_broadband():
    # 'broadband' must not false-match 'road'
    min_name, _ = resolve_ministry_and_sector(None, "National Broadband Optical Fibre Mission")
    assert min_name == "Ministry of Communications"
    assert min_name != "Ministry of Road Transport and Highways"


def test_solar_power_precedence():
    # 'solar power' must match MNRE, not Ministry of Power
    min_name, _ = resolve_ministry_and_sector(None, "Solar Power Generation")
    assert min_name == "Ministry of New and Renewable Energy"


def test_renewable_energy_alias_precedence():
    # Multi-word alias 'renewable energy' must match before single word 'energy'
    min_name, _ = resolve_ministry_and_sector("Department of New and Renewable Energy", None)
    assert min_name == "Ministry of New and Renewable Energy"
    assert min_name != "Ministry of Power"
