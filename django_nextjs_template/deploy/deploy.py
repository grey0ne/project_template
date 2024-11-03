from scripts.commands import (
    INIT_SWARM_SCRIPT, PERFORM_MIGRATIONS, COLLECT_STATIC_SCRIPT,
    BUILD_IMAGES_SCRIPT, UPDATE_SWARM_SCRIPT
)
from scripts.helpers import run_command, run_remote_commands, copy_to_remote
from scripts.constants import DEPLOY_DIR, PROD_APP_PATH, PROJECT_DOMAIN
from scripts.release import release

COMPOSE_DIR = f'{DEPLOY_DIR}/compose'
ENV_FILE = f'{DEPLOY_DIR}/env.prod'

def print_status(msg: str):
    print(f"\033[0;32m{msg}\033[0m")

#run_remote_commands([f"mkdir -p /app/balancer", ])
#copy_to_remote(f'{DEPLOY_DIR}/compose/prod_balancer.yml', '/app/balancer/compose.yml')

release()

run_command(COLLECT_STATIC_SCRIPT)
run_command(BUILD_IMAGES_SCRIPT)

print_status(f"Deploying to {PROJECT_DOMAIN}")
run_remote_commands([f"mkdir -p {PROD_APP_PATH}", ])
print_status(f"Copiyng compose files to {PROJECT_DOMAIN}")
run_command(f"envsubst < {COMPOSE_DIR}/prod.yml.template > {COMPOSE_DIR}/prod.yml")
copy_to_remote(f'{COMPOSE_DIR}/prod.yml', f'{PROD_APP_PATH}/prod.yml')
run_command(f"rm {COMPOSE_DIR}/prod.yml")

copy_to_remote(f"{DEPLOY_DIR}/prod-scripts/certbot_renew.sh", "/etc/cron.daily")
print_status(f"Copiyng env files to {PROJECT_DOMAIN}")
copy_to_remote(f"{DEPLOY_DIR}/env.base", f"{PROD_APP_PATH}/env.base")
copy_to_remote(ENV_FILE, f"{PROD_APP_PATH}/env")
run_remote_commands([INIT_SWARM_SCRIPT, PERFORM_MIGRATIONS, UPDATE_SWARM_SCRIPT])
run_remote_commands([PERFORM_MIGRATIONS, ])