#!/bin/bash

CERTS_VOLUME=/app/certbot/certificates

docker run --rm --name temp_certbot -p 80:80 -v $CERTS_VOLUME:/etc/letsencrypt certbot/certbot:v1.14.0 certonly --non-interactive --keep-until-expiring --standalone --preferred-challenges http --agree-tos --text --email sergey.lihobabin@gmail.com -d $CERT_DOMAIN
