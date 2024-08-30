#!/bin/bash

CERTS_VOLUME=certbot-certificates
CHALLENGE_VOLUME=certbot-challenge

docker run --rm --name temp_certbot -v $CERTS_VOLUME:/etc/letsencrypt -v $CHALLENGE_VOLUME:/tmp/letsencrypt certbot/certbot:v1.14.0 renew --webroot --agree-tos --no-random-sleep-on-renew -w /tmp/letsencrypt
docker exec $(docker ps -q -f name=metagame_nginx) nginx -s reload
