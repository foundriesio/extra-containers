#!/bin/bash

#
# Copyright (c) 2017 Linaro Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

set -e

SCRIPT_VERSION="1.00"

# logging
LOG_LEVEL_ERROR=1
LOG_LEVEL_WARN=2
LOG_LEVEL_INFO=3
LOG_LEVEL_DEBUG=4
LOG_LEVEL_VERBOSE_DEBUG=5

LOGLEVEL_REGEX="^[${LOG_LEVEL_ERROR}-${LOG_LEVEL_VERBOSE_DEBUG}]$"

DEFAULT_TEMPLATE_FILE="/etc/mosquitto/template.conf"
DEFAULT_OUTPUT_FILE="/etc/mosquitto/conf.d/bluemix.conf"

function print_help {
cat << END_OF_HELP_MARKER
COMMAND LINE OPTIONS:
-ll    | --log-level		: default log level output (values: 1 to 5)
-ak    | --api-key		: API Key for deleting and re-adding the gateway device
-at    | --auth-token		: Auth token for API Key
-bo    | --bluemix-org		: Bluemix organization ID
-gdt   | --gw-device-type	: Gateway device type in Bluemix
-gdi   | --gw-device-id		: Gateway device ID
-gp    | --gw-password		: Gateway device auth token (override)
-t     | --template		: Specify the source template file (override)
-o     | --output		: Specify the output destination file (override)
-h     | --help			: Display this help
-v     | --version		: Display script version
END_OF_HELP_MARKER
}

# Set option_loglevel early so that logging can be done
option_loglevel="${LOG_LEVEL_INFO}"

# write_log()
# description:
#   Write information to stdout according the specified log level
# params:
#   1: log level
#   2>: output text
function write_log {
	if [ "${option_loglevel}" -ge "${1}" ]; then
		shift
		echo "${@}" >&2
	fi
}

# these are currently empty variables, but could in fact have default values here
option_api_key=""
option_auth_token=""
option_bluemix_org=""
option_gw_device_type=""
option_gw_device_id=""
# an empty password will use auth-token provided by REST response
option_gw_password=""
# file options
option_template_file="${DEFAULT_TEMPLATE_FILE}"
option_output_file="${DEFAULT_OUTPUT_FILE}"

while [ "${#}" -gt 0 ]; do
	case "${1}" in
	# NOTE: -ll option should be first in command line
	# to debug option parsing
	"-ll" | "--loglevel")
		shift
		if ! [[ "${1}" =~ ${LOGLEVEL_REGEX} ]]; then
			write_log ${LOG_LEVEL_ERROR} "Log level must be between ${LOG_LEVEL_ERROR} and ${LOG_LEVEL_VERBOSE_DEBUG}"
			exit 1
		fi
		option_loglevel="${1}"
		shift
		;;
	"-ak" | "--api-key")
		shift
		option_api_key="${1}"
		shift
		;;
	"-at" | "--auth-token")
		shift
		option_auth_token="${1}"
		shift
		;;
	"-bo" | "--bluemix-org")
		shift
		option_bluemix_org="${1}"
		shift
		;;
	"-gdt" | "--gw-device-type")
		shift
		option_gw_device_type="${1}"
		shift
		;;
	"-gdi" | "--gw-device-id")
		shift
		option_gw_device_id="${1}"
		shift
		;;
	"-gp" | "--gw-password")
		shift
		option_gw_password="${1}"
		shift
		;;
	"-t" | "--template")
		shift
		option_template_file="${1}"
		shift
		;;
	"-o" | "--output")
		shift
		option_output_file="${1}"
		shift
		;;
	"-v" | "--version")
		write_log ${LOG_LEVEL_INFO} "${SCRIPT_VERSION}"
		exit 0
		;;
	"-h" | "--help" | *)
		print_help
		exit 0
		;;
	esac
done

if [ ! -e "${option_template_file}" ]; then
	write_log ${LOG_LEVEL_ERROR} "ERROR: Cannot open ${option_template_file}."
	exit 1
fi

if [ -z ${option_api_key} ]; then
	write_log ${LOG_LEVEL_ERROR} "ERROR: API Key is required.\n"
	print_help
	exit 1
fi

if [ -z ${option_auth_token} ]; then
	write_log ${LOG_LEVEL_ERROR} "ERROR: API auth token is required.\n"
	print_help
	exit 1
fi

if [ -z ${option_bluemix_org} ]; then
	write_log ${LOG_LEVEL_ERROR} "ERROR: Bluemix organization is required.\n"
	print_help
	exit 1
fi

if [ -z ${option_gw_device_type} ]; then
	write_log ${LOG_LEVEL_ERROR} "ERROR: Gateway device type is required.\n"
	print_help
	exit 1
fi

# check for curl package
which curl > /dev/null 2>&1
if [ "${?}" -ne "0" ]; then
	write_log ${LOG_LEVEL_ERROR} "ERROR: curl package required.  Try: sudo apt-get install curl"
	exit 1
fi

# make sure hci0 is ready
hciconfig | grep hci0 > /dev/null 2>&1
if [ "${?}" -ne "0" ]; then
	write_log ${LOG_LEVEL_ERROR} "ERROR: hci0 not ready"
	exit 1
fi

# use BT addr as unique device id for gateway if not specified
if [ -z ${option_gw_device_id} ]; then
	option_gw_device_id="${option_gw_device_type}-$(hciconfig hci0 | grep -m 1 'BD Address' | awk '{print $3}' | tr -d ':')"
	write_log ${LOG_LEVEL_DEBUG} "Gateway device id: ${option_gw_device_id}"
fi

bm_url="https://${option_bluemix_org}.internetofthings.ibmcloud.com/api/v0002"
write_log ${LOG_LEVEL_DEBUG} "Bluemix URL : ${bm_url}"
bm_auth="\"${option_api_key}\":\"${option_auth_token}\""
write_log ${LOG_LEVEL_DEBUG} "Bluemix Auth: ${bm_auth}"

# Check whether a specific device exists in Bluemix
function bm_device_check {
	local cmd
	local resp

	cmd="curl -s -I -X GET -u ${bm_auth} ${bm_url}/device/types/${option_gw_device_type}/devices/${option_gw_device_id}"
	write_log ${LOG_LEVEL_DEBUG} "bm_device_check command:\n${cmd}"
	resp=$(eval ${cmd})
	write_log ${LOG_LEVEL_DEBUG} "bm_device_check response:\n${resp}"

	echo ${resp} | grep "HTTP/1.1" | awk '{print $2}'
}

# Delete a device in Bluemix
# Returns the HTTP status code
function bm_device_delete {
	local cmd
	local resp

	cmd="curl -s -I -X DELETE -u ${bm_auth} ${bm_url}/device/types/${option_gw_device_type}/devices/${option_gw_device_id}"
	write_log ${LOG_LEVEL_DEBUG} "bm_device_delete command:\n${cmd}"
	resp=$(eval ${cmd})
	write_log ${LOG_LEVEL_DEBUG} "bm_device_delete response:\n${resp}"

	echo ${resp} | grep "HTTP/1.1" | awk '{print $2}'
}

# Create a device in Bluemix
# 1: deviceId
# 2: serial #
# 3: fw version
# Returns created device's auth token
function bm_device_create {
	local data
	local cmd
	local resp

	if [ ! -z ${option_gw_password} ]; then
		data="{\"deviceId\":\"${1}\",\"authToken\":\"${option_gw_password}\",\"deviceInfo\":{\"serialNumber\":\"${2}\",\"fwVersion\":\"${3}\"}}"
	else
		data="{\"deviceId\":\"${1}\",\"deviceInfo\":{\"serialNumber\":\"${2}\",\"fwVersion\":\"${3}\"}}"
	fi

	cmd="curl -s -H \"Content-Type: application/json\" -X POST  -d '${data}' -u ${bm_auth} ${bm_url}/device/types/${option_gw_device_type}/devices"
	write_log ${LOG_LEVEL_DEBUG} "bm_device_create command:\n${cmd}"
	resp=$(eval ${cmd})
	write_log ${LOG_LEVEL_DEBUG} "bm_device_create response:\n${resp}"

	# get Bluemix JSON response, find authToken, escape any & chars and remove the quotes
	echo ${resp} | jq '.authToken' | sed -e 's/&/\\&/g' | tr -d '\"'
}

# main script

# if device exists in Bluemix, delete it
check_status=$(bm_device_check)
write_log ${LOG_LEVEL_DEBUG} "Device check ${check_status}"
if [ "${check_status}" -eq "200" ]; then
	write_log ${LOG_LEVEL_INFO} "Deleting prior registration of gateway ${option_gw_device_type}:${option_gw_device_id}"
	del_status=$(bm_device_delete)
	if [ "${del_status}" -ne "204" ]; then
		write_log ${LOG_LEVEL_ERROR} "Error deleting device from Bluemix: ${del_status}"
		exit 1
	fi
fi

# create device in Bluemix
device_auth=$(bm_device_create ${option_gw_device_id} "abcdef" "1.00")
write_log ${LOG_LEVEL_INFO} "Received auth_token '${device_auth}' from Bluemix org ${option_bluemix_org}"
if [ -z ${device_auth} ]; then
	write_log ${LOG_LEVEL_ERROR} "Device auth not returned when creating device in Bluemix"
	exit 1
fi
write_log ${LOG_LEVEL_INFO} "Registered gateway ${option_gw_device_type}:${option_gw_device_id} with Bluemix org ${option_bluemix_org}"

# generate Mosquitto configuration file
cp ${option_template_file} ${option_output_file}
if [ "$?" -ne "0" ]; then
	write_log ${LOG_LEVEL_ERROR} "Could not copy ${option_template_file} as ${option_output_file}."
	exit 1
fi
sed -i "s/#bm-org-id#/$option_bluemix_org/" ${option_output_file}
sed -i "s/#gw-device-type#/$option_gw_device_type/" ${option_output_file}
sed -i "s/#gw-device-id#/$option_gw_device_id/" ${option_output_file}
sed -i "s/#gw-password#/$device_auth/" ${option_output_file}
write_log ${LOG_LEVEL_INFO} "Created ${option_output_file}"
