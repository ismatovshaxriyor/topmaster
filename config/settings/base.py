"""
TopMaster — base settings.
Shared across dev/prod. Environment-driven via django-environ.
"""
from datetime import timedelta
from pathlib import Path

import environ

# config/settings/base.py -> config/settings -> config -> <project root>
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "insecure-dev-key-change-me"),
    ALLOWED_HOSTS=(list, ["*"]),
    CORS_ALLOWED_ORIGINS=(list, []),
    CORS_ALLOW_ALL_ORIGINS=(bool, True),
)

# Read .env if present (compose passes real env vars in containers).
env_file = BASE_DIR / ".env"
if env_file.exists():
    env.read_env(str(env_file))

# ── Core ──────────────────────────────────────────────────────────
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# ── Applications ──────────────────────────────────────────────────
DJANGO_APPS = [
    "daphne",  # must precede staticfiles for ASGI runserver
    "jazzmin",  # must precede django.contrib.admin (overrides admin templates)
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "channels",
    "django_celery_beat",
    "django_celery_results",
    "storages",
    "auditlog",
]

LOCAL_APPS = [
    "apps.common",
    "apps.accounts",
    "apps.catalog",
    "apps.masters",
    "apps.jobs",
    "apps.proposals",
    "apps.reviews",
    "apps.chat",
    "apps.notifications",
    "apps.favorites",
    "apps.support",
    "apps.reports",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ── Middleware ────────────────────────────────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise serves static files (admin, DRF, Swagger UI) under ASGI/uvicorn,
    # which — unlike runserver — does not serve them itself. Must sit right after
    # SecurityMiddleware.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Captures the acting user on audited model changes (must follow auth).
    "auditlog.middleware.AuditlogMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ── Database ──────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="topmaster"),
        "USER": env("POSTGRES_USER", default="topmaster"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="topmaster"),
        "HOST": env("POSTGRES_HOST", default="db"),
        "PORT": env("POSTGRES_PORT", default="5432"),
        "CONN_MAX_AGE": 60,
    }
}

# ── Auth ──────────────────────────────────────────────────────────
AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ── i18n ──────────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

# ── Static & media ────────────────────────────────────────────────
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── DRF ───────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "apps.common.pagination.DefaultPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Global rate limiting (DoS / abuse protection). Sensitive endpoints add
    # stricter, scoped throttles on top (see apps.common.throttles).
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": "60/min",
        "user": "1000/min",
        "login": "10/min",
        "register": "5/min",
        "password_reset": "5/min",
        "support_send": "30/min",
        "report": "20/hour",
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env.int("JWT_ACCESS_MINUTES", default=60)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env.int("JWT_REFRESH_DAYS", default=14)),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "TopMaster API",
    "DESCRIPTION": "TopMaster — Oʻzbekiston xizmatlar marketplace backend API.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    # Drop DRF router APIRootView helpers (else they show under a stray "v1" tag).
    "PREPROCESSING_HOOKS": ["apps.common.openapi.exclude_api_root"],
}

# ── CORS ──────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = env("CORS_ALLOW_ALL_ORIGINS")
CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_CREDENTIALS = True

# ── Redis / Channels / Celery ─────────────────────────────────────
REDIS_URL = env("REDIS_URL", default="redis://redis:6379/0")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [env("CHANNELS_REDIS_URL", default="redis://redis:6379/1")]},
    }
}

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://redis:6379/2")
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("CACHE_REDIS_URL", default="redis://redis:6379/3"),
    }
}

# ── File storage (MinIO / S3-compatible) ──────────────────────────
USE_S3 = env.bool("USE_S3", default=True)

if USE_S3:
    AWS_ACCESS_KEY_ID = env("MINIO_ROOT_USER", default="topmaster")
    AWS_SECRET_ACCESS_KEY = env("MINIO_ROOT_PASSWORD", default="topmaster-secret")
    AWS_STORAGE_BUCKET_NAME = env("MINIO_BUCKET", default="topmaster-media")
    AWS_S3_ENDPOINT_URL = env("MINIO_ENDPOINT_URL", default="http://minio:9000")
    # Browser-facing base for media URLs. For MinIO path-style this MUST include
    # the bucket, e.g. "localhost:9000/topmaster-media". Protocol is separate.
    AWS_S3_CUSTOM_DOMAIN = env("MINIO_PUBLIC_DOMAIN", default=None)
    AWS_S3_URL_PROTOCOL = env("MINIO_URL_PROTOCOL", default="http:")
    AWS_S3_REGION_NAME = env("MINIO_REGION", default="us-east-1")
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = env.bool("MINIO_QUERYSTRING_AUTH", default=True)
    AWS_DEFAULT_ACL = None
    AWS_S3_ADDRESSING_STYLE = "path"  # required by MinIO
    STORAGES = {
        "default": {"BACKEND": "storages.backends.s3.S3Storage"},
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"
        },
    }
else:
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"
        },
    }

# ── Email (transactional only — password reset) ───────────────────
EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = env("EMAIL_HOST", default="mailpit")
EMAIL_PORT = env.int("EMAIL_PORT", default=1025)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="TopMaster <no-reply@topmaster.uz>")

# Front-end deep link the password-reset email points at. The SPA reads
# ?uid=&token= from it and POSTs them to /auth/password/reset/confirm/.
FRONTEND_PASSWORD_RESET_URL = env(
    "FRONTEND_PASSWORD_RESET_URL", default="https://topmaster.uz/reset-password"
)

# ── Firebase / FCM ────────────────────────────────────────────────
# Path to a service-account JSON, mounted into the container. When unset,
# push delivery is skipped gracefully (logged, not raised).
FIREBASE_CREDENTIALS_FILE = env("FIREBASE_CREDENTIALS_FILE", default="")

# ── Audit log (django-auditlog) ───────────────────────────────────
# Track the business-critical models only (not high-volume chat/notification
# rows). Each entry records who/when/what-changed for both admin and API
# writes; browse them in the admin under "Auditlog → Log entries".
AUDITLOG_INCLUDE_TRACKING_MODELS = (
    {"model": "accounts.User", "exclude_fields": ["password", "last_login"]},
    "accounts.UserSettings",
    "masters.MasterProfile",
    "masters.VerificationRequest",
    "jobs.Job",
    "proposals.Proposal",
    "reviews.Review",
    "catalog.Category",
    "catalog.City",
    "support.SupportThread",
    "reports.Report",
)

# ── Domain constants ──────────────────────────────────────────────
PLATFORM_COMMISSION_PERCENT = 10  # informational only — no payment processing

# ── Jazzmin admin theme ───────────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "TopMaster admin",
    "site_header": "TopMaster",
    "site_brand": "TopMaster",
    "site_logo": None,
    "welcome_sign": "TopMaster boshqaruv paneliga xush kelibsiz",
    "copyright": "TopMaster",
    "search_model": ["accounts.User", "masters.MasterProfile", "jobs.Job"],
    "user_avatar": "avatar",
    "topmenu_links": [
        {"name": "Bosh sahifa", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Analitika", "url": "admin-analytics", "permissions": ["auth.view_user"]},
        {"name": "API hujjatlari", "url": "/api/docs/", "new_window": True},
        {"name": "Foydalanuvchilar", "model": "accounts.User"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": [
        "accounts",
        "masters",
        "jobs",
        "proposals",
        "reviews",
        "chat",
        "notifications",
        "favorites",
        "catalog",
        "support",
        "reports",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.Group": "fas fa-users",
        "accounts.User": "fas fa-user",
        "accounts.Device": "fas fa-mobile-screen-button",
        "accounts.UserSettings": "fas fa-sliders",
        "catalog.City": "fas fa-city",
        "catalog.Category": "fas fa-tags",
        "masters.MasterProfile": "fas fa-screwdriver-wrench",
        "masters.Skill": "fas fa-toolbox",
        "masters.PortfolioItem": "fas fa-images",
        "masters.VerificationRequest": "fas fa-id-card",
        "masters.VerificationDocument": "fas fa-file-shield",
        "jobs.Job": "fas fa-briefcase",
        "jobs.JobImage": "fas fa-image",
        "jobs.JobEvent": "fas fa-timeline",
        "proposals.Proposal": "fas fa-file-signature",
        "reviews.Review": "fas fa-star",
        "chat.Conversation": "fas fa-comments",
        "chat.Message": "fas fa-message",
        "notifications.Notification": "fas fa-bell",
        "favorites.SavedMaster": "fas fa-heart",
        "support.FaqTopic": "fas fa-circle-question",
        "support.Faq": "fas fa-question",
        "support.SupportThread": "fas fa-headset",
        "support.SupportMessage": "fas fa-comment-dots",
        "reports.Report": "fas fa-flag",
        "auditlog.LogEntry": "fas fa-clipboard-list",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "language_chooser": False,
}

# Navy navbar + orange accent — TopMaster brand colours.
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-navy",
    "accent": "accent-warning",
    "navbar": "navbar-navy navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}
