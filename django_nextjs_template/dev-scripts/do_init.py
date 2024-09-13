import os
import urllib.error
import urllib.parse
import urllib.request
import json
import fileinput
import time
from typing import Any, NamedTuple

DO_TOKEN = os.getenv("DO_TOKEN", '')
OS_IMAGE = os.getenv("DO_OS_IMAGE", "debian-12-x64")
REGION = os.getenv("DO_REGION", "ams3")
DROPLET_SIZE = os.getenv("DO_SIZE", "s-1vcpu-1gb")
SSH_FINGERPRINT = os.getenv("DO_KEY_FINGERPRINT")
DROPLET_TAGS = ["auto-created"]
DOMAIN = os.getenv("PROJECT_DOMAIN", '')
PG_NODES_NUM = 1
PG_VERSION = "14"
PG_SIZE = "db-s-1vcpu-1gb"
PG_STORAGE_SIZE = 15000 # 15GB
PG_CLUSTER_NAME = os.getenv("DATABASE_CLUSTER", "communal-db")
PG_USERNAME = os.getenv("DATABASE_USER", '')
PROJECT_NAME = os.getenv("PROJECT_NAME", '')
PROJECT_DESCRIPTION = f"{PROJECT_NAME} project"
DROPLET_NAME = f"{PROJECT_NAME}-app"
STATUS_CHECK_INTERVAL = 1 # in seconds

DO_API_DOMAIN = "https://api.digitalocean.com"
DROPLETS_URL = f"{DO_API_DOMAIN}/v2/droplets"

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROD_ENV_FILE = os.path.join(SCRIPTS_DIR, 'env.prod')

DO_HEADERS = {
    "Authorization": f"Bearer {DO_TOKEN}",
    "Content-Type": "application/json"
}


class Response(NamedTuple):
    body: str
    headers: dict[str, str]
    status: int
    error_count: int = 0

    def json(self) -> Any:
        """
        Decode body's JSON.

        Returns:
            Pythonic representation of the JSON object
        """
        try:
            output = json.loads(self.body)
        except json.JSONDecodeError:
            output = ""
        return output


def request(
    url: str,
    data: dict[str, Any] = {},
    params: dict[str, Any] = {},
    headers: dict[str, str] = {},
    method: str = "GET",
    data_as_json: bool = True,
    error_count: int = 0,
) -> Response:
    # HTTP Request based on urllib to get rid of external dependencies
    if not url.casefold().startswith("http"):
        raise urllib.error.URLError("Incorrect and possibly insecure protocol in url")
    method = method.upper()
    request_data = None
    headers = headers or {}
    data = data or {}
    params = params or {}
    headers = {"Accept": "application/json", **headers}

    if method == "GET":
        params = {**params, **data}
        data = {}

    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True, safe="/")

    if data:
        if data_as_json:
            request_data = json.dumps(data).encode()
            headers["Content-Type"] = "application/json; charset=UTF-8"
        else:
            request_data = urllib.parse.urlencode(data).encode()

    httprequest = urllib.request.Request(
        url, data=request_data, headers=headers, method=method
    )

    try:
        with urllib.request.urlopen(httprequest) as httpresponse:
            response = Response(
                headers=httpresponse.headers,
                status=httpresponse.status,
                body=httpresponse.read().decode(
                    httpresponse.headers.get_content_charset("utf-8")
                ),
            )
    except urllib.error.HTTPError as e:
        response = Response(
            body=str(e.reason),
            headers=dict(e.headers),
            status=e.code,
            error_count=error_count + 1,
        )

    return response

class DOException(Exception):
    pass


def save_env_option(option_name: str, value: str):
    with fileinput.input(files=(PROD_ENV_FILE, ), encoding="utf-8", inplace=True) as f:
        for line in f:
            if f'{option_name}=' in line:
                result = f'{option_name}={value}\n'
            else:
                result = line
            print(result, end='')


def do_get_request(url: str) -> dict[str, Any]:
    response = request(url=url, method="GET", headers=DO_HEADERS)
    if response.status != 200:
        raise DOException(f"DO request failed. Status code: {response.status} Body: {response.body}")
    return response.json()


def do_post_request(url: str, data: dict[str, Any] = {}) -> dict[str, Any]:
    response = request(url=url, method="POST", headers=DO_HEADERS, data=data)
    if response.status not in [202, 201, 200]:
        raise DOException(f"DO request failed. Status code: {response.status} Body: {response.body}")
    return response.json()

def get_existing_project(name: str) -> dict[str, Any] | None:
    url = f"{DO_API_DOMAIN}/v2/projects?name={name}"
    data = do_get_request(url)
    projects = data["projects"]
    if len(projects) > 0:
        return projects[0]

def get_or_create_project(name: str, description: str):
    existing_project = get_existing_project(name)
    if existing_project is not None:
        return existing_project
    url = f"{DO_API_DOMAIN}/v2/projects"
    project_data: dict[str, Any] = {
        "name": name,
        "description": description,
        "purpose": "Web Application",
        "environment": "Production"
    }
    response = do_post_request(url, project_data)
    return response["project"]

def get_existing_droplet(name: str) -> dict[str, Any] | None:
    url = f"{DROPLETS_URL}?name={name}"
    data = do_get_request(url)
    droplets = data["droplets"]
    if len(droplets) > 0:
        return droplets[0]


def create_droplet(name: str, project_id: str) -> dict[str, Any]:
    url = DROPLETS_URL
    data: dict[str, Any] = {
        "name": name,
        "region": REGION,
        "size": DROPLET_SIZE,
        "image": OS_IMAGE,
        "ssh_keys": [SSH_FINGERPRINT],
        "backups": False,
        "monitoring": True,
        "tags": DROPLET_TAGS,
        "ipv6": False,
        "with_droplet_agent": True,
        "project_id": project_id
    }
    response = do_post_request(url, data)
    return response['droplet']


def get_or_create_droplet(name: str, project_id: str):
    existing_droplet = get_existing_droplet(name)
    if existing_droplet is not None:
        print(f"Droplet {name} already exists")
        return existing_droplet
    print(f"Creating droplet {name}")
    return create_droplet(name, project_id)


def get_public_address(droplet_data: dict[str, Any]) -> str | None:
    networks = droplet_data["networks"]
    for network in networks["v4"]:
        if network["type"] == "public":
            return network["ip_address"]


def get_existing_pg_cluster(name: str):
    url = f"{DO_API_DOMAIN}/v2/databases?name={name}"
    data = do_get_request(url)
    databases = data["databases"]
    if databases is not None and len(databases) > 0:
        return databases[0]


def get_or_create_pg_cluster(name: str, project_id: str):
    existing_cluster = get_existing_pg_cluster(name)
    if existing_cluster is not None:
        return existing_cluster
    url = f"{DO_API_DOMAIN}/v2/databases"
    pg_cluster_data: dict[str, Any] = {
        "name": name,
        "engine": "pg",
        "num_nodes": PG_NODES_NUM,
        "region": REGION,
        "size": PG_SIZE,
        "version": PG_VERSION,
        "tags": ["auto-created"],
        "project_id": project_id
    }
    response = do_post_request(url, pg_cluster_data)
    return response['database']

def get_pg_user(cluster_id: str, username: str):
    url = f"{DO_API_DOMAIN}/v2/databases/{cluster_id}/users?name={username}"
    data = do_get_request(url)
    users = data["users"]
    if users is not None:
        for user in users:
            if user["name"] == username:
                return user

def get_or_create_pg_user(cluster_id: str, username: str):
    existing_user = get_pg_user(cluster_id, username)
    if existing_user is not None:
        return existing_user
    url = f"{DO_API_DOMAIN}/v2/databases/{cluster_id}/users"
    pg_user_data = {"name": username}
    result = do_post_request(url, pg_user_data)
    return result["user"]

def get_domain_records(domain: str):
    url = f"{DO_API_DOMAIN}/v2/domains/{domain}/records?type=A"
    response = do_get_request(url)
    return response


def create_domain_record(domain: str, droplet_ip: str):
    existing_records = get_domain_records(domain)
    for record in existing_records["domain_records"]:
        #TODO Remove existing incorrect records
        if record["data"] == droplet_ip:
            print(f"Record for {domain} pointing to {droplet_ip} already exists")
            return record
    url = f"{DO_API_DOMAIN}/v2/domains/{domain}/records"
    data: dict[str, Any] = {
        "type": "A",
        "name": "@",
        "data": droplet_ip,
        "priority": None,
        "port": None,
        "ttl": 1800,
        "weight": None,
        "flags": None,
        "tag": None
    }
    response = do_post_request(url, data)
    print(f"DNS record created for {domain} pointing to {droplet_ip}")
    return response["domain_record"]

REQUIRED_VARS: dict[str, str] = {
    'DO_TOKEN': DO_TOKEN,
    'PROJECT_NAME': PROJECT_NAME,
    'DOMAIN': DOMAIN,
    'DATABASE_USER': PG_USERNAME
}

def init_do_infra():
    for var_name, value in REQUIRED_VARS.items():
        if not value:
            print(f"{var_name} is not set")
            return
    project_data = get_or_create_project(PROJECT_NAME, PROJECT_DESCRIPTION)
    droplet_data = get_or_create_droplet(DROPLET_NAME, project_data["id"])
    public_address = get_public_address(droplet_data)
    while public_address is None:
        print(f"Droplet {DROPLET_NAME} does not have public IP address yet. Waiting")
        time.sleep(STATUS_CHECK_INTERVAL)
        droplet_data = get_existing_droplet(DROPLET_NAME)
        if droplet_data:
            public_address = get_public_address(droplet_data)
    print(f"Creating DNS record for droplet {DROPLET_NAME} with IP {public_address}")
    create_domain_record(DOMAIN, public_address)
    print("Public IP: ", public_address)
    pg_cluster = get_or_create_pg_cluster(PG_CLUSTER_NAME, project_data["id"])
    cluster_status = pg_cluster['status']
    cluster_id = pg_cluster['id']
    print("Postgres cluster status: ", pg_cluster["status"])
    save_env_option('DATABASE_HOST', pg_cluster['connection']['host'])
    while cluster_status == "creating":
        print("Postgres Cluster is still creating. Waiting")
        time.sleep(STATUS_CHECK_INTERVAL)
        pg_cluster = get_existing_pg_cluster(PG_CLUSTER_NAME)
        if pg_cluster is not None:
            cluster_status = pg_cluster['status']
    pg_user = get_or_create_pg_user(cluster_id, PG_USERNAME)
    if pg_user['password']:
        save_env_option('DATABASE_PASSWORD', pg_user['password'])


init_do_infra()