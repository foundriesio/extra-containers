# gpsd

multiarch alpine based GPS daemon 

## example

docker run -it -p 2947:2947 --device=/dev/ttyAMA0 forcedinductionz/docker-gpsd -D2 /dev/ttyAMA0
