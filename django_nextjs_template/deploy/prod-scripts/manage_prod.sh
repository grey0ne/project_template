#!/bin/bash

set -a
source ./env.base
source ./env

DOCKER_IMAGE_PREFIX="$REGISTRY_HOSTNAME/$REGISTRY_NAMESPACE/$PROJECT_NAME"

docker run --rm -i --env-file=env.base --env-file=env $DOCKER_IMAGE_PREFIX-django python manage.py ${@:1}