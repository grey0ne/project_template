from scripts.commands import (
    INIT_SWARM_SCRIPT, PERFORM_MIGRATIONS, COLLECT_STATIC_SCRIPT,
    BUILD_IMAGES_SCRIPT, UPDATE_SWARM_SCRIPT, RELOAD_NGINX
)
from scripts.helpers import run_command, run_remote_commands, copy_to_remote, print_status, get_image_hash
from scripts.constants import DEPLOY_DIR, PROD_APP_PATH, PROJECT_DOMAIN, COMPOSE_DIR, DOCKER_IMAGE_PREFIX, PROJECT_NAME
from scripts.release import release
import os

ENV_FILE = f'{DEPLOY_DIR}/env.prod'


release()

run_command(COLLECT_STATIC_SCRIPT)
run_command(BUILD_IMAGES_SCRIPT)

os.environ['DJANGO_IMAGE'] = get_image_hash(f'{DOCKER_IMAGE_PREFIX}-django')
os.environ['NEXTJS_IMAGE'] = get_image_hash(f'{DOCKER_IMAGE_PREFIX}-nextjs')

run_command(f'envsubst < {COMPOSE_DIR}/prod.yml.template > {COMPOSE_DIR}/prod.yml')

print_status(f"Deploying to {PROJECT_DOMAIN}")
run_remote_commands([f"mkdir -p {PROD_APP_PATH}", ])
print_status(f"Copiyng compose files to {PROJECT_DOMAIN}")
copy_to_remote(f'{COMPOSE_DIR}/prod.yml', f'{PROD_APP_PATH}/prod.yml')
run_command(f"rm {COMPOSE_DIR}/prod.yml")

copy_to_remote(f"{DEPLOY_DIR}/prod-scripts/certbot_renew.sh", "/etc/cron.daily")

print_status(f"Copiyng env files to {PROJECT_DOMAIN}")
copy_to_remote(f"{DEPLOY_DIR}/env.base", f"{PROD_APP_PATH}/env.base")
copy_to_remote(ENV_FILE, f"{PROD_APP_PATH}/env")
run_remote_commands([INIT_SWARM_SCRIPT, PERFORM_MIGRATIONS])
run_remote_commands([UPDATE_SWARM_SCRIPT, ])

run_command(f"envsubst '$PROJECT_NAME,$PROJECT_DOMAIN' < {DEPLOY_DIR}/nginx/conf/nginx_prod.template > {DEPLOY_DIR}/nginx/conf/{PROJECT_NAME}.conf")
copy_to_remote(f'{DEPLOY_DIR}/nginx/conf/{PROJECT_NAME}.conf', f'/app/balancer/conf/{PROJECT_NAME}.conf')
run_command(f"rm {DEPLOY_DIR}/nginx/conf/{PROJECT_NAME}.conf")
run_remote_commands([RELOAD_NGINX, ])