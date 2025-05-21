#!/bin/bash

domains=(ttranking.juso-software.com)
email="sobalvarrog_juans@gmail.com"  # CHANGE THIS
staging=0  # Set to 1 for testing/staging rate limits

# Create folders if needed
mkdir -p ./certbot/conf ./certbot/www

# Check if cert already exists
if [ -d "./certbot/conf/live/${domains[0]}" ]; then
  echo "Certificate for ${domains[0]} already exists. Skipping..."
else
  echo "### Requesting certificate for ${domains[*]} ..."

  docker-compose run --rm certbot certonly \
    --webroot -w /var/www/certbot \
    --email $email \
    --agree-tos \
    --no-eff-email \
    -d ${domains[@]} \
    $( [ $staging -ne 0 ] && echo "--staging" )

  echo "### Certificates created."
fi
