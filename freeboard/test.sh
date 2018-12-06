#!/bin/sh -e

nginx
apk add --no-cache curl
curl http://localhost | grep freeboard
