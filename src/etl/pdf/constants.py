"""
MoSPI PDF Ingestion Constants & Mappings
"""

import re
from typing import Dict

_SKIP_KEYWORDS = (
    "total", "sub-total", "sector overview", "all ongoing",
    "grand total", "ministry total", "sector total", "overall"
)

_CODE_RE = re.compile(r'[\(\[]\s*(\d{5,8})\s*[\)\]]')
_NUMERIC_CLEAN_RE = re.compile(r'[^\d.]')

SECTOR_TO_MINISTRY_MAP: Dict[str, str] = {
    "Road Transport & Highways": "Ministry of Road Transport and Highways (MoRTH)",
    "Railways": "Ministry of Railways (MoR)",
    "Thermal Power Generation": "Ministry of Power (MoP)",
    "Hydroelectric Power": "Ministry of Power (MoP)",
    "Petroleum & Natural Gas Pipelines": "Ministry of Petroleum and Natural Gas (MoPNG)",
    "Coal": "Ministry of Coal (MoC)",
    "Steel": "Ministry of Steel (MoS)",
    "Urban Metro & Transit Systems": "Ministry of Housing and Urban Affairs (MoHUA)",
    "Ports & Maritime Infrastructure": "Ministry of Ports, Shipping and Waterways (MoPSW)",
    "Civil Aviation & Airports": "Ministry of Civil Aviation (MoCA)",
    "Telecommunications & Optical Fibre": "Ministry of Communications",
    "Water Resources": "Ministry of Jal Shakti",
    "Renewable Energy (Solar/Wind)": "Ministry of New and Renewable Energy (MNRE)",
    "Defence Infrastructure & Strategic Roads": "Ministry of Defence",
    "Tourism, Hospitality & Wellness": "Ministry of Tourism",
}

MINISTRY_CANONICAL_MAP: Dict[str, str] = {
    "Ministry of Road Transport & Highways": "Ministry of Road Transport and Highways",
    "Ministry of Road Transport and Highways (MoRTH)": "Ministry of Road Transport and Highways",
    "Ministry of Petroleum & Natural Gas": "Ministry of Petroleum and Natural Gas",
    "Ministry of Petroleum and Natural Gas (MoPNG)": "Ministry of Petroleum and Natural Gas",
    "Ministry of Housing & Urban Affairs": "Ministry of Housing and Urban Affairs",
    "Ministry of Housing and Urban Affairs (MoHUA)": "Ministry of Housing and Urban Affairs",
    "Ministry of Health & Family Welfare": "Ministry of Health and Family Welfare",
    "Department of Water Resources, River Development & GR": "Department of Water Resources, River Development and GR",
    "Department for Promotion of Industry & Internal Trade": "Department for Promotion of Industry and Trade",
    "Ministry of Power (MoP)": "Ministry of Power",
    "Ministry of Railways (MoR)": "Ministry of Railways",
    "Ministry of Ports, Shipping and Waterways (MoPSW)": "Ministry of Ports, Shipping and Waterways",
    "Ministry of Civil Aviation (MoCA)": "Ministry of Civil Aviation",
    "Ministry of Communications": "Department of Telecommunications",
}

KNOWN_MINISTRIES = [
    "Ministry of Road Transport and Highways", "Ministry of Railways", "Ministry of Power",
    "Ministry of Petroleum and Natural Gas", "Ministry of Coal", "Ministry of Housing and Urban Affairs",
    "Ministry of Civil Aviation", "Ministry of Steel", "Ministry of Health and Family Welfare",
    "Department of Higher Education", "Department of Telecommunications", "Department of Water Resources",
    "Department for Promotion of Industry and Trade", "Ministry of Mines",
    "Ministry of Ports, Shipping and Waterways", "Ministry of Labour and Employment",
    "Department of Sports", "Ministry of New and Renewable Energy", "Ministry of Defence",
]
