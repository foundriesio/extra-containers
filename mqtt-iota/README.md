MQTT to IOTA Ledger Bridge. Retrieves MQTT data and publishes it to the IOTA Tangle.

## How to use this image

```

docker run -it --rm --name mqtt-iota --net=host -e MQTT_FULL_URL=mqtt://127.0.0.1:1883 -e MQTT_CLIENT_PREFIX=<mqtt client prefix> -e MQTT_TOPIC=<mqtt topic or # for all> IOTA_HOST=<iota node host> -e IOTA_PORT=<iota node port> -e IOTA_SEED=<iota seed> -e IOTA_ADDRESS=<iota address> -e IOTA_TAG=<iota tag> mqtt-iota
```
