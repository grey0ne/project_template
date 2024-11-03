from scripts.constants import COMPOSE_DIR, DEPLOY_DIR
from scripts.helpers import run_remote_commands, copy_to_remote

run_remote_commands([
    f"mkdir -p /app/balancer",
    f"mkdir -p /app/balancer/conf",
])
copy_to_remote(f'{COMPOSE_DIR}/prod_balancer.yml', '/app/balancer/compose.yml')
copy_to_remote(f'{DEPLOY_DIR}/nginx/conf/balancer.conf', '/app/balancer/conf/default.conf')
BALANCER_STACK = "docker stack config -c /app/balancer/compose.yml | docker stack deploy --with-registry-auth --detach=false -c - balancer"
run_remote_commands([BALANCER_STACK, ])
