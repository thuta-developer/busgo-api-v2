"""
FastAPI application entrypoint for Bus Service.
"""
from __future__ import annotations

import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import router as api_router
from app.core.config import settings
from app.core.exceptions import (
    BusGoError,
    busgo_error_handler,
    generic_error_handler,
    validation_error_handler,
)
from app.core.logging import get_logger, setup_logging

setup_logging(level="DEBUG" if settings.DEBUG else "INFO")
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown hooks."""
    logger.info("Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)
    yield
    logger.info("Shutting down %s", settings.APP_NAME)


app = FastAPI(
    title="BusGo — Bus Service",
    version=settings.APP_VERSION,
    description="Operators, buses, routes, trips, seat availability.",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan,
)

# ------------------------------------------------------------------
# Middleware — request_id
# ------------------------------------------------------------------
@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# ------------------------------------------------------------------
# CORS
# ------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# Exception handlers
# ------------------------------------------------------------------
app.add_exception_handler(BusGoError, busgo_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, generic_error_handler)

# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------
app.include_router(api_router, prefix="/api")


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok", "service": settings.APP_NAME}