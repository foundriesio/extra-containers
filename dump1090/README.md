# dump1090 Docker image 


docker build -t test-dump1090 .
docker run -it --privileged -v /dev/bus/usb:/dev/bus/usb -p 80:8080 --name dump1090 test-dump1090