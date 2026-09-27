"""Testing settings — fast, isolated, no external deps."""
from __future__ import annotations

from .base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = ["testserver"]

# In-memory SQLite for fast tests.
# Note: some PostgreSQL-specific features won't work.
# Integration tests will override this.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Fast password hashing
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Fast JWT (HS256 for tests)
SIMPLE_JWT["ALGORITHM"] = "HS256"  # type: ignore[index]
SIMPLE_JWT["SIGNING_KEY"] = "test-secret"  # type: ignore[index]

# Email — locmem
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Disable throttling in tests
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []  # type: ignore[index]