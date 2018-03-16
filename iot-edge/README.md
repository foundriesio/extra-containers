# simple IoT Edge Control container

For more information, reference: https://docs.microsoft.com/en-us/azure/iot-edge/
```
docker run -d -v /var/run/docker.sock:/var/run/docker.sock -e CONNECTIONSTRING="insert_connection_string_from_iot_edge_preview" opensourcefoundries/iot-edge
```
