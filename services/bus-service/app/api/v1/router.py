"""v1 API router for Bus Service."""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()

# Phase 7 မှာ endpoints တွေ ထည့်မယ်:
# router.include_router(operators.router, prefix="/operators", tags=["operators"])
# router.include_router(routes.router, prefix="/routes", tags=["routes"])
# router.include_router(trips.router, prefix="/trips", tags=["trips"])