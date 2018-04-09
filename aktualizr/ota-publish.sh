#!/bin/bash
#
# Copyright (c) 2018 Open Source Foundries Ltd.
# SPDX-License-Identifier: Apache-2.0
#
# Script to publish and sign a pre-built OSTree repository to an OTA+ server.
#

set -e

function usage() {
	cat << EOF >&2
usage: $(basename $0) options

OPTIONS:
	-c	OTA+ credentials zip file (e.g. credentials.zip)
	-h	Shows this message
	-m	Name for the machine target in OTA+ (e.g. raspberrypi3-64)
	-r	OSTree repository (e.g. ostree_repo)
EOF
}

function error() {
	echo "ERROR: $@"
	exit -1
}

function fail() {
	usage
	exit -1
}

function get_opts() {
	declare -r optstr="c:m:r:h"
	while getopts ${optstr} opt; do
		case ${opt} in
			c) credentials=${OPTARG} ;;
			m) machine=${OPTARG} ;;
			r) ostree_repo=${OPTARG} ;;
			h) usage; exit 0 ;;
			*) fail ;;
		esac
	done

	if [ -z "${credentials}" ] || [ -z "${machine}" ] ||
		[ -z "${ostree_repo}" ]; then
		fail
	fi
}

get_opts $@

if [ ! -f "${credentials}" ]; then
	error "Credentials ${credentials} file not found"
fi
if [ ! -d "${ostree_repo}" ]; then
	error "OSTree repository ${ostree_repo} directory not found"
fi

ostree_branch=$(ostree refs --repo ${ostree_repo})
ostree_hash=$(cat ${ostree_repo}/refs/heads/${ostree_branch})
tufrepo=$(mktemp -u -d)
otarepo=$(mktemp -u -d)

echo "Publishing OSTree branch ${ostree_branch} hash ${ostree_hash} to treehub"
garage-push --repo ${ostree_repo} --ref ${ostree_branch} --credentials ${credentials}

echo "Initializing local TUF repository"
garage-sign init --repo ${tufrepo} --home-dir ${otarepo} --credentials ${credentials}

echo "Pulling TUF targets from the remote TUF repository"
garage-sign targets pull --repo ${tufrepo} --home-dir ${otarepo}

echo "Adding OSTree target to the local TUF repository"
garage-sign targets add --repo ${tufrepo} --home-dir ${otarepo} --name ${ostree_branch} \
	--format OSTREE --version ${ostree_hash} --length 0 --url "https://example.com" \
	--sha256 ${ostree_hash} --hardwareids ${machine}

echo "Signing local TUF targets"
garage-sign targets sign --repo ${tufrepo} --home-dir ${otarepo} --key-name targets

echo "Publishing local TUF targets to the remote TUF repository"
garage-sign targets push --repo ${tufrepo} --home-dir ${otarepo}

echo "Verifying remote OSTree + TUF repositories"
garage-check --ref ${ostree_hash} --credentials ${credentials}

echo "Cleaning up local TUF repository"
rm -rf ${tufrepo} ${otarepo}

echo "Local OSTree repository successfully published to the remote OTA+ treehub / TUF repositories"
