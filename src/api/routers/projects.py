"""
Project Explorer, Details & Management Router
"""

import logging
import os
from typing import Optional
from fastapi import APIRouter, Query, Path, Depends
from src.api.db import get_db, parse_json_payload
from src.api.schemas import APIError, ProjectDetail, MonthlySnapshotItem, MilestoneItem
from src.api.auth import get_current_user, require_min_clearance, require_role

logger = logging.getLogger("PAIMANA_API.Projects")
router = APIRouter(tags=["Projects"])


@router.get("/api/projects")
def get_projects(
    search: Optional[str] = Query(None), ministry: Optional[str] = Query(None),
    sector: Optional[str] = Query(None), status: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None), cost_min: Optional[float] = Query(None),
    cost_max: Optional[float] = Query(None), sort_by: str = Query("score", pattern="^(score|cost|progress|name)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0)
):
    conn = None
    try:
        conn = get_db()
        where_clauses, params = ["1=1"], []
        if search:
            # Cap search length to prevent LIKE DoS
            search_capped = search[:100]
            where_clauses.append("(p.project_name LIKE ? OR p.project_id LIKE ? OR p.implementing_agency LIKE ?)")
            params.extend([f"%{search_capped}%"] * 3)
        for key, val in [("p.ministry", ministry), ("p.sector", sector), ("p.status", status), ("r.risk_level", risk_level)]:
            if val and val != "All":
                if key == "r.risk_level" and val.strip().lower() in ["critical", "high"]:
                    where_clauses.append("LOWER(r.risk_level) = 'high'")
                else:
                    where_clauses.append(f"LOWER({key}) = LOWER(?)")
                    params.append(val.strip()[:100])
        if cost_min is not None:
            where_clauses.append("p.approved_cost_cr >= ?"); params.append(cost_min)
        if cost_max is not None:
            where_clauses.append("p.approved_cost_cr <= ?"); params.append(cost_max)

        where_str = " AND ".join(where_clauses)
        sort_map = {'score': 'COALESCE(r.score,0)', 'cost': 'p.approved_cost_cr', 'progress': 'p.physical_progress_pct', 'name': 'p.project_name'}
        col, order = sort_map.get(sort_by, 'COALESCE(r.score,0)'), ("ASC" if sort_order == "asc" else "DESC")
        total = conn.execute(f"SELECT COUNT(*) as total FROM projects p LEFT JOIN risk_scores r ON p.project_id = r.project_id WHERE {where_str}", params).fetchone()['total']

        rows = conn.execute(f"""
            SELECT p.*, COALESCE(r.score,0) as risk_score, COALESCE(r.risk_level,'Low') as risk_level, r.previous_score, r.top_factors
            FROM projects p LEFT JOIN risk_scores r ON p.project_id = r.project_id
            WHERE {where_str} ORDER BY {col} {order} LIMIT ? OFFSET ?
        """, params + [limit, offset]).fetchall()

        results = []
        for r in rows:
            try:
                factors = parse_json_payload(r['top_factors'])
            except Exception:
                factors = []
            top_f = (factors[0].get('factor', str(factors[0])) if isinstance(factors[0], dict) else str(factors[0])) if factors else None
            results.append({
                'project_id': r['project_id'], 'project_name': r['project_name'], 'ministry': r['ministry'],
                'sector': r['sector'], 'implementing_agency': r['implementing_agency'], 'state': r['state'],
                'approved_cost_cr': float(r['approved_cost_cr']), 'revised_cost_cr': float(r['revised_cost_cr']),
                'cumulative_expenditure_cr': float(r['cumulative_expenditure_cr']),
                'physical_progress_pct': float(r['physical_progress_pct']), 'status': r['status'],
                'risk_score': float(r['risk_score'] or 0), 'risk_level': r['risk_level'] or 'Low',
                'previous_score': float(r['previous_score']) if r['previous_score'] else None,
                'top_factor': top_f
            })
        return {"projects": results, "total": total, "limit": limit, "offset": offset}
    except Exception as e:
        logger.error(f"Error fetching projects: {e}", exc_info=True)
        raise APIError(status_code=500, detail="Failed to query project database.", code="PROJECT_QUERY_ERROR")
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass


@router.get("/api/projects/{project_id}", response_model=ProjectDetail)
def get_project_detail(project_id: str = Path(..., description="Project ID e.g. PRJ-00004")):
    conn = None
    try:
        conn = get_db()
        p_row = conn.execute("""
            SELECT p.*, r.score, r.risk_level, r.previous_score, r.top_factors, r.prescriptive_actions,
                   m.cost_overrun_prob, m.cost_overrun_pct_pred, m.cost_overrun_pct_lower, m.cost_overrun_pct_upper,
                   m.time_overrun_prob, m.time_overrun_months_pred, m.time_delay_lower_months, m.time_delay_upper_months
            FROM projects p
            LEFT JOIN risk_scores r ON p.project_id = r.project_id
            LEFT JOIN model_predictions m ON p.project_id = m.project_id AND m.feature_set = 'cuf_plus_extra'
            WHERE p.project_id = ?
        """, [project_id]).fetchone()
        if not p_row:
            conn.close()
            raise APIError(status_code=404, detail=f"Project '{project_id}' not found.", code="PROJECT_NOT_FOUND")

        s_rows = conn.execute("SELECT * FROM monthly_snapshots WHERE project_id = ? ORDER BY snapshot_month ASC", [project_id]).fetchall()
        snapshots = [MonthlySnapshotItem(snapshot_id=s['snapshot_id'], project_id=s['project_id'], snapshot_month=str(s['snapshot_month']), revised_cost_cr=float(s['revised_cost_cr']), cumulative_expenditure_cr=float(s['cumulative_expenditure_cr']), physical_progress_pct=float(s['physical_progress_pct']), status=s['status']) for s in s_rows]

        m_rows = conn.execute("SELECT * FROM milestones WHERE project_id = ? ORDER BY planned_date ASC", [project_id]).fetchall()
        milestones = [MilestoneItem(milestone_id=m['milestone_id'], project_id=m['project_id'], milestone_name=m['milestone_name'], planned_date=str(m['planned_date']), achieved_date=str(m['achieved_date']) if m['achieved_date'] else None, is_delayed=bool(m['is_delayed'])) for m in m_rows]

        norm_factors = [{"factor": f.get("factor", str(f)), "contribution": float(f.get("contribution", 15.0))} if isinstance(f, dict) else {"factor": str(f), "contribution": 15.0} for f in parse_json_payload(p_row['top_factors'])]
        norm_actions = [{"title": a.get("title", "Administrative Directive"), "authority": a.get("authority", "Project Monitoring Group (PMG)"), "statutory_timeline_days": int(a.get("statutory_timeline_days", 30)), "recommended_action": a.get("recommended_action", str(a))} if isinstance(a, dict) else {"title": "Administrative Escalation Directive", "authority": "Project Monitoring Group (PMG)", "statutory_timeline_days": 30, "recommended_action": str(a)} for a in parse_json_payload(p_row['prescriptive_actions'])]

        return ProjectDetail(
            project_id=p_row['project_id'], project_name=p_row['project_name'], ministry=p_row['ministry'],
            sector=p_row['sector'], implementing_agency=p_row['implementing_agency'], state=p_row['state'],
            approved_cost_cr=float(p_row['approved_cost_cr']), revised_cost_cr=float(p_row['revised_cost_cr']),
            cumulative_expenditure_cr=float(p_row['cumulative_expenditure_cr']),
            approval_date=str(p_row['approval_date']), scheduled_start=str(p_row['scheduled_start']),
            scheduled_completion=str(p_row['scheduled_completion']),
            revised_completion=str(p_row['revised_completion']) if p_row['revised_completion'] else None,
            physical_progress_pct=float(p_row['physical_progress_pct']), status=p_row['status'],
            risk_score=float(p_row['score'] or 0), risk_level=p_row['risk_level'] or 'Low',
            previous_score=float(p_row['previous_score']) if p_row['previous_score'] else None,
            top_factors=norm_factors, prescriptive_actions=norm_actions,
            cost_overrun_prob=float(p_row['cost_overrun_prob']) if p_row['cost_overrun_prob'] is not None else None,
            cost_overrun_pct_pred=float(p_row['cost_overrun_pct_pred']) if p_row['cost_overrun_pct_pred'] is not None else None,
            cost_overrun_pct_lower=float(p_row['cost_overrun_pct_lower']) if p_row['cost_overrun_pct_lower'] is not None else None,
            cost_overrun_pct_upper=float(p_row['cost_overrun_pct_upper']) if p_row['cost_overrun_pct_upper'] is not None else None,
            time_overrun_prob=float(p_row['time_overrun_prob']) if p_row['time_overrun_prob'] is not None else None,
            time_overrun_months_pred=float(p_row['time_overrun_months_pred']) if p_row['time_overrun_months_pred'] is not None else None,
            time_delay_lower_months=float(p_row['time_delay_lower_months']) if p_row['time_delay_lower_months'] is not None else None,
            time_delay_upper_months=float(p_row['time_delay_upper_months']) if p_row['time_delay_upper_months'] is not None else None,
            snapshots=snapshots, milestones=milestones
        )
    except APIError:
        raise
    except Exception as e:
        logger.error(f"Error fetching project detail: {e}", exc_info=True)
        raise APIError(status_code=500, detail="Failed to fetch project detail.", code="PROJECT_DETAIL_ERROR")
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass


@router.delete("/api/projects/{project_id}")
def delete_project(project_id: str = Path(..., description="Project ID to remove"), user=Depends(require_role(["admin", "nodal_officer"]))):
    conn = None
    try:
        conn = get_db()
        cur = conn.cursor()
        row = cur.execute("SELECT project_name FROM projects WHERE project_id = ?", (project_id,)).fetchone()
        if not row:
            raise APIError(status_code=404, detail=f"Project '{project_id}' not found.", code="PROJECT_NOT_FOUND")
        for tbl in ["alerts", "risk_scores", "model_predictions", "milestones", "monthly_snapshots", "projects"]:
            cur.execute(f"DELETE FROM {tbl} WHERE project_id = ?", (project_id,))
        conn.commit()
        logger.info(f"Project {project_id} deleted by user {user.get('email','unknown')}")
        return {"status": "success", "deleted_project_id": project_id, "message": f"Successfully deleted project {project_id}."}
    except APIError:
        raise
    except Exception as e:
        logger.error(f"Error deleting project: {e}", exc_info=True)
        raise APIError(status_code=500, detail="Failed to delete project.", code="PROJECT_DELETE_ERROR")
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass


@router.delete("/api/projects")
def clear_all_projects(user=Depends(require_min_clearance(5))):
    # Production safeguard: block purge in production unless explicitly allowed
    if os.getenv("ENVIRONMENT", "development") == "production" and os.getenv("ALLOW_PURGE", "false").lower() != "true":
        raise APIError(status_code=403, detail="Purge disabled in production. Set ALLOW_PURGE=true to enable.", code="PURGE_DISABLED")
    conn = None
    try:
        conn = get_db()
        cur = conn.cursor()
        for tbl in ["alerts", "risk_scores", "model_predictions", "milestones", "monthly_snapshots", "projects"]:
            cur.execute(f"DELETE FROM {tbl}")
        conn.commit()
        logger.warning(f"PURGE ALL executed by {user.get('email','unknown')} clearance {user.get('clearance_level')}")
        return {"status": "success", "message": "All projects and telemetry data have been purged successfully."}
    except Exception as e:
        logger.error(f"Error purging projects: {e}", exc_info=True)
        raise APIError(status_code=500, detail="Failed to clear database projects.", code="PURGE_ERROR")
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass
