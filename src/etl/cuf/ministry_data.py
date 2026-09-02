"""
PAIMANA AI - Authoritative Sovereign Ministries & Agency Mappings
Reference metadata dictionaries used by the CUF resolver.
"""

CANONICAL_MINISTRIES = [
    "Ministry of Road Transport and Highways", "Ministry of Railways", "Ministry of Power",
    "Ministry of Petroleum and Natural Gas", "Ministry of Coal", "Ministry of Housing and Urban Affairs",
    "Ministry of Civil Aviation", "Ministry of Steel", "Department of Atomic Energy",
    "Ministry of Chemicals and Fertilizers", "Ministry of Jal Shakti", "Ministry of Communications",
    "Ministry of Mines", "Ministry of Ports, Shipping and Waterways", "Ministry of Health and Family Welfare",
    "Ministry of New and Renewable Energy", "Ministry of Defence", "Ministry of Heavy Industries",
    "Ministry of Education", "Ministry of Commerce and Industry", "Ministry of Tourism",
    "Ministry of Statistics and Programme Implementation (MoSPI)"
]

MINISTRY_ALIAS_MAP = {
    # Road Transport
    "road transport": "Ministry of Road Transport and Highways", "morth": "Ministry of Road Transport and Highways",
    "roadways": "Ministry of Road Transport and Highways", "highways": "Ministry of Road Transport and Highways",
    "ministry of road transport": "Ministry of Road Transport and Highways",
    "ministry of road transport & highways": "Ministry of Road Transport and Highways",
    "ministry of road transport and highways": "Ministry of Road Transport and Highways",
    "ministry of road transport and highways (morth)": "Ministry of Road Transport and Highways",
    # Railways
    "railways": "Ministry of Railways", "railway": "Ministry of Railways", "mor": "Ministry of Railways",
    "ministry of railways": "Ministry of Railways", "ministry of railways (mor)": "Ministry of Railways",
    # Power
    "power": "Ministry of Power", "mop": "Ministry of Power", "electricity": "Ministry of Power",
    "ministry of power": "Ministry of Power", "ministry of power (mop)": "Ministry of Power",
    # Petroleum & Natural Gas
    "petroleum": "Ministry of Petroleum and Natural Gas", "mopng": "Ministry of Petroleum and Natural Gas",
    "oil & gas": "Ministry of Petroleum and Natural Gas", "oil and gas": "Ministry of Petroleum and Natural Gas",
    "ministry of petroleum": "Ministry of Petroleum and Natural Gas",
    "ministry of petroleum & natural gas": "Ministry of Petroleum and Natural Gas",
    "ministry of petroleum and natural gas": "Ministry of Petroleum and Natural Gas",
    "ministry of petroleum and natural gas (mopng)": "Ministry of Petroleum and Natural Gas",
    # Coal
    "coal": "Ministry of Coal", "moc": "Ministry of Coal",
    "ministry of coal": "Ministry of Coal", "ministry of coal (moc)": "Ministry of Coal",
    # Housing & Urban
    "housing": "Ministry of Housing and Urban Affairs", "mohua": "Ministry of Housing and Urban Affairs",
    "urban transit": "Ministry of Housing and Urban Affairs", "urban affairs": "Ministry of Housing and Urban Affairs",
    "urban infrastructure": "Ministry of Housing and Urban Affairs",
    "ministry of housing": "Ministry of Housing and Urban Affairs",
    "ministry of housing & urban": "Ministry of Housing and Urban Affairs",
    "ministry of housing & urban affairs": "Ministry of Housing and Urban Affairs",
    "ministry of housing and urban affairs": "Ministry of Housing and Urban Affairs",
    "ministry of housing and urban affairs (mohua)": "Ministry of Housing and Urban Affairs",
    # Civil Aviation
    "civil aviation": "Ministry of Civil Aviation", "aviation": "Ministry of Civil Aviation", "moca": "Ministry of Civil Aviation",
    "ministry of civil aviation": "Ministry of Civil Aviation", "ministry of civil aviation (moca)": "Ministry of Civil Aviation",
    # Steel
    "steel": "Ministry of Steel", "mos": "Ministry of Steel", "metallurgy": "Ministry of Steel",
    "ministry of steel": "Ministry of Steel", "ministry of steel (mos)": "Ministry of Steel",
    # Atomic Energy
    "atomic energy": "Department of Atomic Energy", "dae": "Department of Atomic Energy", "nuclear": "Department of Atomic Energy",
    "department of atomic energy": "Department of Atomic Energy", "department of atomic energy (dae)": "Department of Atomic Energy",
    # Chemicals & Fertilizers
    "chemicals": "Ministry of Chemicals and Fertilizers", "fertilizers": "Ministry of Chemicals and Fertilizers",
    "ministry of chemicals": "Ministry of Chemicals and Fertilizers",
    "ministry of chemicals & fertilizers": "Ministry of Chemicals and Fertilizers",
    "ministry of chemicals and fertilizers": "Ministry of Chemicals and Fertilizers",
    # Jal Shakti / Water Resources
    "jal shakti": "Ministry of Jal Shakti", "water resources": "Ministry of Jal Shakti", "irrigation": "Ministry of Jal Shakti",
    "ministry of jal shakti": "Ministry of Jal Shakti", "department of water resources": "Ministry of Jal Shakti",
    "department of water resources, river development and gr": "Ministry of Jal Shakti",
    # Communications
    "communications": "Ministry of Communications", "telecommunications": "Ministry of Communications",
    "telecom": "Ministry of Communications", "dot": "Ministry of Communications",
    "department of telecommunications": "Ministry of Communications", "ministry of communications": "Ministry of Communications",
    # Mines
    "mines": "Ministry of Mines", "mining": "Ministry of Mines", "ministry of mines": "Ministry of Mines",
    # Ports & Shipping
    "ports": "Ministry of Ports, Shipping and Waterways", "shipping": "Ministry of Ports, Shipping and Waterways",
    "mopsw": "Ministry of Ports, Shipping and Waterways", "waterways": "Ministry of Ports, Shipping and Waterways",
    "ministry of ports": "Ministry of Ports, Shipping and Waterways",
    "ministry of ports, shipping & waterways": "Ministry of Ports, Shipping and Waterways",
    "ministry of ports, shipping and waterways": "Ministry of Ports, Shipping and Waterways",
    "ministry of ports, shipping and waterways (mopsw)": "Ministry of Ports, Shipping and Waterways",
    # Renewable Energy
    "renewable energy": "Ministry of New and Renewable Energy", "mnre": "Ministry of New and Renewable Energy",
    "new and renewable energy": "Ministry of New and Renewable Energy",
    "ministry of new and renewable energy": "Ministry of New and Renewable Energy",
    "ministry of new and renewable energy (mnre)": "Ministry of New and Renewable Energy",
    # Defence, Health, Heavy Industries, Education, Commerce, Tourism, MoSPI
    "defence": "Ministry of Defence", "defense": "Ministry of Defence", "ministry of defence": "Ministry of Defence",
    "health": "Ministry of Health and Family Welfare", "ministry of health": "Ministry of Health and Family Welfare",
    "ministry of health & family welfare": "Ministry of Health and Family Welfare",
    "ministry of health and family welfare": "Ministry of Health and Family Welfare",
    "heavy industries": "Ministry of Heavy Industries", "ministry of heavy industries": "Ministry of Heavy Industries",
    "education": "Ministry of Education", "ministry of education": "Ministry of Education",
    "commerce": "Ministry of Commerce and Industry", "ministry of commerce": "Ministry of Commerce and Industry",
    "ministry of commerce and industry": "Ministry of Commerce and Industry",
    "tourism": "Ministry of Tourism", "ministry of tourism": "Ministry of Tourism",
    "mospi": "Ministry of Statistics and Programme Implementation (MoSPI)",
    "ministry of statistics": "Ministry of Statistics and Programme Implementation (MoSPI)",
    "ministry of statistics and programme implementation": "Ministry of Statistics and Programme Implementation (MoSPI)",
    "ministry of statistics and programme implementation (mospi)": "Ministry of Statistics and Programme Implementation (MoSPI)"
}

AGENCY_MAP = {
    "nhai": ("Ministry of Road Transport and Highways", "Road Transport & Highways"),
    "nhidcl": ("Ministry of Road Transport and Highways", "Road Transport & Highways"),
    "morth": ("Ministry of Road Transport and Highways", "Road Transport & Highways"),
    "pwd": ("Ministry of Road Transport and Highways", "Road Transport & Highways"),
    "rvnl": ("Ministry of Railways", "Railways"), "dfccil": ("Ministry of Railways", "Railways"),
    "dfcc": ("Ministry of Railways", "Railways"), "ircon": ("Ministry of Railways", "Railways"),
    "krcl": ("Ministry of Railways", "Railways"), "nhsrcl": ("Ministry of Railways", "Railways"),
    "railnet": ("Ministry of Railways", "Railways"),
    "ntpc": ("Ministry of Power", "Power Transmission & Distribution"),
    "nhpc": ("Ministry of Power", "Power Transmission & Distribution"),
    "pgcil": ("Ministry of Power", "Power Transmission & Distribution"),
    "powergrid": ("Ministry of Power", "Power Transmission & Distribution"),
    "neepco": ("Ministry of Power", "Power Transmission & Distribution"),
    "iocl": ("Ministry of Petroleum and Natural Gas", "Petroleum & Natural Gas Pipelines"),
    "bpcl": ("Ministry of Petroleum and Natural Gas", "Petroleum & Natural Gas Pipelines"),
    "hpcl": ("Ministry of Petroleum and Natural Gas", "Petroleum & Natural Gas Pipelines"),
    "ongc": ("Ministry of Petroleum and Natural Gas", "Petroleum & Natural Gas Pipelines"),
    "gail": ("Ministry of Petroleum and Natural Gas", "Petroleum & Natural Gas Pipelines"),
    "ccl": ("Ministry of Coal", "Coal Mining & Infrastructure"),
    "bccl": ("Ministry of Coal", "Coal Mining & Infrastructure"),
    "ncl": ("Ministry of Coal", "Coal Mining & Infrastructure"),
    "secl": ("Ministry of Coal", "Coal Mining & Infrastructure"),
    "sccl": ("Ministry of Coal", "Coal Mining & Infrastructure"),
    "cil": ("Ministry of Coal", "Coal Mining & Infrastructure"),
    "sail": ("Ministry of Steel", "Steel & Metallurgy"),
    "rinl": ("Ministry of Steel", "Steel & Metallurgy"),
    "nmdc": ("Ministry of Steel", "Steel & Metallurgy"),
    "bmrcl": ("Ministry of Housing and Urban Affairs", "Urban Metro & Transit Systems"),
    "dmrc": ("Ministry of Housing and Urban Affairs", "Urban Metro & Transit Systems"),
    "kmrl": ("Ministry of Housing and Urban Affairs", "Urban Metro & Transit Systems"),
    "cmrl": ("Ministry of Housing and Urban Affairs", "Urban Metro & Transit Systems"),
    "upmrc": ("Ministry of Housing and Urban Affairs", "Urban Metro & Transit Systems"),
    "nbcc": ("Ministry of Housing and Urban Affairs", "Urban Metro & Transit Systems"),
    "cpwd": ("Ministry of Housing and Urban Affairs", "Urban Metro & Transit Systems"),
    "aai": ("Ministry of Civil Aviation", "Civil Aviation & Airports"),
    "npcil": ("Department of Atomic Energy", "Atomic Energy & Nuclear Plants"),
    "bhavini": ("Department of Atomic Energy", "Atomic Energy & Nuclear Plants"),
    "hurl": ("Ministry of Chemicals and Fertilizers", "Fertilizer Plants & Petrochemicals"),
    "tfl": ("Ministry of Chemicals and Fertilizers", "Fertilizer Plants & Petrochemicals"),
    "bvfcl": ("Ministry of Chemicals and Fertilizers", "Fertilizer Plants & Petrochemicals"),
    "ppa": ("Ministry of Jal Shakti", "Water Resources & Irrigation"),
    "cwc": ("Ministry of Jal Shakti", "Water Resources & Irrigation"),
    "bsnl": ("Ministry of Communications", "Telecommunications & Optical Fibre"),
    "mtnl": ("Ministry of Communications", "Telecommunications & Optical Fibre"),
    "jnpt": ("Ministry of Ports, Shipping and Waterways", "Ports & Maritime Infrastructure"),
    "iwai": ("Ministry of Ports, Shipping and Waterways", "Ports & Maritime Infrastructure")
}

DEFAULT_SECTOR_MAP = {
    "Ministry of Road Transport and Highways": "Road Transport & Highways",
    "Ministry of Railways": "Railways",
    "Ministry of Power": "Power Transmission & Distribution",
    "Ministry of Petroleum and Natural Gas": "Petroleum & Natural Gas Pipelines",
    "Ministry of Coal": "Coal Mining & Infrastructure",
    "Ministry of Housing and Urban Affairs": "Urban Metro & Transit Systems",
    "Ministry of Civil Aviation": "Civil Aviation & Airports",
    "Ministry of Steel": "Steel & Metallurgy",
    "Department of Atomic Energy": "Atomic Energy & Nuclear Plants",
    "Ministry of Chemicals and Fertilizers": "Fertilizer Plants & Petrochemicals",
    "Ministry of Jal Shakti": "Water Resources & Irrigation",
    "Ministry of Communications": "Telecommunications & Optical Fibre",
    "Ministry of Mines": "Mining & Mineral Processing",
    "Ministry of Ports, Shipping and Waterways": "Ports & Maritime Infrastructure",
    "Ministry of New and Renewable Energy": "Renewable Energy (Solar/Wind)",
    "Ministry of Defence": "Defence Infrastructure & Strategic Roads",
    "Ministry of Health and Family Welfare": "Healthcare Infrastructure",
    "Ministry of Heavy Industries": "Heavy Industries & Manufacturing",
    "Ministry of Education": "Higher Education Infrastructure",
    "Ministry of Commerce and Industry": "Industrial Corridors & Logistics",
    "Ministry of Tourism": "Tourism Infrastructure",
    "Ministry of Statistics and Programme Implementation (MoSPI)": "Central Infrastructure Monitoring",
}
