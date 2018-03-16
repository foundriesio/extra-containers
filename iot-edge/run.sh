#!/bin/bash

connstr=${CONNECTIONSTRING}

iotedgectl setup --connection-string "$connstr" --auto-cert-gen-force-no-passwords
iotedgectl start
