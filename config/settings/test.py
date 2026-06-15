"""Test settings.

Inherits dev but removes external-service dependencies so the suite runs
anywhere (no Redis / MinIO / SMTP needed) and is deterministic:

* in-memory cache  → throttling state is local & cleared per test (see conftest)
* in-memory email  → assert against ``mail.outbox``
* in-memory channels → no Redis for WebSocket layer
* local file storage → no MinIO for uploads
"""
from .dev import *  # noqa: F401,F403

# ── No external services ──────────────────────────────────────────
CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
}
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

# Uploads go to a temp filesystem dir, never MinIO.
USE_S3 = False
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# Hash faster — tests don't need PBKDF2's work factor.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Throttling stays ON (rates from base) so it is exercised by tests; the
# per-test cache clear in conftest keeps counters isolated. Individual tests
# tighten rates via @override_settings when asserting throttle behaviour.
