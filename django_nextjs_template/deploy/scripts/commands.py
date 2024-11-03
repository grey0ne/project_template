from scripts.constants import (
    REGISTRY_PASSWORD, REGISTRY_HOSTNAME, REGISTRY_USERNAME,
    DOCKER_IMAGE_PREFIX, PROD_APP_PATH, DEPLOY_DIR, PROJECT_NAME, PROJECT_DIR
)

PRINT_COMMAND = """
    GREEN='\033[0;32m'
    RED='\033[0;31m'
    NC='\033[0m'

    function print_status () {
        echo "${GREEN}$1${NC}"
    }

    function print_error () {
        echo "${RED}$1${NC}" >&2
    }
"""

GET_ADDR = """
for ADDR in $(ip addr show "eth0" | awk '/inet / {print $2}')
do
    if [[ $ADDR == *16 ]]
    then
        RESULT_ADDR=${ADDR::-3}
    fi
done
"""

LOGIN_REGISTRY = f"""
{PRINT_COMMAND}
print_status "Login to registry"
echo {REGISTRY_PASSWORD} | docker login {REGISTRY_HOSTNAME} --username {REGISTRY_USERNAME} --password-stdin
"""

JOIN_SWARM = """
if [ "$(docker info --format '{{.Swarm.LocalNodeState}}')" = "active" ]; then
    print_status "Swarm already initialized"
else
    print_status "Initializing swarm"
    docker swarm init --advertise-addr $RESULT_ADDR
fi
"""

PERFORM_MIGRATIONS = f"""
{PRINT_COMMAND}
print_status "Update image for migrations"
docker pull {DOCKER_IMAGE_PREFIX}-django
print_status "Perform migrations"
docker run --rm -i --env-file={PROD_APP_PATH}/env.base --env-file={PROD_APP_PATH}/env {DOCKER_IMAGE_PREFIX}-django python manage.py migrate
"""

INIT_SWARM_SCRIPT = f"""
{PRINT_COMMAND}
{GET_ADDR}
{LOGIN_REGISTRY}
{JOIN_SWARM}
"""

UPDATE_SWARM_SCRIPT = f"""
{PRINT_COMMAND}
print_status "Update swarm"
docker stack config -c {PROD_APP_PATH}/prod.yml | docker stack deploy --with-registry-auth --detach=false -c - {PROJECT_NAME}
print_status "Prune images"
docker image prune -f
print_status "Deploy completed"
"""

COLLECT_STATIC_SCRIPT = PRINT_COMMAND + f"""
print_status "Collecting static files for django"
docker run --rm -i --env-file={DEPLOY_DIR}/env.base --env-file={DEPLOY_DIR}/env.prod -e BUILD_STATIC=true -v ./backend:/app/src {PROJECT_NAME}-django python manage.py collectstatic --noinput
"""

CHECK_BUILD_STATUS = """
    BUILD_RESULT_STATUS=$?
    if [ ${BUILD_RESULT_STATUS} -ne 0 ]; then
        print_error "$1 Build failed!"
        exit "${BUILD_RESULT_STATUS}"
    fi
"""
BUILD_IMAGE_COMMAND = PRINT_COMMAND + """
function build_image () {
""" + f"""
    set -e
    print_status "Building $1"
    docker build --secret id=sentry_auth,env=SENTRY_AUTH_TOKEN  -t {DOCKER_IMAGE_PREFIX}-$1 -f $2 $3  --platform linux/amd64
    {CHECK_BUILD_STATUS}
    print_status "$1 image hash: $RESULT"
    echo $RESULT
""" + """
}
"""


BUILD_IMAGES_SCRIPT = f"""
{PRINT_COMMAND}
{BUILD_IMAGE_COMMAND}

print_status "Building images"
export DOCKER_CLI_HINTS="false"
export DJANGO_IMAGE=$(build_image "django" "{PROJECT_DIR}/backend/Dockerfile.prod" "backend")
cd {PROJECT_DIR}/spa
npm run build
cd {PROJECT_DIR}
export NEXTJS_IMAGE=$(build_image "nextjs" "{PROJECT_DIR}/spa/Dockerfile.prod" "spa")
print_status "$NEXTJS_IMAGE"

{LOGIN_REGISTRY}
print_status "Pushing images to registry"
docker push {DOCKER_IMAGE_PREFIX}-django
docker push {DOCKER_IMAGE_PREFIX}-nextjs
""" 


RELOAD_NGINX = f"""
NGINX_CONTAINER=$(docker ps -q -f name=nginx)
docker exec $NGINX_CONTAINER nginx -s reload
"""