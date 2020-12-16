#!/bin/sh

# create the device certificate
#
# On the first connection attempt, it will trigger the google thing creation,
# registration and so forth 

PROV_DIR=${1:-/prov}
DEVICE_ID_FILE=${2:-/prov/thing_name}

GOOGLE_CONFIG_CREDENTIAL="/config/google.json"

if [ -f "$DEVICE_ID_FILE" ]; then
    echo "$DEVICE_ID_FILE exists."
else
    while [ ! -f $GOOGLE_CONFIG_CREDENTIAL ]
    do
        sleep 5 # or less like 0.2
        echo "Waiting $GOOGLE_CONFIG_CREDENTIAL"
    done
        ls -l $GOOGLE_CONFIG_CREDENTIAL
        DEVICE_UUID=$(uuidgen)
        DEVICE_ID="fio-google-${DEVICE_UUID}"
        echo "[provision] Device name: ${DEVICE_ID}"
        echo "${DEVICE_ID}" > "${PROV_DIR}/thing_name"
        openssl req -x509 -newkey rsa:2048 -keyout ${PROV_DIR}/rsa_private.pem -nodes -out ${PROV_DIR}/rsa_cert.pem -subj "/CN=unused"
fi

DEVICE_ID="$(cat ${PROV_DIR}/thing_name)"
echo "[provision] Device name: ${DEVICE_ID}"
export GOOGLE_APPLICATION_CREDENTIALS="$GOOGLE_CONFIG_CREDENTIAL"
echo "9"


