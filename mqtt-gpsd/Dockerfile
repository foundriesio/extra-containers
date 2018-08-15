FROM alpine:3.8

RUN apk add --no-cache python3 py3-pip && \
    pip3 install gpsd-py3 paho-mqtt

WORKDIR /src

COPY run.py .

ENTRYPOINT ["python3", "/src/run.py"]
