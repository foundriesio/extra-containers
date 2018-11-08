FROM alpine:latest

RUN apk add --no-cache python3 py3-pip && \
    pip3 install gpsd-py3 paho-mqtt sseclient pyyaml

WORKDIR /src

COPY run.py .
COPY subscriptions.yml .

ENTRYPOINT ["python3", "/src/run.py"]

