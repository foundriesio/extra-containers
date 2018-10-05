A cross-platform container image of [rtlsdr](https://osmocom.org/projects/rtl-sdr/wiki)

## How to use this image

```
docker run -it --privileged -v /dev/bus/usb:/dev/bus/usb hub.foundries.io/rtl-sdr rtl_sdr --help
```
