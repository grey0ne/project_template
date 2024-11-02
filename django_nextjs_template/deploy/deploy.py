import os
import subprocess
from subprocess import PIPE
from scripts.commands import INIT_SWARM
from scripts.constants import PROJECT_DOMAIN

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))


def run_command(command: str):
    subprocess.run(command, shell=True, check=True)

def run_remote_command(commands: list[str]):
    ssh_command = ['ssh', f'root@{PROJECT_DOMAIN}', "bash -s"]
    command = " && ".join(commands)
    p = subprocess.run(ssh_command, stdout=PIPE, input=command, encoding='ascii')
    if p.stdout:
        print(p.stdout)

run_remote_command([f"mkdir -p /app/balancer", INIT_SWARM])
run_command(f'scp {SCRIPTS_DIR}/compose/prod_balancer.yml root@{PROJECT_DOMAIN}:/app/balancer/compose.yml')