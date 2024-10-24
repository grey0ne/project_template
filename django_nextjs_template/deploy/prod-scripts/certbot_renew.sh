#!/bin/bash

CERTS_VOLUME=certbot-certificates
CHALLENGE_VOLUME=certbot-challenge
NGINX_CONTAINER=registry-nginx

docker run --rm --name temp_certbot -v $CERTS_VOLUME:/etc/letsencrypt -v $CHALLENGE_VOLUME:/tmp/letsencrypt certbot/certbot:v1.14.0 renew --webroot --agree-tos --no-random-sleep-on-renew -w /tmp/letsencrypt
docker exec $NGINX_CONTAINER nginx -s reload
