"""
Filter Options Dropdown Metadata Router
"""

import logging
from fastapi import APIRouter
from src.api.db import get_db
from src.api.schemas import APIError

logger = logging.getLogger("PAIMANA_API.Filters")
router = APIRouter(tags=["Filters"])


@router.get("/api/filters/options")
def get_filter_options():
    conn = None
    try:
        conn = get_db()
        ministries = [r[0] for r in conn.execute("SELECT DISTINCT ministry FROM projects ORDER BY ministry").fetchall()]
        sectors = [r[0] for r in conn.execute("SELECT DISTINCT sector FROM projects ORDER BY sector").fetchall()]
        states = [r[0] for r in conn.execute("SELECT DISTINCT state FROM projects ORDER BY state").fetchall()]
        return {
            "ministries": ministries,
            "sectors": sectors,
            "states": states,
            "statuses": ["On Track", "Delayed", "Stalled", "Completed"],
            "risk_levels": ["High", "Medium", "Low"]
        }
    except Exception as e:
        logger.error(f"Error fetching filter options: {e}", exc_info=True)
        raise APIError(status_code=500, detail="Failed to retrieve filter options.", code="FILTER_OPTIONS_ERROR")
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass
