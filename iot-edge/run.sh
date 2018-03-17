#!/bin/bash

connstr=${CONNECTIONSTRING}

ARCH=amd64
file -L /bin/ls | grep -q aarch64 && ARCH=arm && echo "aarch64" || true
file -L /bin/ls | grep -q armhf && ARCH=arm && echo "armhf" || true

[ $ARCH = "arm" ] && image=' --image microsoft/azureiotedge-agent:1.0.0-preview021-linux-arm32v7 '

iotedgectl setup $image --connection-string "$connstr" --auto-cert-gen-force-no-passwords
iotedgectl start
