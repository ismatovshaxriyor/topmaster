#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# One-time Let's Encrypt bootstrap for topmaster.ismatov.uz.
#
# Run ONCE on the server, from the repo root, AFTER the app stack is up
# (db/redis/minio/web) and DNS already points at this host:
#
#   LETSENCRYPT_EMAIL=you@example.com ./deploy/init-letsencrypt.sh
#
# Test first against staging to avoid hitting rate limits:
#   STAGING=1 LETSENCRYPT_EMAIL=you@example.com ./deploy/init-letsencrypt.sh
# ─────────────────────────────────────────────────────────────────
set -euo pipefail

DOMAIN="topmaster.ismatov.uz"
EMAIL="${LETSENCRYPT_EMAIL:-admin@ismatov.uz}"
STAGING="${STAGING:-0}"

COMPOSE="docker compose -f docker-compose.prod.yml"
CONF_DIR="./deploy/certbot/conf"
WWW_DIR="./deploy/certbot/www"
LIVE="$CONF_DIR/live/$DOMAIN"

mkdir -p "$LIVE" "$WWW_DIR"

# 1) Temporary self-signed cert so Nginx can start before the real one exists.
if [ ! -s "$LIVE/fullchain.pem" ]; then
  echo "→ Creating a temporary self-signed certificate so Nginx can boot..."
  docker run --rm -v "$(pwd)/deploy/certbot/conf:/etc/letsencrypt" certbot/certbot \
    openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
      -keyout "/etc/letsencrypt/live/$DOMAIN/privkey.pem" \
      -out "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" \
      -subj "/CN=$DOMAIN"
fi

# 2) Start Nginx (serves the ACME challenge over :80).
echo "→ Starting Nginx..."
$COMPOSE up -d nginx

# 3) Replace the dummy cert with a real Let's Encrypt certificate.
echo "→ Requesting the real certificate from Let's Encrypt..."
STAGING_FLAG=""
[ "$STAGING" = "1" ] && STAGING_FLAG="--staging"

docker run --rm \
  -v "$(pwd)/deploy/certbot/conf:/etc/letsencrypt" \
  -v "$(pwd)/deploy/certbot/www:/var/www/certbot" \
  certbot/certbot \
  sh -c "rm -rf /etc/letsencrypt/live/$DOMAIN /etc/letsencrypt/archive/$DOMAIN /etc/letsencrypt/renewal/$DOMAIN.conf; \
    certbot certonly --webroot -w /var/www/certbot $STAGING_FLAG \
      -d $DOMAIN --email '$EMAIL' --agree-tos --no-eff-email --non-interactive"

# 4) Reload Nginx so it picks up the real certificate.
echo "→ Reloading Nginx..."
$COMPOSE exec nginx nginx -s reload || $COMPOSE restart nginx

echo "✓ Done. Open https://$DOMAIN/health/ — it should be valid and return ok."
[ "$STAGING" = "1" ] && echo "  (STAGING cert is untrusted by browsers — re-run without STAGING=1 for production.)"
