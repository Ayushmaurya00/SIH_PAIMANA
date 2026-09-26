"""
Health Check & Dependency Diagnostics Endpoint
"""

import os
import time
import datetime
from fastapi import APIRouter
from src.api.db import get_db, ROOT_DIR, DB_PATH
from src.api.rag_service import ProjectIntelligenceService

router = APIRouter(tags=["Health"])
rag_service = ProjectIntelligenceService(db_path=DB_PATH)


@router.get("/api/health")
def health_check():
    """
    Returns API health along with live status of core dependencies.
    """
    start_t = time.time()
    db_status = "unavailable"
    project_count = 0
    db_latency_ms = None

    conn = None
    try:
        conn = get_db(retries=1)
        count_row = conn.execute("SELECT COUNT(*) FROM projects").fetchone()
        project_count = count_row[0] if count_row else 0
        db_latency_ms = round((time.time() - start_t) * 1000, 2)
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass

    model_bundle_path = os.path.join(ROOT_DIR, "artifacts", "models", "model_bundle_cuf_plus_extra.joblib")
    models_ready = os.path.exists(model_bundle_path)

    # Do not leak absolute paths
    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "service": "PAIMANA AI API",
        "version": "2.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "dependencies": {
            "database": {
                "status": db_status,
                "latency_ms": db_latency_ms,
                "projects_count": project_count
            },
            "llm_service": {
                "provider": "google_gemini" if rag_service.llm_available else "deterministic_fallback",
                "status": "available" if rag_service.llm_available else "offline (fallback mode active)",
                "active_model": rag_service.active_model or "deterministic_template",
                "key_configured": bool(os.getenv("GEMINI_API_KEY", "").strip())
            },
            "ollama_llm": {
                "status": "available" if rag_service.ollama_available else "offline (fallback mode active)",
                "active_model": rag_service.active_model or "deterministic_template"
            },
            "ml_models": {
                "status": "loaded" if models_ready else "not_found"
            }
        }
    }
