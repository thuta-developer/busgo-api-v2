"""Development settings."""
from __future__ import annotations

from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Allow localhost origins
CORS_ALLOW_ALL_ORIGINS = True

# Verbose logging
LOGGING["root"]["level"] = "DEBUG"  # type: ignore[index]

# Email — console backend in dev
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"