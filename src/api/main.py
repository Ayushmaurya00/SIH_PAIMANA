"""
PAIMANA AI - FastAPI Backend Service (Enterprise Edition)
Clean Modular Application Orchestrator
"""

import os
import sys
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

load_dotenv()
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.api.schemas import APIError
from src.api.db import get_db, parse_json_payload
from src.api.limiter import get_global_limiter
from src.api.rag_service import ProjectIntelligenceService

from src.api.routers.health import router as health_router
from src.api.routers.dashboard import router as dashboard_router
from src.api.routers.projects import router as projects_router
from src.api.routers.alerts import router as alerts_router
from src.api.routers.models import router as models_router
from src.api.routers.assistant import router as assistant_router
from src.api.routers.filters import router as filters_router
from src.api.routers.export_report import router as export_router
from src.api.routers.import_reports import router as import_router
from src.api.routers.auth import router as auth_router

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO), format='[%(asctime)s] %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger("PAIMANA_API")

raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000")
allowed_origins = [orig.strip() for orig in raw_origins.split(",") if orig.strip() and orig.strip() != "*"]
if not allowed_origins:
    allowed_origins = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"]

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

app = FastAPI(
    title="PAIMANA AI - Infrastructure Project Monitoring & Early Warning API",
    description="MoSPI / IPMD Decision Support System grounded in CUF telemetry, XGBoost, and SHAP explainability.",
    version="2.0.0"
)

# In production, disable regex to avoid credential leakage; use explicit origins
if ENVIRONMENT == "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if ENVIRONMENT == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; object-src 'none'"
    return response


@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(status_code=exc.status_code, content={"status": "error", "code": exc.code, "message": exc.detail, "details": exc.details})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"status": "error", "code": exc.status_code, "message": str(exc.detail)})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"status": "error", "code": "VALIDATION_ERROR", "message": "Invalid request parameters.", "details": exc.errors()})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception on {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"status": "error", "code": "INTERNAL_ERROR", "message": "An unexpected internal server error occurred."})


# Mount Routers
for r in [health_router, dashboard_router, projects_router, alerts_router, models_router, assistant_router, filters_router, export_router, import_router, auth_router]:
    app.include_router(r)

# Backward Compatibility Re-exports (singleton)
rate_limiter = get_global_limiter(requests_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "30")))
rag_service = ProjectIntelligenceService()
