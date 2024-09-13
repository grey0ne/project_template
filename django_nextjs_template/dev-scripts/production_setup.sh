#!/bin/bash

if [ $# -eq 0 ] ; then
    echo "Provide hostname"
else
    DOMAIN=$1
    # Install Docker engine
    echo "Setting up docker"
    ssh root@$1 'bash -s' < dev-scripts/setup_docker_debian.sh

    # Register domains in certbot
    echo "Setting up certbot for $DOMAIN"
    ssh root@$DOMAIN "export CERT_DOMAIN=$DOMAIN && bash -s" < dev-scripts/init_certbot.sh
    scp dev-scripts/certbot_renew.sh root@$DOMAIN:/etc/cron.daily
fi
