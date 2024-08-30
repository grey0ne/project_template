#!/bin/bash

set -a
source ./env.base
source ./env

docker run --rm -i --env-file=env.base --env-file=env registry.meta-game.io/metagame-django python manage.py ${@:1}