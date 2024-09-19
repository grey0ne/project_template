#!/bin/bash

set -e

ENV_FILE=$1

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

function print_status () {
    echo -e "${GREEN}$1${NC}" >&2
}

function print_error () {
    echo -e "${RED}$1${NC}" >&2
}

function build_image () {
    set -e
    print_status "Building $1"
    docker build --secret id=sentry_auth,env=SENTRY_AUTH_TOKEN  -t $REGISTRY_HOSTNAME/$PROJECT_NAME-$1 -f $2 $3  --platform linux/amd64
    BUILD_RESULT_STATUS=$?
    if [ ${BUILD_RESULT_STATUS} -ne 0 ]; then
        print_error "$1 Build failed!"
        exit "${BUILD_RESULT_STATUS}"
    fi
    local RESULT=$(docker inspect --format='{{index .RepoDigests 0}}' $REGISTRY_HOSTNAME/$PROJECT_NAME-$1)
    print_status "$1 image hash: $RESULT"
    echo $RESULT
}

source dev-scripts/env.base
source $ENV_FILE

DEPLOY_HOSTNAME=$PROJECT_DOMAIN

print_status "Collecting static files for django"
docker run --rm -i --env-file=./dev-scripts/env.base --env-file=./dev-scripts/env.dev -e BUILD_STATIC=true -v ./backend:/app/src $PROJECT_NAME-django python manage.py collectstatic --noinput
print_status "Building images"
export DOCKER_CLI_HINTS="false"
export NGINX_IMAGE=$(build_image "nginx" "nginx/Dockerfile" ".")
rm -rf backend/static
export DJANGO_IMAGE=$(build_image "django" "backend/Dockerfile.prod" "backend")
cd spa
npm run build
export NEXTJS_IMAGE=$(build_image "nextjs" "spa/Dockerfile.prod" "spa")
print_status "$NEXTJS_IMAGE"

print_status "Loggin in to $REGISTRY_HOSTNAME"
echo $REGISTRY_PASSWORD | docker login $REGISTRY_HOSTNAME --username $REGISTRY_USERNAME --password-stdin

print_status "Pushing images to registry"
docker push $REGISTRY_HOSTNAME/$PROJECT_NAME-django
docker push $REGISTRY_HOSTNAME/$PROJECT_NAME-nextjs
docker push $REGISTRY_HOSTNAME/$PROJECT_NAME-nginx

print_status "Deploying to $DEPLOY_HOSTNAME"
ssh root@$DEPLOY_HOSTNAME "mkdir -p /app/$PROJECT_NAME"
print_status "Copiyng compose files to $DEPLOY_HOSTNAME"
envsubst '$DJANGO_IMAGE $NGINX_IMAGE $NEXTJS_IMAGE' < docker/prod.yml > docker/prod.yml.tmp
scp dev-scripts/certbot_renew.sh root@$DEPLOY_HOSTNAME:/etc/cron.daily
scp docker/common.yml root@$DEPLOY_HOSTNAME:/app/$PROJECT_NAME
scp docker/prod.yml.tmp root@$DEPLOY_HOSTNAME:/app/$PROJECT_NAME/prod.yml
rm docker/prod.yml.tmp
print_status "Copiyng env files to $DEPLOY_HOSTNAME"
scp dev-scripts/env.base root@$DEPLOY_HOSTNAME:/app/$PROJECT_NAME/env.base
scp $ENV_FILE root@$DEPLOY_HOSTNAME:/app/$PROJECT_NAME/env
print_status "Copiyng scripts to $DEPLOY_HOSTNAME"
scp dev-scripts/swarm_deploy.sh dev-scripts/manage_prod.sh root@$DEPLOY_HOSTNAME:/app/$PROJECT_NAME
ssh root@$DEPLOY_HOSTNAME "cd /app/$PROJECT_NAME && ./swarm_deploy.sh"