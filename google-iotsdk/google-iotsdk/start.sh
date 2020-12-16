#!/bin/sh

GOOGLE_PROVISION_LOC="/prov"
GOOGLE_CONFIG="/config/google.config"
GOOGLE_CONFIG_CREDENTIAL="/config/google.json"
GOOGLE_ROOTCA="/google-iotsdk/roots.pem"

DEVICE_ID_FILE="${GOOGLE_PROVISION_LOC}/thing_name"

while [ ! -f $GOOGLE_CONFIG ]
do
    sleep 2 # or less like 0.2
    echo "Waiting $GOOGLE_CONFIG"
done
    ls -l $GOOGLE_CONFIG
    . $GOOGLE_CONFIG
    echo "PROJECT_ID: $PROJECT_ID"
    echo "REGISTRY_ID: $REGISTRY_ID"
    echo "DEVICE_ID_FILE: $DEVICE_ID_FILE"

# make sure provisioning dir exists
if [ ! -d "${GOOGLE_PROVISION_LOC}" ]; then
	echo "No provisioning directory found: ${GOOGLE_PROVISION_LOC}!"
	exit 1
fi

if [ ! -e ${GOOGLE_PROVISION_LOC}/rsa_cert.pem ] || [ ! -e ${GOOGLE_PROVISION_LOC}/rsa_private.pem ]; then
	/google-iotsdk/provision.sh "${AWS_PROVISION_LOC}" "$DEVICE_ID_FILE"
fi
export GOOGLE_APPLICATION_CREDENTIALS="$GOOGLE_CONFIG_CREDENTIAL"

if [ -f "$DEVICE_ID_FILE" ]; then
    echo "DEVICE_ID_FILE: $DEVICE_ID_FILE"
    DEVICE_ID="$(cat ${DEVICE_ID_FILE})"
    echo "DEVICE_ID: $DEVICE_ID"
fi

python3 /google-iotsdk/service.py \
--project_id=$PROJECT_ID \
--registry_id=$REGISTRY_ID \
--device_id=$DEVICE_ID \
--private_key_file="${GOOGLE_PROVISION_LOC}/rsa_private.pem"  \
--rsa_certificate_file="${GOOGLE_PROVISION_LOC}/rsa_cert.pem"  \
--ca_certs="${GOOGLE_ROOTCA}"
