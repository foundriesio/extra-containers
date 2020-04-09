#!/bin/sh

AWS_ENDPOINT="ats.iot.us-east-2.amazonaws.com"
AWS_CERT_LOC="/certs"
AWS_PROVISION_LOC="/prov"

parse_args()
{
    while [ $# -gt 0 ]
    do
        case $1 in
        --endpoint)
            AWS_ENDPOINT=$2
            shift
            shift
            ;;
        --cert-location)
            AWS_CERT_LOC=$2
            shift
            shift
            ;;
        --provision-location)
            AWS_PROVISION_LOC=$2
            shift
            shift
            ;;
        *)
            shift
            ;;
        esac
    done
}

parse_args "$@"

# make sure provisioning dir exists
if [ ! -d "${AWS_PROVISION_LOC}" ]; then
	echo "No provisioning directory found: ${AWS_PROVISION_LOC}!"
	exit 1
fi

if [ ! -e ${AWS_PROVISION_LOC}/device.key ] || [ ! -e ${AWS_PROVISION_LOC}/device.crt ]; then
	/provision.sh "root" "/certs" "${AWS_PROVISION_LOC}" "${AWS_ENDPOINT}"
fi

python3 /service.py --thing-name "$(cat ${AWS_PROVISION_LOC}/thing_name)" --endpoint "${AWS_ENDPOINT}" \
	--provision-location "${AWS_PROVISION_LOC}" \
	--cert-location  "${AWS_CERT_LOC}"
