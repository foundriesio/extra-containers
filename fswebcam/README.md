# fswebcam Docker image 
[![Microbadger](https://images.microbadger.com/badges/image/linarotechnologies/fswebcam-docker.svg)](http://microbadger.com/images/linarotechnologies/fswebcam-docker "Image size")
[![Docker Stars](https://img.shields.io/docker/stars/linarotechnologies/fswebcam-docker.svg?maxAge=86400)](https://hub.docker.com/r/linarotechnologies/fswebcam-docker/)
[![Docker Pulls](https://img.shields.io/docker/pulls/linarotechnologies/fswebcam-docker.svg?maxAge=86400)](https://hub.docker.com/r/linarotechnologies/fswebcam-docker/)

usage: 
```
#Run as Root
curl -L https://raw.githubusercontent.com/akbennettatlinaro/fswebcam-docker/master/run.sh > /usr/bin/fswebcam
chmod +x /usr/bin/fswebcam

#Run as normal user
fswebcam --no-banner -r 640x480 image.jpg
```
