[Dump1090](https://github.com/mutability/dump1090) is a simple Mode S decoder for RTLSDR devices

## How to use this image
```
docker run -it --privileged -v /dev/bus/usb:/dev/bus/usb -p 80:8080 hub.foundries.io/dump1090
```
