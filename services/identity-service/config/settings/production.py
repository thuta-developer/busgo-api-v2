"""Production settings — hardened."""
from __future__ import annotations

import os

from .base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if h.strip()
]

# Security headers
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# CORS — explicit only
CORS_ALLOW_ALL_ORIGINS = False

# Email — real backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# JSON logs
LOGGING["handlers"]["console"]["formatter"] = "json"  # type: ignore[index]