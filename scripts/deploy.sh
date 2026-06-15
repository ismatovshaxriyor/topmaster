#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# Production (re)deploy. Run on the EC2 host — manually or via CI over SSH.
# Pulls latest code, rebuilds, and waits for the web container to be healthy.
# Migrations + collectstatic + reference seeding run automatically inside the
# web container's entrypoint (RUN_MIGRATIONS=true).
# ─────────────────────────────────────────────────────────────────
set -euo pipefail

# Always operate from the repo root, no matter where we're called from.
cd "$(dirname "$0")/.."

COMPOSE="docker compose -f docker-compose.prod.yml"

echo "→ Pulling latest code..."
git pull --ff-only

echo "→ Building and starting containers..."
$COMPOSE up -d --build --remove-orphans

echo "→ Waiting for the web container to become healthy..."
cid="$($COMPOSE ps -q web)"
for i in $(seq 1 40); do
    status="$(docker inspect --format '{{.State.Health.Status}}' "$cid" 2>/dev/null || echo starting)"
    if [ "$status" = "healthy" ]; then
        echo "  web is healthy."
        break
    fi
    if [ "$i" -eq 40 ]; then
        echo "✗ web did not become healthy in time. Recent logs:"
        $COMPOSE logs --tail 60 web
        exit 1
    fi
    sleep 3
done

echo "→ Pruning dangling images..."
docker image prune -f >/dev/null

echo "✓ Deploy complete."
$COMPOSE ps

# CI/CD smoke test — verifying the GitHub Actions → EC2 pipeline end-to-end.
