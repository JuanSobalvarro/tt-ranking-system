#!/bin/bash

domains=(ttranking.juso-software.com)
email="sobalvarrog_juans@gmail.com"
staging=0 # Set to 1 for testing

mkdir -p ./certbot/conf ./certbot/www

if [ -d "./certbot/conf/live/${domains[0]}" ]; then
  echo "Certificate for ${domains[0]} already exists. Skipping..."
else
  echo "### Requesting certificate for ${domains[*]} ..."

  docker-compose run --rm certbot sh -c "certbot certonly \
    --webroot -w /var/www/certbot \
    --email $email \
    --agree-tos \
    --no-eff-email \
    -d ${domains[*]} \
    $( [ $staging -ne 0 ] && echo '--staging' )"

  echo "### Certificates created."
fi
