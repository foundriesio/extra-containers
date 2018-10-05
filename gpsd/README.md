multiarch Alpine based GPS daemon

## How to use this image

docker run -it -p 2947:2947 --device=/dev/ttyAMA0 hub.foundries.io/gpsd -D2 /dev/ttyAMA0
