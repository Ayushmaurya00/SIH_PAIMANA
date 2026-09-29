"""
AI Assistant / Copilot Query Router with Rate Limiting
"""

import os
import logging
from fastapi import APIRouter, Request
from src.api.db import DB_PATH
from src.api.limiter import get_global_limiter
from src.api.schemas import APIError, AssistantQueryRequest, AssistantQueryResponse
from src.api.rag_service import ProjectIntelligenceService

logger = logging.getLogger("PAIMANA_API.Assistant")
router = APIRouter(tags=["Assistant"])

RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "30"))
rate_limiter = get_global_limiter(requests_per_minute=RATE_LIMIT_PER_MINUTE)
rag_service = ProjectIntelligenceService(db_path=DB_PATH)


@router.post("/api/assistant/query", response_model=AssistantQueryResponse)
def query_assistant(req: AssistantQueryRequest, request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    allowed, retry_after = rate_limiter.is_allowed(client_ip)
    if not allowed:
        raise APIError(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {RATE_LIMIT_PER_MINUTE} queries per minute allowed.",
            code="RATE_LIMIT_EXCEEDED",
            details={"retry_after_seconds": retry_after}
        )

    try:
        res = rag_service.query(question=req.question, context_project_id=req.context_project_id)
        return AssistantQueryResponse(
            answer=res['answer'],
            sources=res['sources'],
            confidence=res['confidence'],
            grounded_verified=res.get('grounded_verified', True),
            fallback_mode=res.get('fallback_mode', False),
            mode=res.get('mode', 'fallback'),
            model_used=res.get('model_used', None)
        )
    except APIError:
        raise
    except Exception as e:
        logger.error(f"Error querying AI assistant: {e}", exc_info=True)
        raise APIError(status_code=500, detail="Failed to process assistant query.", code="COPILOT_QUERY_ERROR")
