"""
CSV Portfolio Risk & Early Warning Report Exporter Router
"""

import io
import csv
import datetime
import logging
from starlette.responses import Response
from fastapi import APIRouter, Depends
from src.api.db import get_db
from src.api.schemas import APIError
from src.api.auth import get_current_user

logger = logging.getLogger("PAIMANA_API.Export")
router = APIRouter(tags=["Export"])


@router.get("/api/export/risk-report")
def export_risk_report(user=Depends(get_current_user)):
    """
    Exports full MoSPI Central Sector Portfolio Risk & Early Warning Report as CSV.
    """
    conn = None
    try:
        conn = get_db()
        sql = """
            SELECT p.project_id, p.project_name, p.ministry, p.sector, p.implementing_agency, p.state,
                   p.approved_cost_cr, p.revised_cost_cr, p.cumulative_expenditure_cr, p.physical_progress_pct,
                   p.status, r.score as risk_score, r.risk_level,
                   m.cost_overrun_pct_pred, m.cost_overrun_pct_lower, m.cost_overrun_pct_upper,
                   m.time_overrun_months_pred, m.time_delay_lower_months, m.time_delay_upper_months
            FROM projects p
            LEFT JOIN risk_scores r ON p.project_id = r.project_id
            LEFT JOIN model_predictions m ON p.project_id = m.project_id AND m.feature_set = 'cuf_plus_extra'
            ORDER BY r.score DESC, p.approved_cost_cr DESC
        """
        rows = conn.execute(sql).fetchall()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Project ID", "Project Name", "Ministry", "Sector", "Agency", "State",
            "Sanctioned Outlay (Cr)", "Revised Estimate (Cr)", "Expenditure (Cr)", "Progress (%)",
            "Status", "Risk Score (0-100)", "Risk Level",
            "Pred Cost Escalation (%)", "Cost Escalation Lower 90% CI", "Cost Escalation Upper 90% CI",
            "Pred Time Delay (Mos)", "Time Delay Lower 90% CI", "Time Delay Upper 90% CI"
        ])
        for r in rows:
            writer.writerow(list(r))

        csv_data = output.getvalue()
        output.close()
        headers = {
            "Content-Disposition": f'attachment; filename="MoSPI_Portfolio_Risk_Report_{datetime.date.today().isoformat()}.csv"'
        }
        return Response(content=csv_data, media_type="text/csv", headers=headers)
    except Exception as e:
        logger.error(f"Error exporting risk report: {e}", exc_info=True)
        raise APIError(status_code=500, detail="Failed to export risk report.", code="EXPORT_ERROR")
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass
