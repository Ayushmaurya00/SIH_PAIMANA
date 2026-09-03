"""
Project Naming Conventions & Risk Modifiers
"""

import random
from src.data_gen.constants import STATES_LIST

SECTOR_RISK_MODIFIER = {
    "Hydroelectric Power": 0.40, "Urban Metro & Transit Systems": 0.36, "Atomic Energy & Nuclear Plants": 0.35,
    "Water Resources & Irrigation": 0.32, "Railways": 0.26, "Defence Infrastructure & Strategic Roads": 0.22,
    "Thermal Power Generation": 0.16, "Mining & Mineral Processing": 0.15, "Coal Mining & Infrastructure": 0.14,
    "Steel & Metallurgy": 0.12, "Road Transport & Highways": 0.10, "Ports & Maritime Infrastructure": 0.08,
    "Urban Infrastructure & Water Supply": 0.08, "Petroleum & Natural Gas Pipelines": 0.06,
    "Fertilizer Plants & Petrochemicals": 0.05, "Heavy Engineering & Equipment": 0.04,
    "Oil Refineries & Petrochemicals": 0.02, "Inland Waterways": 0.00, "Civil Aviation & Airports": -0.08,
    "Telecommunications & Optical Fibre": -0.15, "Power Transmission & Distribution": -0.12,
    "Renewable Energy (Solar/Wind)": -0.22
}

AGENCY_RISK_MODIFIER = {
    "PGCIL": -0.16, "SECI": -0.15, "DMRC": -0.12, "NTPC": -0.12, "IOCL": -0.10, "AAI": -0.08,
    "NHAI": 0.02, "GAIL": 0.00, "BPCL": -0.02, "HPCL": -0.02, "SAIL": 0.04, "BHEL": 0.06, "IRCON": 0.04,
    "BRO": 0.15, "NHIDCL": 0.22, "RVNL": 0.18, "State PWD": 0.28, "State Irrigation Dept": 0.30,
    "State Urban Dev Auth": 0.20, "BSNL": 0.25, "Coal India (CIL)": 0.12, "NPCIL": 0.20, "NHPC": 0.25
}

STATE_TERRAIN_MODIFIER = {
    "Jammu & Kashmir": 0.24, "Himachal Pradesh": 0.20, "Uttarakhand": 0.22, "Arunachal Pradesh": 0.28,
    "Assam": 0.16, "Meghalaya": 0.20, "Manipur": 0.25, "Nagaland": 0.26, "Mizoram": 0.24, "Sikkim": 0.22,
    "Tripura": 0.18, "Ladakh": 0.30, "West Bengal": 0.18, "Bihar": 0.16, "Kerala": 0.18, "Tamil Nadu": 0.05,
    "Gujarat": -0.10, "Maharashtra": -0.04, "Karnataka": -0.02, "Telangana": -0.06, "Andhra Pradesh": -0.04,
    "Madhya Pradesh": -0.02, "Rajasthan": 0.00, "Uttar Pradesh": 0.02, "Odisha": 0.06, "Jharkhand": 0.10,
    "Chhattisgarh": 0.08, "Punjab": 0.00, "Haryana": -0.02, "Goa": 0.04, "Delhi": -0.02
}

INDIAN_STATES = list(STATE_TERRAIN_MODIFIER.keys())

MILESTONE_TEMPLATES = {
    "Road Transport & Highways": [
        "Land Acquisition & 3D Notification (90% RoW)", "Forest & Environmental Clearance",
        "EPC / HAM Contract Award & Financial Close", "Earthwork, Embankment & Subgrade Completion",
        "Major Bridges & Flyover Structures Erection", "Bituminous Pavement, Signage & Final COD"
    ],
    "Railways": [
        "Detailed Alignment Survey & RoW Acquisition", "Forest & Railway Board Sanction",
        "Tendering & Major Civil Contract Award", "Earthwork, Tunnels & Bridge Abutments",
        "Track Laying & 25kV OHE Electrification", "Signalling (Kavach) & CRS Safety Inspection"
    ],
    "Urban Metro & Transit Systems": [
        "Land & Depot Acquisition Approval", "Utility Shifting & Tree Clearance",
        "Viaduct Pier Construction & TBM Tunneling", "Underground / Elevated Stations Civil Structure",
        "Third Rail / OHE & CBTC Signalling", "Rolling Stock Trials & CMRS Certification"
    ],
    "Hydroelectric Power": [
        "Stage-II Forest Clearance & R&R Settlement", "River Diversion & Coffer Dam Construction",
        "Head Race Tunnel (HRT) Excavation", "Main Dam Concrete Placement / Embankment",
        "Turbine & Generator Assembly Erection", "Reservoir Impoundment & Grid Synchronization"
    ],
    "Atomic Energy & Nuclear Plants": [
        "AERB Site Clearance & Environmental Approval", "First Pour of Concrete (FPC) Milestone",
        "Reactor Building Inner Containment Dome", "Reactor Pressure Vessel & Steam Generator Installation",
        "Secondary Piping, Turbine & Grid Interface", "AERB Fuel Loading Permission & Full Power COD"
    ],
    "Renewable Energy (Solar/Wind)": [
        "Solar Park / Land Lease Execution", "Grid Connectivity & PPA Execution",
        "Module Mounting Structures & Inverter Civil Work", "Solar PV Module / WTG Erection",
        "Transmission Line to Pooling Substation", "RLDC Charging & Commercial Operation Declaration"
    ],
    "Generic": [
        "Statutory Approvals & Land Possession", "Engineering Design & EPC Contract Award",
        "Civil Works Foundation & Substructure", "Main Equipment Supply & Installation",
        "Piping, Cabling & Auxiliary Works", "Pre-commissioning, Testing & Final Handover"
    ]
}

INDIAN_CITIES = [
    "Nagpur", "Varanasi", "Ahmedabad", "Bengaluru", "Hyderabad", "Kolkata", "Patna",
    "Pune", "Jaipur", "Lucknow", "Bhubaneswar", "Ranchi", "Guwahati", "Kochi",
    "Visakhapatnam", "Surat", "Indore", "Bhopal", "Chandigarh", "Shimla", "Dehradun",
    "Raipur", "Mangaluru", "Jammu", "Srinagar", "Agartala", "Imphal", "Shillong"
]


def generate_realistic_project_name(sector: str, state: str, idx: int) -> str:
    city = random.choice(INDIAN_CITIES)
    phase = random.choice(["Phase-I", "Phase-II", "Phase-III", "Package 1", "Package 2", "Stage-I", "Stage-II"])
    prefix_map = {
        "Road Transport & Highways": f"4-Laning of NH-{random.randint(11, 99)} ({city}-{state}) - {phase}",
        "Railways": f"Railway Doubling & Electrification near {city} ({state}) - {phase}",
        "Urban Metro & Transit Systems": f"{city} Metro Rail Corridor ({phase})",
        "Civil Aviation & Airports": f"New Terminal Building at {city} Airport, {state}",
        "Hydroelectric Power": f"{city} Hydroelectric Project (HEP) Stage-{random.randint(1, 3)} ({state})"
    }
    return prefix_map.get(sector, f"{sector} Project at {city}, {state} ({phase})")
