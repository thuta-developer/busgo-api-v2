"""Custom exceptions and handlers for FastAPI services."""
from __future__ import annotations

from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class BusGoError(Exception):
    """Base application error."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(BusGoError):
    def __init__(self, message: str = "Resource not found", details: dict | None = None):
        super().__init__(
            code="NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


class ConflictError(BusGoError):
    def __init__(self, code: str, message: str, details: dict | None = None):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            details=details,
        )


class UnauthorizedError(BusGoError):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            code="UNAUTHORIZED",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class ForbiddenError(BusGoError):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(
            code="FORBIDDEN",
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
        )


def _error_response(
    request: Request,
    code: str,
    message: str,
    status_code: int,
    details: dict | None = None,
) -> JSONResponse:
    """Standard error envelope."""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "details": details or {},
            },
            "request_id": getattr(request.state, "request_id", None),
        },
    )


async def busgo_error_handler(request: Request, exc: BusGoError) -> JSONResponse:
    return _error_response(request, exc.code, exc.message, exc.status_code, exc.details)


async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return _error_response(
        request,
        code="VALIDATION_ERROR",
        message="Request validation failed.",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        details={"errors": exc.errors()},
    )


async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return _error_response(
        request,
        code="INTERNAL_ERROR",
        message="An unexpected error occurred.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )