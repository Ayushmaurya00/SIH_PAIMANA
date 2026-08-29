"""
CUF Column Mappings & Sector Metadata
"""

SECTOR_TO_MINISTRY_MAP = {
    "Road Transport & Highways": "Ministry of Road Transport and Highways (MoRTH)",
    "Road Transport and Highways": "Ministry of Road Transport and Highways (MoRTH)",
    "Roads & Highways": "Ministry of Road Transport and Highways (MoRTH)",
    "Roads and Highways": "Ministry of Road Transport and Highways (MoRTH)",
    "Railways": "Ministry of Railways (MoR)",
    "Power Transmission & Distribution": "Ministry of Power (MoP)",
    "Transmission & Distribution": "Ministry of Power (MoP)",
    "Thermal Power Generation": "Ministry of Power (MoP)",
    "Electricity Generation": "Ministry of Power (MoP)",
    "Hydroelectric Power": "Ministry of Power (MoP)",
    "Energy Storage": "Ministry of Power (MoP)",
    "Petroleum & Natural Gas Pipelines": "Ministry of Petroleum and Natural Gas (MoPNG)",
    "Oil Refineries & Petrochemicals": "Ministry of Petroleum and Natural Gas (MoPNG)",
    "Oil & Gas": "Ministry of Petroleum and Natural Gas (MoPNG)",
    "Coal Mining & Infrastructure": "Ministry of Coal (MoC)",
    "Coal": "Ministry of Coal (MoC)",
    "Steel & Metallurgy": "Ministry of Steel (MoS)",
    "Steel": "Ministry of Steel (MoS)",
    "Metals & Mining": "Ministry of Mines",
    "Mining & Mineral Processing": "Ministry of Mines",
    "Urban Metro & Transit Systems": "Ministry of Housing and Urban Affairs (MoHUA)",
    "Urban Public Transport": "Ministry of Housing and Urban Affairs (MoHUA)",
    "Urban Infrastructure & Water Supply": "Ministry of Housing and Urban Affairs (MoHUA)",
    "Real Estate": "Ministry of Housing and Urban Affairs (MoHUA)",
    "Construction": "Ministry of Housing and Urban Affairs (MoHUA)",
    "Ports & Maritime Infrastructure": "Ministry of Ports, Shipping and Waterways (MoPSW)",
    "Inland Waterways": "Ministry of Ports, Shipping and Waterways (MoPSW)",
    "Shipping": "Ministry of Ports, Shipping and Waterways (MoPSW)",
    "Civil Aviation & Airports": "Ministry of Civil Aviation (MoCA)",
    "Aviation & Aviation Infrastructure": "Ministry of Civil Aviation (MoCA)",
    "Telecommunications & Optical Fibre": "Ministry of Communications",
    "Telecommunication": "Ministry of Communications",
    "Education": "Ministry of Education",
    "Healthcare": "Ministry of Health and Family Welfare",
    "Water Resources": "Ministry of Jal Shakti",
    "Water Resources & Irrigation": "Ministry of Jal Shakti",
    "Waste & Water": "Ministry of Jal Shakti",
    "Atomic Energy & Nuclear Plants": "Department of Atomic Energy (DAE)",
    "Renewable Energy (Solar/Wind)": "Ministry of New and Renewable Energy (MNRE)",
    "Heavy Engineering & Equipment": "Ministry of Heavy Industries",
    "Fertilizer Plants & Petrochemicals": "Ministry of Chemicals and Fertilizers",
    "Tourism, Hospitality & Wellness": "Ministry of Tourism",
    "Logistics Infrastructure": "Ministry of Commerce and Industry",
    "Defence Infrastructure & Strategic Roads": "Ministry of Defence"
}

COLUMN_MAPPINGS = {
    "project id": "project_id", "project_id": "project_id", "cuf id": "project_id", "cuf_id": "project_id", "project code": "project_id",
    "project name": "project_name", "project_name": "project_name", "name of project": "project_name", "project title": "project_name",
    "ministry": "ministry", "ministry name": "ministry", "ministry / department": "ministry",
    "sector": "sector", "sector name": "sector",
    "implementing agency": "implementing_agency", "implementing_agency": "implementing_agency", "agency": "implementing_agency", "executing agency": "implementing_agency",
    "state": "state", "state / ut": "state", "location": "state",
    "approved cost (cr)": "approved_cost_cr", "approved cost (₹ cr)": "approved_cost_cr", "approved_cost_cr": "approved_cost_cr", "original cost": "approved_cost_cr", "sanctioned cost": "approved_cost_cr", "approved cost": "approved_cost_cr",
    "revised cost (cr)": "revised_cost_cr", "revised cost (₹ cr)": "revised_cost_cr", "revised_cost_cr": "revised_cost_cr", "anticipated cost": "revised_cost_cr", "latest revised cost": "revised_cost_cr",
    "cumulative expenditure (cr)": "cumulative_expenditure_cr", "cumulative expenditure (₹ cr)": "cumulative_expenditure_cr", "cumulative_expenditure_cr": "cumulative_expenditure_cr", "expenditure incurred": "cumulative_expenditure_cr", "cumulative expenditure": "cumulative_expenditure_cr",
    "approval date": "approval_date", "approval_date": "approval_date", "date of approval": "approval_date", "date of sanction": "approval_date",
    "scheduled start": "scheduled_start", "scheduled_start": "scheduled_start", "start date": "scheduled_start", "actual / scheduled start": "scheduled_start",
    "scheduled completion": "scheduled_completion", "scheduled_completion": "scheduled_completion", "original completion date": "scheduled_completion", "target date of completion": "scheduled_completion",
    "revised completion": "revised_completion", "revised_completion": "revised_completion", "anticipated completion date": "revised_completion", "expected completion": "revised_completion",
    "physical progress (%)": "physical_progress_pct", "physical progress pct": "physical_progress_pct", "physical_progress_pct": "physical_progress_pct", "physical progress": "physical_progress_pct", "progress (%)": "physical_progress_pct",
    "status": "status", "project status": "status", "monitoring status": "status"
}

REQUIRED_CANONICAL_COLUMNS = {
    "project_id", "project_name", "ministry", "sector", "implementing_agency",
    "state", "approved_cost_cr", "physical_progress_pct"
}

VALID_STATUSES = {"On Track", "Delayed", "Stalled", "Completed"}
