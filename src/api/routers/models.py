"""
ML Model Metrics & Evaluation Comparison Router
"""

import logging
from typing import List
from fastapi import APIRouter
from src.api.db import get_db
from src.api.schemas import APIError, ModelMetricItem

logger = logging.getLogger("PAIMANA_API.Models")
router = APIRouter(tags=["Models"])


@router.get("/api/models/metrics", response_model=List[ModelMetricItem])
def get_model_metrics():
    conn = None
    try:
        conn = get_db()
        rows = conn.execute("SELECT * FROM model_metrics ORDER BY feature_set, target, accuracy DESC").fetchall()
        results = [ModelMetricItem(**dict(r)) for r in rows]
        return results
    except Exception as e:
        logger.error(f"Error fetching model metrics: {e}", exc_info=True)
        raise APIError(status_code=500, detail="Failed to fetch model evaluation metrics.", code="METRICS_ERROR")
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass
