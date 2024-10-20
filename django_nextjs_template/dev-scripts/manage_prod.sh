#!/bin/bash

set -a
source ./env.base
source ./env

docker run --rm -i --env-file=env.base --env-file=env $REGISTRY_HOSTNAME/$REGISTRY_NAMESPACE/$PROJECT_NAME-django python manage.py ${@:1}