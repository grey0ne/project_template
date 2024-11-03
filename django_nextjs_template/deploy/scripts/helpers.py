import subprocess
from subprocess import PIPE
from scripts.constants import PROJECT_DOMAIN

def run_command(command: str):
    subprocess.run(command, shell=True, check=True)

def run_remote_commands(commands: list[str]):
    ssh_command = ['ssh', f'root@{PROJECT_DOMAIN}', "bash -s"]
    command = " && ".join(commands)
    p = subprocess.run(ssh_command, stdout=PIPE, input=command, encoding='ascii')
    if p.stdout:
        print(p.stdout)

def copy_to_remote(source: str, destination: str):
    run_command(f'scp {source} root@{PROJECT_DOMAIN}:{destination}')