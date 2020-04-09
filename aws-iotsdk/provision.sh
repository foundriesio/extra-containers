#!/bin/sh

# create the device certificate
#
# On the first connection attempt, it will trigger the aws thing creation,
# registration and so forth 

CA=${1:-root}
CERT_DIR=${2:-/certs}
PROV_DIR=${3:-/prov}
ENDPOINT=${4:-ats.iot.us-east-1.amazonaws.com}

# TODO: support pulling in serial # for static naming
DEVICE_UUID=$(uuidgen)
DEVICE_NAME="fio-aws-${DEVICE_UUID}"

echo "[provision] Device name: ${DEVICE_NAME}"
echo "${DEVICE_NAME}" > "${PROV_DIR}/thing_name"
echo "[provision] Generating device key: ${PROV_DIR}/device.key"
openssl genrsa -out "${PROV_DIR}/device.key" 2048
echo "[provision] Generating device csr: ${PROV_DIR}/device.csr"
openssl req -new -key "${PROV_DIR}/device.key" -out "${PROV_DIR}/device.csr"  -subj "/CN=${DEVICE_NAME}"
echo "[provision] Generating device certificate: ${PROV_DIR}/device.crt"
openssl x509 -req -in "${PROV_DIR}/device.csr" -CA "${CERT_DIR}/$CA.ca.pem" -CAkey "${CERT_DIR}/$CA.ca.key" -CAcreateserial -out "${PROV_DIR}/device.crt.tmp" -days 500 -sha256
cat "${PROV_DIR}/device.crt.tmp" "${CERT_DIR}/$CA.ca.pem" > "${PROV_DIR}/device.crt"
echo "[provision] Cleaning up temp files"
rm "${PROV_DIR}/device.crt.tmp" "${PROV_DIR}/device.csr"
echo "[provision] Done"
