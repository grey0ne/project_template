#!/bin/bash

if [ $# -eq 0 ] ; then
    echo "Provide hostname"
else
    DOMAIN=$1
    # Install Docker engine
    echo "Setting up docker"
    ssh root@$1 'bash -s' < deploy/setup_docker_debian.sh

    # Register domains in certbot
    echo "Setting up certbot for $DOMAIN"
    ssh root@$DOMAIN "export CERT_DOMAIN=$DOMAIN && bash -s" < deploy/init_certbot.sh
    scp deploy/certbot_renew.sh root@$DOMAIN:/etc/cron.daily
fi
