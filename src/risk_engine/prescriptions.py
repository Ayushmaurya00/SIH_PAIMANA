"""
PAIMANA AI - Prescriptive Infrastructure Remediation Playbook Engine
Translates leading SHAP feature attributions and rule violations into actionable,
domain-specific statutory and administrative remediation playbooks for MoSPI / IPMD.
"""

from typing import Dict, Any, List, Optional

# Structured domain remediation library mapped to leading risk drivers
PRESCRIPTIVE_PLAYBOOKS = {
    'delayed_milestones': {
        'title': 'Statutory Right-of-Way & Civil Milestone Escalation',
        'authority': 'State Empowered Committee / MoSPI IPMD',
        'statutory_timeline_days': 15,
        'recommended_action': (
            "Invoke PM GatiShakti portal escalation to coordinate inter-ministerial clearance. "
            "Trigger Joint Collector fast-track review under Section 3D (NHAI/Railways Act) for pending land parcels."
        ),
        'category': 'Statutory & Land Acquisition'
    },
    'milestone_slippage_ratio': {
        'title': 'Comprehensive Critical Path & Schedule Acceleration Review',
        'authority': 'Project Director & Lead EPC Contractor',
        'statutory_timeline_days': 21,
        'recommended_action': (
            "Conduct micro-scheduling audit of critical path milestones. Require contractor to submit a catch-up "
            "resource mobilization plan with augmented double-shift equipment deployment."
        ),
        'category': 'Contractor & Execution'
    },
    'expenditure_to_progress_ratio': {
        'title': 'Financial Forensic Audit & Escrow Milestone Reconciliation',
        'authority': 'Integrated Financial Adviser (IFA) & Chief Vigilance Officer',
        'statutory_timeline_days': 10,
        'recommended_action': (
            "Freeze unlinked mobilization advance disbursements. Reconcile Measurement Books (MB) against physical "
            "site inspection geo-tagged photos before clearing next Running Account (RA) bills."
        ),
        'category': 'Financial Governance'
    },
    'expenditure_vs_time_gap': {
        'title': 'Expenditure Velocity Realignment & DPR Rationalization',
        'authority': 'Public Investment Board (PIB) / Ministry Financial Wing',
        'statutory_timeline_days': 30,
        'recommended_action': (
            "Review Revised Cost Estimate (RCE) submission. Determine if capital outlay pace reflects material cost "
            "escalation or scope expansion requiring Revised Administrative Approval."
        ),
        'category': 'Cost Control'
    },
    'progress_vs_time_gap': {
        'title': 'Civil Work Acceleration & Bottleneck Decongestion',
        'authority': 'Implementing Agency Chief Engineer & MoSPI Nodal Officer',
        'statutory_timeline_days': 14,
        'recommended_action': (
            "Establish weekly nodal progress dashboard. Identify specific local utility shifts (power/water lines) "
            "and engage Municipal / State authorities under fast-track single-window protocol."
        ),
        'category': 'Operational Bottlenecks'
    },
    'agency_historical_overrun_avg': {
        'title': 'Agency Track Record Institutional Oversight & Support',
        'authority': 'NITI Aayog Project Monitoring Unit / MoSPI High-Level Committee',
        'statutory_timeline_days': 30,
        'recommended_action': (
            "Deploy Independent Engineer / Technical Advisory Panel to bolster agency contract management "
            "and dispute resolution capability under Vivad se Vishwas-II framework."
        ),
        'category': 'Institutional Capacity'
    },
    'is_megaproject': {
        'title': 'Megaproject Governance Protocol (Flyvbjerg Escalation Law)',
        'authority': 'Cabinet Committee on Economic Affairs (CCEA)',
        'statutory_timeline_days': 45,
        'recommended_action': (
            "Form Dedicated Special Purpose Vehicle (SPV) Oversight Board with monthly milestone telemetry reporting "
            "directly to the Minister of State (Independent Charge) MoSPI."
        ),
        'category': 'Megaproject Scale'
    },
    'state_historical_overrun_avg': {
        'title': 'State-Level Coordination Committee (SLCC) Direct Engagement',
        'authority': 'Chief Secretary of State & Union Ministry Secretary',
        'statutory_timeline_days': 14,
        'recommended_action': (
            "Convene bilateral SLCC meeting with State Chief Secretary to resolve forest clearance approvals "
            "and law-and-order/quarry permit constraints."
        ),
        'category': 'State Inter-Agency'
    }
}


def get_prescriptions_for_factors(top_factors: List[Dict[str, Any]], project_context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Translates top contributing factors and rule flags into actionable domain playbooks.
    """
    prescriptions = []
    seen_categories = set()

    for factor_info in top_factors:
        raw_factor = factor_info.get('raw_factor') or factor_info.get('factor', '')
        
        # Match against playbook keys
        matched_key = None
        for key in PRESCRIPTIVE_PLAYBOOKS:
            if key in raw_factor.lower() or raw_factor.lower() in key:
                matched_key = key
                break

        if not matched_key:
            # Check secondary keywords
            if 'milestone' in raw_factor.lower():
                matched_key = 'delayed_milestones'
            elif 'expenditure' in raw_factor.lower() or 'ratio' in raw_factor.lower():
                matched_key = 'expenditure_to_progress_ratio'
            elif 'agency' in raw_factor.lower():
                matched_key = 'agency_historical_overrun_avg'
            elif 'mega' in raw_factor.lower() or 'cost' in raw_factor.lower():
                matched_key = 'is_megaproject'

        if matched_key and matched_key in PRESCRIPTIVE_PLAYBOOKS:
            playbook = PRESCRIPTIVE_PLAYBOOKS[matched_key].copy()
            if playbook['category'] not in seen_categories:
                playbook['triggering_factor'] = factor_info.get('factor', raw_factor)
                playbook['contribution_pts'] = factor_info.get('contribution', 0)
                prescriptions.append(playbook)
                seen_categories.add(playbook['category'])

    # Default fallback if no specific playbook matched
    if not prescriptions:
        prescriptions.append({
            'title': 'Standard Monitoring & Quarterly Milestone Verification',
            'authority': 'Implementing Agency Regional Executive Director',
            'statutory_timeline_days': 30,
            'recommended_action': "Continue monthly physical inspection and ensure CUF data upload integrity.",
            'category': 'Routine Governance',
            'triggering_factor': 'General Monitoring Schedule',
            'contribution_pts': 0
        })

    return prescriptions[:3]
