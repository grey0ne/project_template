#!/bin/bash

set -a
source ./env.base
source ./env

GREEN='\033[0;32m'
NC='\033[0m'

function print_status () {
    echo -e "${GREEN}$1${NC}"
}

for ADDR in $(ip addr show "eth0" | awk '/inet / {print $2}')
do
    if [[ $ADDR == *16 ]]
    then
        RESULT_ADDR=${ADDR::-3}
    fi
done

DOCKER_IMAGE_PREFIX="$REGISTRY_HOSTNAME/$REGISTRY_NAMESPACE/$PROJECT_NAME"

print_status "Login to registry"
echo $REGISTRY_PASSWORD | docker login $REGISTRY_HOSTNAME --username $REGISTRY_USERNAME --password-stdin
print_status "Init swarm"
docker swarm init --advertise-addr $RESULT_ADDR
cd /app/$PROJECT_NAME
print_status "Update image for migrations"
docker pull $DOCKER_IMAGE_PREFIX-django
print_status "Perform migrations"
docker run --rm -i --env-file=env.base --env-file=env $DOCKER_IMAGE_PREFIX-django python manage.py migrate
print_status "Update swarm"
docker stack config -c common.yml -c prod.yml | docker stack deploy --with-registry-auth --detach=false -c - $PROJECT_NAME
print_status "Prune images"
docker image prune -f
print_status "Deploy completed"