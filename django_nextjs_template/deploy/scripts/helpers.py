import subprocess
from subprocess import PIPE
from scripts.constants import PROJECT_DOMAIN

def run_command(command: str):
    subprocess.run(command, shell=True, check=True)

def run_remote_commands(commands: list[str]):
    ssh_command = ['ssh', f'root@{PROJECT_DOMAIN}', "bash -s"]
    command = "\n".join(commands)
    p = subprocess.run(ssh_command, stdout=PIPE, input=command, encoding='ascii')
    if p.stdout:
        print(p.stdout)

def copy_to_remote(source: str, destination: str):
    run_command(f'scp {source} root@{PROJECT_DOMAIN}:{destination}')

def get_image_hash(image_name: str) -> str:
    command = ["docker", "inspect", "--format={{index .RepoDigests 0}}", image_name]
    p = subprocess.run(command, stdout=PIPE, encoding='ascii')
    if p.stdout:
        return p.stdout.strip()
    return ""

def print_status(msg: str):
    print(f"\033[0;32m{msg}\033[0m")
