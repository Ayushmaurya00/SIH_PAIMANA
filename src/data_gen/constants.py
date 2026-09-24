"""
Domain Configurations: Ministries, Sectors, Implementing Agencies, States & Templates
"""

MINISTRY_SECTOR_MAP = {
    "Ministry of Road Transport and Highways (MoRTH)": ["Road Transport & Highways"],
    "Ministry of Railways (MoR)": ["Railways"],
    "Ministry of Power (MoP)": ["Power Transmission & Distribution", "Thermal Power Generation", "Hydroelectric Power"],
    "Ministry of Petroleum and Natural Gas (MoPNG)": ["Petroleum & Natural Gas Pipelines", "Oil Refineries & Petrochemicals"],
    "Ministry of Coal (MoC)": ["Coal Mining & Infrastructure"],
    "Ministry of Steel (MoS)": ["Steel & Metallurgy"],
    "Ministry of Housing and Urban Affairs (MoHUA)": ["Urban Metro & Transit Systems", "Urban Infrastructure & Water Supply"],
    "Ministry of Ports, Shipping and Waterways (MoPSW)": ["Ports & Maritime Infrastructure", "Inland Waterways"],
    "Ministry of Civil Aviation (MoCA)": ["Civil Aviation & Airports"],
    "Ministry of Communications": ["Telecommunications & Optical Fibre"],
    "Ministry of Mines": ["Mining & Mineral Processing"],
    "Ministry of Chemicals and Fertilizers": ["Fertilizer Plants & Petrochemicals"],
    "Ministry of Jal Shakti": ["Water Resources & Irrigation"],
    "Department of Atomic Energy (DAE)": ["Atomic Energy & Nuclear Plants"],
    "Ministry of New and Renewable Energy (MNRE)": ["Renewable Energy (Solar/Wind)"],
    "Ministry of Heavy Industries": ["Heavy Engineering & Equipment"],
    "Ministry of Defence": ["Defence Infrastructure & Strategic Roads"]
}

SECTOR_AGENCY_MAP = {
    "Road Transport & Highways": ["NHAI", "NHIDCL", "State PWD", "MoRTH Direct"],
    "Railways": ["RVNL", "IRCON", "DFCCIL", "Zonal Railways", "KRCL"],
    "Power Transmission & Distribution": ["PGCIL", "State Transco", "REC Power"],
    "Thermal Power Generation": ["NTPC", "DVC", "State Genco"],
    "Hydroelectric Power": ["NHPC", "SJVN", "NEEPCO", "THDC"],
    "Petroleum & Natural Gas Pipelines": ["GAIL", "IOCL", "BPCL", "HPCL"],
    "Oil Refineries & Petrochemicals": ["IOCL", "BPCL", "HPCL", "CPCL", "MRPL"],
    "Coal Mining & Infrastructure": ["Coal India (CIL)", "NLCIL", "SCCL"],
    "Steel & Metallurgy": ["SAIL", "RINL", "NMDC"],
    "Urban Metro & Transit Systems": ["DMRC", "Maha-Metro", "BMRCL", "CMRL", "KMRL", "UPMRC"],
    "Urban Infrastructure & Water Supply": ["NBCC", "State Urban Dev Auth", "Smart City SPVs"],
    "Ports & Maritime Infrastructure": ["JNPA", "Deendayal Port Auth", "Paradip Port", "V.O.C. Port", "Cochin Port"],
    "Inland Waterways": ["IWAI"],
    "Civil Aviation & Airports": ["AAI", "Special Purpose Airport JV"],
    "Telecommunications & Optical Fibre": ["BSNL", "BBNL (BharatNet)"],
    "Mining & Mineral Processing": ["NALCO", "HCL", "HZL"],
    "Fertilizer Plants & Petrochemicals": ["NFL", "RCF", "HURL", "BVFCL"],
    "Water Resources & Irrigation": ["WAPCOS", "State Irrigation Dept", "NWDA"],
    "Atomic Energy & Nuclear Plants": ["NPCIL", "BHAVINI", "UCIL"],
    "Renewable Energy (Solar/Wind)": ["SECI", "SJVN Green", "NTPC REL"],
    "Heavy Engineering & Equipment": ["BHEL", "HMT"],
    "Defence Infrastructure & Strategic Roads": ["BRO", "DGNP", "MES"]
}

STATES_LIST = [
    "Maharashtra", "Uttar Pradesh", "Tamil Nadu", "Gujarat", "Karnataka",
    "West Bengal", "Rajasthan", "Andhra Pradesh", "Odisha", "Madhya Pradesh",
    "Telangana", "Bihar", "Assam", "Kerala", "Punjab", "Haryana",
    "Chhattisgarh", "Jharkhand", "Uttarakhand", "Himachal Pradesh",
    "Jammu and Kashmir", "Multi-State / National"
]
