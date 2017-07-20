# Freeboard in a container
* Added freeboard-mqtt plugin
* Alpine Linux with nginx, so it's teeeeny!

[![Microbadger](https://images.microbadger.com/badges/image/linarotechnologies/freeboard-demo.svg)](http://microbadger.com/images/linarotechnologies/freeboard-demo "Image size")
[![Docker Stars](https://img.shields.io/docker/stars/linarotechnologies/freeboard-demo.svg?maxAge=86400)](https://hub.docker.com/r/linarotechnologies/freeboard-demo/)
[![Docker Pulls](https://img.shields.io/docker/pulls/linarotechnologies/freeboard-demo.svg?maxAge=86400)](https://hub.docker.com/r/linarotechnologies/freeboard-demo/)


### How to use this image with default widgets

```
docker run --name myfreeboard -p 8081:80 -v $PWD/dashboard-private.json:/usr/share/nginx/html/dashboard.json -d freeboard
```

This will expose an installation of Freeboard and load the dashboard.json http://localhost:8081/?load=dashboard.json

*If you didn't modify dashboard.json to point to your devices and your cloudmqtt credentials you can modify these using the dashboard*

### Configure Cloudmqtt server datasource(s)
![Datasource](/datasource.png)

### Configure widgets
![Widget](/widget.png)

### View widgets
![Dashboard](/dashboard.png)
