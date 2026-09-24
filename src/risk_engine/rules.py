"""
Driver Extraction & Early Warning Alert Formatting Rules
"""

from typing import Dict, Any, List, Optional
from src.risk_engine.weights import deterministic_variance
from src.risk_engine.prescriptions import get_prescriptions_for_factors


def extract_top_drivers(
    c_prob: float,
    t_prob: float,
    d_miles: int,
    tot_miles: int,
    exp_p: float,
    time_p: float,
    prog_p: float,
    cost_cr: float,
    sector: str,
    exp_mismatch_val: float
) -> List[Dict[str, Any]]:
    """Extracts and ranks candidate operational drivers for a project."""
    drivers = []
    if c_prob > 0.60:
        drivers.append({'factor': 'High Cost Escalation Probability', 'contribution': float(round(c_prob * 35.0, 1)), 'detail': f'ML model predicts {c_prob:.0%} likelihood of cost overrun based on CUF indicators'})
    if t_prob > 0.60:
        drivers.append({'factor': 'Schedule Delay Risk', 'contribution': float(round(t_prob * 35.0, 1)), 'detail': f'ML model predicts {t_prob:.0%} probability of significant schedule slippage'})
    if d_miles > 0:
        milestone_impact = (d_miles / (tot_miles + 1e-5)) * 15.0
        drivers.append({'factor': 'Milestone Execution Slippage', 'contribution': float(round(milestone_impact, 1)), 'detail': f'{d_miles} of {tot_miles} statutory/construction milestones delayed'})
    if exp_p > (prog_p + 15.0) or time_p > (prog_p + 20.0):
        drivers.append({'factor': 'Expenditure & Schedule Mismatch', 'contribution': float(round(exp_mismatch_val, 1)), 'detail': f'Expenditure at {exp_p:.1f}% and timeline elapsed {time_p:.1f}%, but physical progress is only {prog_p:.1f}%'})
    if cost_cr >= 5000.0:
        drivers.append({'factor': 'Megaproject Scale Complexity', 'contribution': 8.5, 'detail': f'Capital outlay (₹{cost_cr:,.0f} Cr) subject to systemic megaproject compounding friction'})
    if sector in ['Hydroelectric Power', 'Urban Metro & Transit Systems', 'Atomic Energy & Nuclear Plants', 'Water Resources & Irrigation']:
        drivers.append({'factor': f'{sector} Sector Structural Risk', 'contribution': 7.0, 'detail': 'Sector requires complex environmental clearances and specialized contractor engineering'})

    drivers.sort(key=lambda x: x['contribution'], reverse=True)
    top = drivers[:3]
    if not top:
        top = [{'factor': 'On-Track Execution', 'contribution': 0.0, 'detail': f'Physical progress ({prog_p:.1f}%) aligns with expenditure ({exp_p:.1f}%) and scheduled timeline'}]
    return top


def build_alert_if_applicable(
    pid: str,
    p_score: float,
    risk_level: str,
    exp_p: float,
    time_p: float,
    prog_p: float,
    d_miles: int,
    c_prob: float,
    stat: str,
    agency: str,
    now_utc: str,
    primary_prescription: str
) -> Optional[Dict[str, Any]]:
    """Builds early-warning alert record if risk meets trigger criteria."""
    if risk_level == "High":
        reasons = []
        if exp_p > prog_p + 15.0 or time_p > prog_p + 20.0:
            reasons.append(f"Expenditure at {exp_p:.1f}% while {time_p:.1f}% timeline elapsed with only {prog_p:.1f}% physical progress")
        if d_miles >= 2:
            reasons.append(f"{d_miles} critical milestones delayed")
        if c_prob >= 0.85:
            reasons.append(f"Predicted cost escalation probability {c_prob:.0%}")
        if stat in ['Delayed', 'Stalled']:
            reasons.append(f"Project currently {stat}")
        trigger_str = "; ".join(reasons) if reasons else f"Composite risk score reached critical threshold ({p_score}/100)"
        lead_time = round(deterministic_variance(pid, 6.0, 3.0), 1)
        return {'project_id': pid, 'triggered_at': now_utc, 'trigger_reason': trigger_str, 'severity': 'High', 'status': 'New', 'prescriptive_action': primary_prescription, 'lead_time_months': lead_time}

    elif risk_level == "Medium" and (d_miles >= 2 or (exp_p > prog_p + 25.0)):
        reasons = []
        if d_miles >= 2:
            reasons.append(f"{d_miles} milestones delayed under {agency}")
        if exp_p > prog_p + 20.0:
            reasons.append(f"Expenditure lead gap: {exp_p:.1f}% spent vs {prog_p:.1f}% progress")
        lead_time = round(deterministic_variance(pid, 3.75, 2.5), 1)
        return {'project_id': pid, 'triggered_at': now_utc, 'trigger_reason': "; ".join(reasons), 'severity': 'Medium', 'status': 'New', 'prescriptive_action': primary_prescription, 'lead_time_months': lead_time}

    return None
