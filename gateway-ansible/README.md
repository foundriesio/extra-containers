# Gateway Ansible Setup Scripts

Ansible scripts to setup your minimal system as an IoT gateway.

## Setup your host

### Ubuntu/Debian

```
apt -y install ansible
```

### Mac OS X

```
brew install ansible
```

## Deploy your SSH public key

Make sure to setup your SSH public key before calling ansible:

```
ssh-copy-id <gateway host>
```

## Gateway Targets

### IoT-Gateway

```
ansible-playbook -e "mqttuser= mqttpass= mqtthost= mqttport= gitci= tag=" -i targethost, -u linaro iot-gateway.yml
```

Ansible tags:

 - --tags local      # load hawkbit, freeboard, bt-joiner and mosquitto-local
 - --tags gateway    # load mosquitto-local, bt-joiner, freeboard and tinyproxy
 - --tags cloud      # load mosquitto-cloud, bt-joiner and tinyproxy
 - --tags mosquitto-local
 - --tags mosquitto-cloud
 - --tags hawkbit
 - --tags bt-joiner
 - --tags tinyproxy
 - --tags freeboard

Arguments:

 - **mqttuser**: mosquitto remote username
 - **mqttpass**: mosquitto remote password
 - **mqtthost**: remote mqtt address
 - **mqttport**: remote mqtt service port
 - **gitci**: address for your private hawkbit server
 - **tag**: docker container tag (e.g. latest-arm64, latest-armhf or empty for latest)
 - **brokerhost**: mosquitto websocket host (for use with freeboard)
 - **brokeruser**: mosquitto websocket user (for use with freeboard)
 - **brokerpw**: mosquitto websocket password (for use with freeboard)

**Note**: don't forget the comma after *targethost*!

Optional helper script
```
./iot-gateway.sh demo # call ansible to deploy all containers for a demo setup
```

### Freeboard dashboard

The sample dashboard-private.json file is used to demonstrate how to set up a persistent freeboard dashboard.  The device names and groups will have to be changed to match those in your setup.

If you modify and use dashboard-private.json, you can browse to the persistent page by appending **?load=dashboard.json**
 - i.e. http://targethost/?load=dashboard.json
 - i.e. http://targethost/?load=dashboards/default.json - a complex dashboard that requires modification
 - i.e. http://targethost/?load=dashboards/simple.json - a simple 'catch all' dashboard
