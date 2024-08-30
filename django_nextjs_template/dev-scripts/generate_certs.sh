#!/usr/bin/env bash

CERT_NAME=${1}
CERT_DOMAIN=${2}


# Define variables
BIN_OPENSSL=/usr/bin/openssl
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
LOCAL_CERT_PATH=${SCRIPT_DIR}/ssl
LOCAL_CERT_CERT=${LOCAL_CERT_PATH}/${CERT_NAME}.crt
LOCAL_CERT_KEY=${LOCAL_CERT_PATH}/${CERT_NAME}.key

echo "${CERT_NAME}"
echo "${CERT_DOMAIN}"

# Generate SSL certificate
mkdir -p ${LOCAL_CERT_PATH}
${BIN_OPENSSL} req -x509 -out ${LOCAL_CERT_CERT} -keyout ${LOCAL_CERT_KEY} \
-newkey rsa:2048 -nodes -sha256 \
-subj "/CN=${CERT_DOMAIN}" -extensions EXT \
-config <(printf "[dn]\nCN=${CERT_DOMAIN}\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS.1:${CERT_DOMAIN}\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")

# Show results
echo ""
echo "New SSL certificate was generated:"
echo "- Certificate: ${LOCAL_CERT_CERT}"
echo "- Key: ${LOCAL_CERT_KEY}"
echo ""

