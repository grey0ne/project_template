from scripts.helpers import run_remote_commands, print_status
from scripts.commands import SETUP_CERTBOT, SETUP_DOCKER, PROJECT_DOMAIN, GEN_FAKE_CERTS

run_remote_commands([
    f"mkdir -p /app/certbot/certificates",
    f"mkdir -p /app/certbot/challenge",
])
print_status("Setting up docker")
run_remote_commands([ SETUP_DOCKER, ])
print_status(f"Setting up certbot for domain {PROJECT_DOMAIN}")
run_remote_commands([ SETUP_CERTBOT, ])
print_status(f"Copying fake certs to dummy folder")
run_remote_commands([ GEN_FAKE_CERTS, ])
