FROM python:3.7-alpine3.9

# Add the required dependencies to install psutil that are missing from alpine
# See: https://github.com/giampaolo/psutil/issues/872#issuecomment-272248943
RUN apk add gcc linux-headers libc-dev

# Begin the install proper
RUN python3 -m pip install --no-cache --upgrade pip
RUN python3 -m pip install wiotp-sdk==0.10.0 psutil
ADD ibm-iotsdk/ /opt/ibm/iotpsutil/
RUN chmod +x /opt/ibm/iotpsutil/*.py

RUN mkdir -p /config
RUN mkdir -p /ibm-iotsdk

WORKDIR /
COPY ibm-iotsdk/* /ibm-iotsdk/

ENTRYPOINT ["/ibm-iotsdk/start.sh"]
