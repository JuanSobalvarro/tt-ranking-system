#!/bin/sh

CERT_PATH="/etc/letsencrypt/live/ttranking.juso-software.com/fullchain.pem"
TARGET_CONF="/etc/nginx/conf.d/default.conf"

# Decide which config to use
if [ -f "$CERT_PATH" ]; then
    echo "✅ SSL certificates found. Using nginx.conf (SSL enabled)."
    cp /etc/nginx/templates/ttranking.conf $TARGET_CONF
else
    echo "⚠️ No SSL certificates found. Using dummy.conf (HTTP only)."
    cp /etc/nginx/templates/dummy.conf $TARGET_CONF
fi

# Start Nginx
exec nginx -g 'daemon off;'
