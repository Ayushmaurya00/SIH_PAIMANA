"""
Early Warning Alerts Triage & Review Router
Supports chunked pagination (limit/offset) and status updates.
"""

import logging
from typing import Optional, List
from fastapi import APIRouter, Query, Depends
from src.api.db import get_db
from src.api.schemas import APIError, AlertItem
from src.api.auth import require_role

logger = logging.getLogger("PAIMANA_API.Alerts")
router = APIRouter(tags=["Alerts"])


@router.get("/api/alerts", response_model=List[AlertItem])
def get_alerts(
    severity: Optional[str] = Query(None, pattern="^(High|Medium|Low)$"),
    status: Optional[str] = Query(None),
    limit: Optional[int] = Query(None, ge=1),
    offset: Optional[int] = Query(0, ge=0)
):
    conn = None
    try:
        conn = get_db()
        where_clauses = ["1=1"]
        params = []
        if severity:
            where_clauses.append("a.severity = ?")
            params.append(severity)
        if status:
            where_clauses.append("a.status = ?")
            params.append(status)

        where_str = " AND ".join(where_clauses)
        limit_clause = ""
        if limit is not None:
            limit_clause = f" LIMIT {int(limit)} OFFSET {int(offset or 0)}"
        elif offset:
            limit_clause = f" OFFSET {int(offset)}"

        query_sql = f"""
            SELECT a.alert_id, a.project_id, a.triggered_at, a.trigger_reason,
                   a.severity, a.status, a.prescriptive_action, a.lead_time_months,
                   p.project_name, p.ministry, p.sector, p.implementing_agency,
                   p.approved_cost_cr, r.score as risk_score, r.risk_level
            FROM alerts a
            JOIN projects p ON a.project_id = p.project_id
            JOIN risk_scores r ON a.project_id = r.project_id
            WHERE {where_str}
            ORDER BY CASE WHEN a.severity = 'High' THEN 1 WHEN a.severity = 'Medium' THEN 2 ELSE 3 END,
                     r.score DESC, a.alert_id ASC
            {limit_clause}
        """
        rows = conn.execute(query_sql, params).fetchall()
        results = [AlertItem(**dict(r)) for r in rows]
        return results
    except Exception as e:
        logger.error(f"Error fetching alerts: {e}", exc_info=True)
        raise APIError(status_code=500, detail="Failed to query early warning alerts.", code="ALERTS_ERROR")
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass


@router.get("/api/alerts/count")
def get_alerts_count(
    severity: Optional[str] = Query(None, pattern="^(High|Medium|Low)$"),
    status: Optional[str] = Query(None)
):
    conn = None
    try:
        conn = get_db()
        where_clauses = ["1=1"]
        params = []
        if severity:
            where_clauses.append("severity = ?")
            params.append(severity)
        if status:
            where_clauses.append("status = ?")
            params.append(status)

        where_str = " AND ".join(where_clauses)
        row = conn.execute(f"SELECT count(*) as cnt FROM alerts WHERE {where_str}", params).fetchone()
        return {"count": row["cnt"] if row else 0}
    except Exception as e:
        logger.error(f"Error counting alerts: {e}", exc_info=True)
        raise APIError(status_code=500, detail="Failed to count early warning alerts.", code="ALERTS_COUNT_ERROR")
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass


@router.post("/api/alerts/{alert_id}/review")
def review_alert(
    alert_id: int,
    current_user: dict = Depends(require_role(["admin", "nodal_officer"]))
):
    conn = None
    try:
        conn = get_db()
        cur = conn.execute("UPDATE alerts SET status = 'Reviewed' WHERE alert_id = ?", [alert_id])
        if cur.rowcount == 0:
            raise APIError(status_code=404, detail=f"Alert ID {alert_id} not found.", code="ALERT_NOT_FOUND")
        conn.commit()
        return {"status": "success", "alert_id": alert_id, "updated_status": "Reviewed"}
    except APIError:
        raise
    except Exception as e:
        logger.error(f"Error reviewing alert {alert_id}: {e}", exc_info=True)
        raise APIError(status_code=500, detail="Failed to update alert review status.", code="ALERT_REVIEW_ERROR")
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass
