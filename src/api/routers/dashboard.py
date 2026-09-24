"""
Dashboard Summary KPIs & Distribution Aggregations Router
"""

import logging
from fastapi import APIRouter
from src.api.db import get_db, parse_json_payload
from src.api.schemas import APIError, DashboardKPIs, ProjectSummary

logger = logging.getLogger("PAIMANA_API.Dashboard")
router = APIRouter(tags=["Dashboard"])


@router.get("/api/dashboard/summary", response_model=DashboardKPIs)
def get_dashboard_summary():
    """
    Returns high-level KPI metrics, sector risk distribution, ministry distribution,
    state geographic distribution, scale breakdown, and top 10 urgent at-risk projects.
    """
    conn = None
    try:
        conn = get_db()
        proj_query = """
            SELECT COUNT(*) as total_projects,
                   SUM(approved_cost_cr) as total_approved,
                   SUM(revised_cost_cr) as total_revised,
                   SUM(cumulative_expenditure_cr) as total_expenditure,
                   SUM(CASE WHEN status = 'Delayed' THEN 1 ELSE 0 END) as delayed_count,
                   SUM(CASE WHEN status = 'Stalled' THEN 1 ELSE 0 END) as stalled_count,
                   SUM(CASE WHEN status = 'On Track' THEN 1 ELSE 0 END) as on_track_count,
                   SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed_count
            FROM projects
        """
        row_agg = conn.execute(proj_query).fetchone()

        total_projects = row_agg['total_projects'] or 0
        total_approved = float(row_agg['total_approved'] or 0)
        total_revised = float(row_agg['total_revised'] or 0)
        total_exp = float(row_agg['total_expenditure'] or 0)
        net_overrun_pct = round(((total_revised - total_approved) / (total_approved + 1e-5)) * 100.0, 2)

        risk_rows = conn.execute("SELECT risk_level, COUNT(*) as count FROM risk_scores GROUP BY risk_level").fetchall()
        risk_dict = {r['risk_level']: r['count'] for r in risk_rows}

        sector_query = """
            SELECT p.sector,
                   COUNT(p.project_id) as count,
                   ROUND(AVG(r.score), 1) as avg_risk_score,
                   ROUND(SUM(p.approved_cost_cr), 0) as total_cost_cr,
                   ROUND(AVG((p.revised_cost_cr - p.approved_cost_cr) / p.approved_cost_cr * 100.0), 1) as overrun_rate
            FROM projects p
            JOIN risk_scores r ON p.project_id = r.project_id
            GROUP BY p.sector
            ORDER BY count DESC
        """
        sector_dist = [dict(r) for r in conn.execute(sector_query).fetchall()]

        ministry_query = """
            SELECT p.ministry,
                   COUNT(p.project_id) as count,
                   SUM(CASE WHEN p.status IN ('Delayed', 'Stalled') THEN 1 ELSE 0 END) as delayed_count,
                   ROUND(AVG(r.score), 1) as avg_risk_score,
                   ROUND(SUM(p.approved_cost_cr), 0) as total_cost_cr
            FROM projects p
            JOIN risk_scores r ON p.project_id = r.project_id
            GROUP BY p.ministry
            ORDER BY count DESC LIMIT 8
        """
        ministry_dist = [dict(r) for r in conn.execute(ministry_query).fetchall()]

        tier_query = """
            SELECT 
                CASE 
                    WHEN approved_cost_cr < 500 THEN 'Small (< ₹500 Cr)'
                    WHEN approved_cost_cr < 1500 THEN 'Medium (₹500-1500 Cr)'
                    WHEN approved_cost_cr < 5000 THEN 'Large (₹1500-5000 Cr)'
                    ELSE 'Mega (> ₹5000 Cr)'
                END as tier,
                COUNT(*) as count,
                SUM(CASE WHEN r.risk_level = 'High' THEN 1 ELSE 0 END) as high_risk_count,
                ROUND(AVG(r.score), 1) as avg_risk_score
            FROM projects p
            JOIN risk_scores r ON p.project_id = r.project_id
            GROUP BY tier
            ORDER BY count DESC
        """
        cost_tier_dist = [dict(r) for r in conn.execute(tier_query).fetchall()]

        state_query = """
            SELECT p.state,
                   COUNT(p.project_id) as total_projects,
                   ROUND(SUM(p.approved_cost_cr), 0) as total_outlay_cr,
                   ROUND(SUM(CASE WHEN r.risk_level = 'High' THEN p.approved_cost_cr ELSE 0 END), 0) as capital_at_risk_cr,
                   SUM(CASE WHEN r.risk_level = 'High' THEN 1 ELSE 0 END) as high_risk_count,
                   ROUND(AVG(r.score), 1) as avg_risk_score
            FROM projects p
            JOIN risk_scores r ON p.project_id = r.project_id
            GROUP BY p.state
            ORDER BY capital_at_risk_cr DESC
        """
        state_dist = [dict(r) for r in conn.execute(state_query).fetchall()]

        top_query = """
            SELECT p.project_id, p.project_name, p.ministry, p.sector, p.implementing_agency,
                   p.state, p.approved_cost_cr, p.revised_cost_cr, p.cumulative_expenditure_cr,
                   p.physical_progress_pct, p.status, r.score as risk_score, r.risk_level,
                   r.previous_score, r.top_factors
            FROM projects p
            JOIN risk_scores r ON p.project_id = r.project_id
            ORDER BY r.score DESC, p.approved_cost_cr DESC
            LIMIT 10
        """
        top_rows = conn.execute(top_query).fetchall()
        top_projects = []
        for r in top_rows:
            factors = parse_json_payload(r['top_factors'])
            top_factor_str = None
            if factors:
                first_f = factors[0]
                top_factor_str = first_f.get('factor', 'Systemic Overrun Risk') if isinstance(first_f, dict) else str(first_f)
            top_projects.append(ProjectSummary(
                project_id=r['project_id'],
                project_name=r['project_name'],
                ministry=r['ministry'],
                sector=r['sector'],
                implementing_agency=r['implementing_agency'],
                state=r['state'],
                approved_cost_cr=float(r['approved_cost_cr']),
                revised_cost_cr=float(r['revised_cost_cr']),
                cumulative_expenditure_cr=float(r['cumulative_expenditure_cr']),
                physical_progress_pct=float(r['physical_progress_pct']),
                status=r['status'],
                risk_score=float(r['risk_score']),
                risk_level=r['risk_level'],
                previous_score=float(r['previous_score']) if r['previous_score'] else None,
                top_factor=top_factor_str
            ))

        return DashboardKPIs(
            total_projects=total_projects,
            total_approved_cost_cr=total_approved,
            total_revised_cost_cr=total_revised,
            total_expenditure_cr=total_exp,
            net_cost_overrun_pct=net_overrun_pct,
            delayed_projects_count=row_agg['delayed_count'] or 0,
            stalled_projects_count=row_agg['stalled_count'] or 0,
            on_track_projects_count=row_agg['on_track_count'] or 0,
            completed_projects_count=row_agg['completed_count'] or 0,
            high_risk_count=risk_dict.get('High', 0),
            medium_risk_count=risk_dict.get('Medium', 0),
            low_risk_count=risk_dict.get('Low', 0),
            sector_distribution=sector_dist,
            ministry_distribution=ministry_dist,
            cost_tier_distribution=cost_tier_dist,
            state_distribution=state_dist,
            top_at_risk_projects=top_projects
        )
    except Exception as e:
        logger.error(f"Error fetching dashboard summary: {e}", exc_info=True)
        raise APIError(status_code=500, detail="Failed to calculate dashboard KPIs.", code="SUMMARY_ERROR")
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass
