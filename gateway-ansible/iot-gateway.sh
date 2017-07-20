# Gateway target hostname
hostname=10.0.1.3

# Docker tag to use (linaro-technologies docker images now support multiple architectures)
tag=latest

# Location where hawkbit is running
gitci=10.0.1.2

#Cloudmqtt configuration
cloudmqtthost=m12.cloudmqtt.com
cloudmqttport=18645
cloudmqttuser=username
cloudmqttpw=password

#First argument Ansible tags
ansibletags="$1"

ansible-playbook -e "mqttuser=$cloudmqttuser mqttpass=$cloudmqttpw mqtthost=$cloudmqtthost mqttport=$cloudmqttport "\
                 -e "gitci=$gitci tag=$tag" \
                 -e "brokerhost=$hostname brokeruser='' brokerpw=''" \
                  -i linaro@$hostname, iot-gateway.yml --tags $ansibletags
