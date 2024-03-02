# Copyright (c) 2020 Foundries.io
#
# SPDX-License-Identifier: BSD-3-Clause
#

# STAGE 1
# AWS CommonRuntime for Python has openssl issues with > 1.0.2
FROM ubuntu:18.04 as awsiot-dev

ENV AWS_CRT_VERS=0.5.9
ENV AWS_CRT_SHA=0f950ea5219cfea22248854691bb7d3a3bef67dc

ENV AWS_IOT_SDK_VERS=1.0.3
ENV AWS_IOT_SDK_SHA=30152d11302b130c7e69a78b24cb3655d81753a6

# [UBUNTU]
RUN apt-get update && \
    apt-get install -y python3 git ca-certificates curl \
        cmake build-essential libssl-dev python3-dev python3-pip zlib1g-dev

# install python3 dependencies in advance -- we can copy them later
RUN pip3 install --no-cache --upgrade pip && \
    pip3 install --no-cache --upgrade setuptools wheel psutil

# setup AWS Common Runtime for Python
RUN git clone https://github.com/awslabs/aws-crt-python -b v${AWS_CRT_VERS} && \
    [ "$(cat aws-crt-python/.git/HEAD)" = "${AWS_CRT_SHA}" ] && \
    cd aws-crt-python && \
    git submodule init && \
    git submodule update && \
    sed -i "s/':libcrypto.a'/'crypto', 'z'/g" setup.py && \
    sed -i "s/sys\/errno.h/errno.h/g" aws-common-runtime/aws-c-io/source/posix/socket.c && \
    sed -i "s/add_subdirectory(tests)/# add_subdirectory(tests)/g" aws-common-runtime/aws-c-cal/CMakeLists.txt && \
    sed -i "s/add_subdirectory(tests)/# add_subdirectory(tests)/g" aws-common-runtime/aws-c-http/CMakeLists.txt && \
    sed -i "s/add_subdirectory(bin\/elasticurl)/# add_subdirectory(bin\/elasticurl)/g" aws-common-runtime/aws-c-http/CMakeLists.txt && \
    python3 setup.py build && \
    python3 setup.py install && \
    cd .. && \
    tar -czf aws-crt-python.tar.gz /aws-crt-python/build/lib.*/*

# setup AWS IoT SDK for Python
RUN git clone https://github.com/aws/aws-iot-device-sdk-python-v2 -b v${AWS_IOT_SDK_VERS} && \
    [ "$(cat aws-iot-device-sdk-python-v2/.git/HEAD)" = "${AWS_IOT_SDK_SHA}" ] && \
    cd aws-iot-device-sdk-python-v2 && \
    python3 setup.py build && \
    python3 setup.py install && \
    cd .. && \
    tar -czf aws-iot-device-sdk-python-v2.tar.gz /aws-iot-device-sdk-python-v2/build/lib/*

# save python psutil binaries
RUN tar -czf psutils.tar.gz /usr/local/lib/python3.6/dist-packages/psutil*

# pre-download get-pip script
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"

# STAGE 2
# AWS CommonRuntime for Python has openssl issues with > 1.0.2
FROM ubuntu:18.04

# [UBUNTU]
RUN apt-get update && \
    apt-get install -y python3 python3-distutils ca-certificates \
        libssl1.0.0 curl uuid-runtime

# [UBUNTU]: this is a bit sketchy, but it saves about 250MB in recommended packages
COPY --from=awsiot-dev /get-pip.py /
RUN python3 get-pip.py

RUN pip3 install --no-cache --upgrade pip && \
    pip3 install --no-cache --upgrade setuptools wheel enum34 pyserial paho-mqtt && \
    mkdir /certs

COPY --from=awsiot-dev /psutils.tar.gz /
COPY --from=awsiot-dev /aws-crt-python.tar.gz /
COPY --from=awsiot-dev /aws-iot-device-sdk-python-v2.tar.gz /

RUN tar -xzf /psutils.tar.gz && \
    tar -xzf /aws-crt-python.tar.gz --strip 3 && \
    tar -xzf /aws-iot-device-sdk-python-v2.tar.gz --strip 3 && \
    rm *.tar.gz

COPY start.sh /
COPY provision.sh /
COPY service.py /
COPY certs/* /certs/


ENTRYPOINT ["/start.sh"]
