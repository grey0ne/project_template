#!/bin/bash

set -e

ENV_FILE=$1

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_DIR=$(pwd)
DEPLOY_DIR="$PROJECT_DIR/deploy"
COMPOSE_DIR="$DEPLOY_DIR/compose"

function print_status () {
    echo -e "${GREEN}$1${NC}" >&2
}

function print_error () {
    echo -e "${RED}$1${NC}" >&2
}


function build_image () {
    set -e
    print_status "Building $1"
    docker build --secret id=sentry_auth,env=SENTRY_AUTH_TOKEN  -t $DOCKER_IMAGE_PREFIX-$1 -f $2 $3  --platform linux/amd64
    BUILD_RESULT_STATUS=$?
    if [ ${BUILD_RESULT_STATUS} -ne 0 ]; then
        print_error "$1 Build failed!"
        exit "${BUILD_RESULT_STATUS}"
    fi
    local RESULT=$(docker inspect --format='{{index .RepoDigests 0}}' $DOCKER_IMAGE_PREFIX-$1)
    print_status "$1 image hash: $RESULT"
    echo $RESULT
}

DOCKER_IMAGE_PREFIX="$REGISTRY_HOSTNAME/$REGISTRY_NAMESPACE/$PROJECT_NAME"
DEPLOY_HOSTNAME=$PROJECT_DOMAIN

print_status "Collecting static files for django"
docker run --rm -i --env-file=$DEPLOY_DIR/env.base --env-file=$DEPLOY_DIR/env.prod -e BUILD_STATIC=true -v ./backend:/app/src $PROJECT_NAME-django python manage.py collectstatic --noinput
print_status "Building images"
export DOCKER_CLI_HINTS="false"
export NGINX_IMAGE=$(build_image "nginx" "deploy/nginx/Dockerfile" ".")
rm -rf backend/static
export DJANGO_IMAGE=$(build_image "django" "backend/Dockerfile.prod" "backend")
cd spa
npm run build
cd ../
export NEXTJS_IMAGE=$(build_image "nextjs" "spa/Dockerfile.prod" "spa")
print_status "$NEXTJS_IMAGE"

print_status "Loggin in to $REGISTRY_HOSTNAME"
echo $REGISTRY_PASSWORD | docker login $REGISTRY_HOSTNAME --username $REGISTRY_USERNAME --password-stdin

print_status "Pushing images to registry"
docker push $DOCKER_IMAGE_PREFIX-django
docker push $DOCKER_IMAGE_PREFIX-nextjs
docker push $DOCKER_IMAGE_PREFIX-nginx

print_status "Deploying to $DEPLOY_HOSTNAME"
ssh root@$DEPLOY_HOSTNAME "mkdir -p /app/$PROJECT_NAME"
print_status "Copiyng compose files to $DEPLOY_HOSTNAME"
envsubst < $COMPOSE_DIR/prod.yml.template > $COMPOSE_DIR/prod.yml
scp $DEPLOY_DIR/prod-scripts/certbot_renew.sh root@$DEPLOY_HOSTNAME:/etc/cron.daily
scp $COMPOSE_DIR/prod.yml root@$DEPLOY_HOSTNAME:/app/$PROJECT_NAME/prod.yml
rm $COMPOSE_DIR/prod.yml
print_status "Copiyng env files to $DEPLOY_HOSTNAME"
scp $DEPLOY_DIR/env.base root@$DEPLOY_HOSTNAME:/app/$PROJECT_NAME/env.base
scp $ENV_FILE root@$DEPLOY_HOSTNAME:/app/$PROJECT_NAME/env
print_status "Copiyng scripts to $DEPLOY_HOSTNAME"
scp $DEPLOY_DIR/prod-scripts/swarm_deploy.sh $DEPLOY_DIR/prod-scripts/manage_prod.sh root@$DEPLOY_HOSTNAME:/app/$PROJECT_NAME
ssh root@$DEPLOY_HOSTNAME "cd /app/$PROJECT_NAME && ./swarm_deploy.sh"