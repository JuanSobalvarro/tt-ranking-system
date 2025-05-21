#!/bin/bash
docker-compose exec certbot certbot renew --webroot -w /var/www/certbot --quiet && \
docker exec nginx nginx -s reload
