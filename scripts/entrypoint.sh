#!/usr/bin/env bash
# Wait for core services, optionally migrate, then run the given command.
set -euo pipefail

wait_for() {
    local host="$1" port="$2" name="$3"
    echo "Waiting for ${name} (${host}:${port})..."
    until nc -z "$host" "$port" 2>/dev/null; do
        sleep 1
    done
    echo "${name} is up."
}

DB_HOST="${POSTGRES_HOST:-db}"
DB_PORT="${POSTGRES_PORT:-5432}"
REDIS_HOST="$(echo "${REDIS_URL:-redis://redis:6379/0}" | sed -E 's#redis://([^:/]+).*#\1#')"

wait_for "$DB_HOST" "$DB_PORT" "PostgreSQL"
wait_for "$REDIS_HOST" "6379" "Redis"

if [ "${RUN_MIGRATIONS:-false}" = "true" ]; then
    echo "Applying database migrations..."
    python manage.py migrate --noinput
    echo "Collecting static files..."
    python manage.py collectstatic --noinput || true
    echo "Seeding reference data (cities, categories, FAQ)..."
    python manage.py seed_catalog || true
    python manage.py seed_support || true
fi

exec "$@"
