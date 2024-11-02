from scripts.constants import REGISTRY_PASSWORD, REGISTRY_HOSTNAME, REGISTRY_USERNAME

PRINT_COMMAND = """
    GREEN='\033[0;32m'
    NC='\033[0m'

    function print_status () {
        echo -e "${GREEN}$1${NC}"
    }
"""

INIT_SWARM = PRINT_COMMAND + """
for ADDR in $(ip addr show "eth0" | awk '/inet / {print $2}')
do
    if [[ $ADDR == *16 ]]
    then
        RESULT_ADDR=${ADDR::-3}
    fi
done

print_status "Login to registry"
""" + f"""
echo {REGISTRY_PASSWORD} | docker login {REGISTRY_HOSTNAME} --username {REGISTRY_USERNAME} --password-stdin
""" + """
if [ "$(docker info --format '{{.Swarm.LocalNodeState}}')" = "active" ]; then
    print_status "Swarm already initialized"
else
    print_status "Initializing swarm"
    docker swarm init --advertise-addr $RESULT_ADDR
fi
"""

