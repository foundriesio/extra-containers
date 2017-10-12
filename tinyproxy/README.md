# Tinyproxy

## Build the container

```
docker build -t tinyproxy --force-rm -f Dockerfile .
```

## Run the container

```
docker run --restart=always -d -t --net=host --read-only --tmpfs=/var/run --tmpfs=/var/log --tmpfs=/tmp --add-host=gitci.com:<hawkbit ip address> --name tinyproxy tinyproxy
```

## Run the pre-built container

```
docker run --restart=always -d -t --net=host --read-only --tmpfs=/var/run --tmpfs=/var/log --tmpfs=/tmp --add-host=gitci.com:<hawkbit ip address> --name tinyproxy linarotechnologies/tinyproxy:latest
```
