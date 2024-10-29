from do_utils import request, save_env_option
import os

CURRENT_VERION = int(os.getenv('PROJECT_VERSION', 1))

def release():
    next_version = CURRENT_VERION + 1
    save_env_option('PROJECT_VERSION', str(next_version))

release()