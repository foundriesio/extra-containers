FROM debian:10.3-slim
ARG DEBIAN_FRONTEND=noninteractive

# [UBUNTU]
RUN apt-get update && \
    apt-get install -y python3 git ca-certificates curl \
        cmake build-essential libssl-dev python3-dev python3-pip zlib1g-dev openssl uuid-runtime libffi-dev 

# install python3 dependencies in advance -- we can copy them later
RUN python3 -m pip install --no-cache --upgrade pip && \
    python3 -m pip install --no-cache --upgrade setuptools wheel psutil

RUN python3 -m pip install --no-cache --upgrade cryptography>=2.9.2
RUN python3 -m pip install --no-cache --upgrade google-api-python-client>=1.9.3
RUN python3 -m pip install --no-cache --upgrade google-auth-httplib2>=0.0.3
RUN python3 -m pip install --no-cache --upgrade google-auth>=1.18.0
RUN python3 -m pip install --no-cache --upgrade google-cloud-pubsub>=1.6.0
RUN python3 -m pip install --no-cache --upgrade google-cloud-iot>=1.0.0
RUN python3 -m pip install --no-cache --upgrade grpc-google-iam-v1>=0.12.3
RUN python3 -m pip install --no-cache --upgrade pyjwt>=1.7.1
RUN python3 -m pip install --no-cache --upgrade paho-mqtt>=1.5.0


RUN mkdir -p /config
RUN mkdir -p /google-iotsdk
RUN mkdir -p /prov

WORKDIR /
COPY google-iotsdk/* /google-iotsdk/

ENTRYPOINT ["/google-iotsdk/start.sh"]
