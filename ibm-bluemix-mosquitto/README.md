A [Mosquitto](http://mosquitto.org/) container image tailored for communitcating
with [IBM BlueMix](https://www.ibm.com/developerworks/cloud/library/cl-mqtt-bluemix-iot-node-red-app/index.html)

## How to use this image

Create a local environment file containing the IBM Bluemix authentication keys:

```
$ cat ibm-bluemix-mosquitto.env
BLUEMIX_AUTHKEY=a-org-key
BLUEMIX_AUTHTOKEN=token
BLUEMIX_ORG=bluemixorg
GW_DEVICE_TYPE=hikey
```

Then run the containiner giving your local environment file with *--env-file*:

```
docker run -p9001:9001 -p1883:1883 --env-file=/home/osf/ibm-bluemix-mosquitto.env hub.foundries.io/ibm-bluemix-mosquitto
```
