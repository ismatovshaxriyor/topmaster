"""Development settings."""
from .base import *  # noqa: F401,F403
from .base import REST_FRAMEWORK

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Browsable API is handy in dev.
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
}

# Keep installed apps minimal-clean; django-extensions is optional in dev.
try:
    import django_extensions  # noqa: F401

    INSTALLED_APPS += ["django_extensions"]  # noqa: F405
except ImportError:
    pass

CORS_ALLOW_ALL_ORIGINS = True

INTERNAL_IPS = ["127.0.0.1"]

# Serve static straight from app/finders in dev — no collectstatic needed,
# and changes are picked up without restart.
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
