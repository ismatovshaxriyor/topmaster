#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# One-time Let's Encrypt bootstrap for topmaster.ismatov.uz.
#
# Strategy: start Nginx with a temporary HTTP-only config (needs no certificate)
# so it can answer the ACME challenge on :80, obtain the certificate, then swap
# back to the full TLS config. No dummy cert, no crash loop.
#
# Run ONCE on the server, from the repo root, AFTER db/redis/minio/web are up
# and DNS already points at this host:
#
#   sudo LETSENCRYPT_EMAIL=you@example.com ./deploy/init-letsencrypt.sh
#
# Test against staging first (avoids rate limits):
#   sudo STAGING=1 LETSENCRYPT_EMAIL=you@example.com ./deploy/init-letsencrypt.sh
# ─────────────────────────────────────────────────────────────────
set -euo pipefail

DOMAIN="topmaster.ismatov.uz"
EMAIL="${LETSENCRYPT_EMAIL:-admin@ismatov.uz}"
STAGING="${STAGING:-0}"

COMPOSE="docker compose -f docker-compose.prod.yml"
CONFD="./deploy/nginx/conf.d"
CONF_DIR="./deploy/certbot/conf"
WWW_DIR="./deploy/certbot/www"

mkdir -p "$CONF_DIR" "$WWW_DIR"

# 0) Recover from any interrupted previous run.
[ -f "$CONFD/topmaster.conf.disabled" ] && [ ! -f "$CONFD/topmaster.conf" ] && \
  mv "$CONFD/topmaster.conf.disabled" "$CONFD/topmaster.conf"
rm -f "$CONFD/bootstrap.conf"

restore_full_config() {
  rm -f "$CONFD/bootstrap.conf"
  [ -f "$CONFD/topmaster.conf.disabled" ] && \
    mv "$CONFD/topmaster.conf.disabled" "$CONFD/topmaster.conf"
}

# 1) Swap in a temporary HTTP-only config (no TLS → Nginx starts without a cert).
echo "→ Switching Nginx to a temporary HTTP-only config..."
[ -f "$CONFD/topmaster.conf" ] && mv "$CONFD/topmaster.conf" "$CONFD/topmaster.conf.disabled"
cat > "$CONFD/bootstrap.conf" <<EOF
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN;
    location /.well-known/acme-challenge/ { root /var/www/certbot; }
    location / { return 200 'bootstrap ok'; add_header Content-Type text/plain; }
}
EOF
# On any later failure, always put the real config back.
trap restore_full_config EXIT

# 2) (Re)start Nginx with the bootstrap config so :80 is served reliably.
echo "→ Starting Nginx (HTTP-only)..."
$COMPOSE up -d --force-recreate nginx
sleep 3

# 3) Clean any leftover/empty cert lineage, then request the real certificate.
echo "→ Requesting the certificate from Let's Encrypt..."
rm -rf "$CONF_DIR/live/$DOMAIN" "$CONF_DIR/archive/$DOMAIN" "$CONF_DIR/renewal/$DOMAIN.conf"
STAGING_FLAG=""
[ "$STAGING" = "1" ] && STAGING_FLAG="--staging"

docker run --rm \
  -v "$(pwd)/deploy/certbot/conf:/etc/letsencrypt" \
  -v "$(pwd)/deploy/certbot/www:/var/www/certbot" \
  certbot/certbot certonly --webroot -w /var/www/certbot $STAGING_FLAG \
    -d "$DOMAIN" --email "$EMAIL" --agree-tos --no-eff-email --non-interactive

# 4) Restore the full TLS config and recreate Nginx with the real certificate.
echo "→ Restoring full TLS config and reloading Nginx..."
restore_full_config
trap - EXIT
$COMPOSE up -d --force-recreate nginx

echo "✓ Done. Open https://$DOMAIN/health/ — it should be valid and return ok."
[ "$STAGING" = "1" ] && echo "  (STAGING cert is untrusted by browsers — re-run without STAGING=1 for production.)"
