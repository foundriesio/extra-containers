A cross-platform [Freeboard](https://freeboard.io/) container

### How to use this image

```
docker run -p 8081:80 hub.foundries.io/freeboard

# Or with your own custom layout:
docker run -p 8081:80 -v $PWD/dashboard-private.json:/usr/share/nginx/html/dashboard.json hub.foundries.io/freeboard
```

This will expose an installation of Freeboard and load the dashboard.json http://localhost:8081/?load=dashboard.json

*If you didn't modify dashboard.json to point to your devices and your cloudmqtt credentials you can modify these using the dashboard*

### Configure Cloudmqtt server datasource(s)
![Datasource](/datasource.png)

### Configure widgets
![Widget](/widget.png)

### View widgets
![Dashboard](/dashboard.png)
