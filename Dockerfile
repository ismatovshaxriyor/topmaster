# ── TopMaster backend image ───────────────────────────────────────
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# System deps: build tools for psycopg/Pillow, netcat for wait scripts, curl for healthcheck.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        libjpeg-dev \
        zlib1g-dev \
        netcat-openbsd \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Python deps (cache layer).
COPY requirements.txt requirements-dev.txt ./
ARG INSTALL_DEV=true
RUN pip install -r requirements.txt && \
    if [ "$INSTALL_DEV" = "true" ]; then pip install -r requirements-dev.txt; fi

# Project source.
COPY . .

RUN chmod +x scripts/*.sh

EXPOSE 8000

ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
