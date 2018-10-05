A cross-plaform [coap](https://github.com/obgm/libcoap) client/server container

## How to use this image
```
# start a server
docker run --net host hub.foundries.io/libcoap coap-server

# get the time from the server
docker run --net host libcoap coap-client -m get coap://[::1]/time
```
