#!/usr/bin/env python

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Python sample for connecting to Google Cloud IoT Core via MQTT, using JWT.
This example connects to Google Cloud IoT Core via MQTT, using a JWT for device
authentication. After connecting, by default the device publishes 100 messages
to the device's MQTT topic at a rate of one per second, and then exits.
Before you run the sample, you must follow the instructions in the README
for this sample.
"""

# [START iot_mqtt_includes]
import argparse
import datetime
import logging
import os
import random
import ssl
import time
import psutil
import platform
import threading
import json
import io

import jwt
import paho.mqtt.client as mqtt
from google.cloud import iot_v1

# [END iot_mqtt_includes]

# GLOBALS
GOOGLE_PUBLISH_DELAY_SECS = 5

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.CRITICAL)

# The initial backoff time after a disconnection occurs, in seconds.
minimum_backoff_time = 1

# The maximum backoff time before giving up, in seconds.
MAXIMUM_BACKOFF_TIME = 32

# Whether to wait with exponential backoff before publishing.
should_backoff = False


# [START iot_mqtt_jwt]
def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
        Args:
         project_id: The cloud project ID this device belongs to
         private_key_file: A path to a file containing either an RSA256 or
                 ES256 private key.
         algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'
        Returns:
            A JWT generated from the given project_id and private key, which
            expires in 20 minutes. After 20 minutes, your client will be
            disconnected, and a new JWT will have to be generated.
        Raises:
            ValueError: If the private_key_file does not contain a known key.
        """

    token = {
            # The time that the token was issued at
            'iat': datetime.datetime.utcnow(),
            # The time the token expires.
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=20),
            # The audience field should always be set to the GCP project id.
            'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
            algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)
# [END iot_mqtt_jwt]


# [START iot_mqtt_config]
def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return '{}: {}'.format(rc, mqtt.error_string(rc))


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print('on_connect', mqtt.connack_string(rc))

    # After a successful connect, reset backoff time and stop backing off.
    global should_backoff
    global minimum_backoff_time
    should_backoff = False
    minimum_backoff_time = 1


def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print('on_disconnect', error_str(rc))

    # Since a disconnect occurred, the next loop iteration will wait with
    # exponential backoff.
    global should_backoff
    should_backoff = True


def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    print('on_publish')


def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = str(message.payload.decode('utf-8'))
    print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, message.topic, str(message.qos)))


def get_client(
        project_id, cloud_region, registry_id, device_id, private_key_file,
        algorithm, ca_certs, mqtt_bridge_hostname, mqtt_bridge_port):
    """Create our MQTT client. The client_id is a unique string that identifies
    this device. For Google Cloud IoT Core, it must be in the format below."""
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
            project_id, cloud_region, registry_id, device_id)
    print('Device client_id is \'{}\''.format(client_id))

    client = mqtt.Client(client_id=client_id)

    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    client.username_pw_set(
            username='unused',
            password=create_jwt(
                    project_id, private_key_file, algorithm))

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Register message callbacks. https://eclipse.org/paho/clients/python/docs/
    # describes additional callbacks that Paho supports. In this example, the
    # callbacks just print to standard out.
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to the Google MQTT bridge.
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    # This is the topic that the device will receive configuration updates on.
    mqtt_config_topic = '/devices/{}/config'.format(device_id)

    # Subscribe to the config topic.
    client.subscribe(mqtt_config_topic, qos=1)

    # The topic that the device will receive commands on.
    mqtt_command_topic = '/devices/{}/commands/#'.format(device_id)

    # Subscribe to the commands topic, QoS 1 enables message acknowledgement.
    print('Subscribing to {}'.format(mqtt_command_topic))
    client.subscribe(mqtt_command_topic, qos=0)

    return client
# [END iot_mqtt_config]

def create_rs256_device(
        service_account_json, project_id, cloud_region, registry_id, device_id,
        certificate_file):
    """Create a new device with the given id, using RS256 for
    authentication."""
    # [START iot_create_rsa_device]
    # project_id = 'YOUR_PROJECT_ID'
    # cloud_region = 'us-central1'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    # certificate_file = 'path/to/certificate.pem'

    client = iot_v1.DeviceManagerClient()

    exists = False

    parent = client.registry_path(project_id, cloud_region, registry_id)

    devices = list(client.list_devices(parent=parent))

    for device in devices:
        if device.id == device_id:
            exists = True


    if not exists:
        with io.open(certificate_file) as f:
            certificate = f.read()

        # Note: You can have multiple credentials associated with a device.
        device_template = {
            'id': device_id,
            'credentials': [{
                'public_key': {
                    'format': 'RSA_X509_PEM',
                    'key': certificate
                }
            }]
        }
        return client.create_device(parent, device_template)
    else:
        print('Device exists, skipping')
    # [END iot_create_rsa_device]


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=(
            'Example Google Cloud IoT Core MQTT device connection code.'))
    parser.add_argument(
            '--algorithm',
            choices=('RS256', 'ES256'),
            default='RS256',
            help='Which encryption algorithm to use to generate the JWT.')
    parser.add_argument(
            '--ca_certs',
            default='/google-iotsdk/roots.pem',
            help='CA root from https://pki.google.com/roots.pem')
    parser.add_argument(
            '--cloud_region', default='us-central1', help='GCP cloud region')
    parser.add_argument(
            '--data',
            default='Hello there',
            help='The telemetry data sent on behalf of a device')
    parser.add_argument(
            '--device_id',
            default='homeassistant-device',
            help='Cloud IoT Core device id')
    parser.add_argument(
            '--jwt_expires_minutes',
            default=20,
            type=int,
            help='Expiration time, in minutes, for JWT tokens.')
    parser.add_argument(
            '--listen_dur',
            default=60,
            type=int,
            help='Duration (seconds) to listen for configuration messages')
    parser.add_argument(
            '--message_type',
            choices=('event', 'state'),
            default='event',
            help=('Indicates whether the message to be published is a '
                  'telemetry event or a device state message.'))
    parser.add_argument(
            '--mqtt_bridge_hostname',
            default='mqtt.googleapis.com',
            help='MQTT bridge hostname.')
    parser.add_argument(
            '--mqtt_bridge_port',
            choices=(8883, 443),
            default=8883,
            type=int,
            help='MQTT bridge port.')
    parser.add_argument(
            '--private_key_file',
            default='/google-iotsdk/rsa_private.pem',
            help='Path to private key file.')
    parser.add_argument(
            '--project_id',
            default='homeassistant-281519',
            help='GCP cloud project name')
    parser.add_argument(
            '--registry_id',
            default='homeassistant-registry',
            help='Cloud IoT Core registry id')
    parser.add_argument(
            '--service_account_json',
            default='/config/google.json',
            help='Path to service account json file.')
    parser.add_argument(
            '--rsa_certificate_file',
            default='/google-iotsdk/rsa_cert.pem',
            help='Path to service account json file.')

    return parser.parse_args()

class LockedData(object):
    def __init__(self, thing_name=platform.node()):
        self.lock = threading.Lock()
        self.thing_name = thing_name
        self.before_ts = 0
        self.ioBefore = None
        self.diskBefore = None
        self.disconnect_called = False

    def toJSON(self):
        after_ts = time.time()
        ioAfter = psutil.net_io_counters()
        diskAfter = psutil.disk_io_counters()
        # Calculate the time taken between IO checks
        duration = after_ts - self.before_ts
        data = {
            "name": self.thing_name,
            "cpu": psutil.cpu_percent(percpu=False),
            "mem": psutil.virtual_memory().percent,
            "network": {
                "up": round((ioAfter.bytes_sent - self.ioBefore.bytes_sent) / (duration * 1024), 2),
                "down": round((ioAfter.bytes_recv - self.ioBefore.bytes_recv) / (duration * 1024), 2),
            },
            "disk": {
                "read": round((diskAfter.read_bytes - self.diskBefore.read_bytes) / (duration * 1024), 2),
                "write": round((diskAfter.write_bytes - self.diskBefore.write_bytes) / (duration * 1024), 2),
            },
        }
        self.before_ts = after_ts
        self.ioBefore = ioAfter
        self.diskBefore = diskAfter
        return data


locked_data = LockedData()


def mqtt_device_demo(args):
    """Connects a device, sends data, and receives data."""
    # [START iot_mqtt_run]
    global minimum_backoff_time
    global MAXIMUM_BACKOFF_TIME

    # Publish to the events or state topic based on the flag.
    sub_topic = 'events' if args.message_type == 'event' else 'state'

    mqtt_topic = '/devices/{}/{}'.format(args.device_id, sub_topic)

    jwt_iat = datetime.datetime.utcnow()
    jwt_exp_mins = args.jwt_expires_minutes
    print('CA {}'.format(args.ca_certs))
    client = get_client(
        args.project_id, args.cloud_region, args.registry_id,
        args.device_id, args.private_key_file, args.algorithm,
        args.ca_certs, args.mqtt_bridge_hostname, args.mqtt_bridge_port)

    # Take initial reading
    psutil.cpu_percent(percpu=False)
    locked_data.thing_name = args.device_id
    locked_data.before_ts = time.time()
    locked_data.ioBefore = psutil.net_io_counters()
    locked_data.diskBefore = psutil.disk_io_counters()
    psutil.disk_io_counters(perdisk=False, nowrap=True)

    publish_count = 1


    # Publish num_messages messages to the MQTT bridge once per second.
    while True:
       # Process network events.
        client.loop()

        print("[Google IoT] Updating values [%d]" % (publish_count))

        # Wait if backoff is required.
        if should_backoff:
            # If backoff time is too large, give up.
            if minimum_backoff_time > MAXIMUM_BACKOFF_TIME:
                print('Exceeded maximum backoff time. Giving up.')
                break

            # Otherwise, wait and connect again.
            delay = minimum_backoff_time + random.randint(0, 1000) / 1000.0
            print('Waiting for {} before reconnecting.'.format(delay))
            time.sleep(delay)
            minimum_backoff_time *= 2
            client.connect(args.mqtt_bridge_hostname, args.mqtt_bridge_port)
        # [START iot_mqtt_jwt_refresh]
        seconds_since_issue = (datetime.datetime.utcnow() - jwt_iat).seconds
        if seconds_since_issue > 60 * jwt_exp_mins:
            print('Refreshing token after {}s'.format(seconds_since_issue))
            jwt_iat = datetime.datetime.utcnow()
            client.loop()
            client.disconnect()
            client = get_client(
                args.project_id, args.cloud_region,
                args.registry_id, args.device_id, args.private_key_file,
                args.algorithm, args.ca_certs, args.mqtt_bridge_hostname,
                args.mqtt_bridge_port)
        # [END iot_mqtt_jwt_refresh]
        # Publish "payload" to the MQTT topic. qos=1 means at least once
        # delivery. Cloud IoT Core also supports qos=0 for at most once
        # delivery.

        data = locked_data.toJSON()
        payload = json.dumps(data)
        print('Publish message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, mqtt_topic, str(1)))
        client.publish(mqtt_topic, payload, qos=1)

        publish_count += 1
        # Send events every second. State should not be updated as often
        for i in range(0, GOOGLE_PUBLISH_DELAY_SECS):
            time.sleep(1)
            client.loop()
    # [END iot_mqtt_run]


def main():
    args = parse_command_line_args()
    print('project_id: {}'.format(
    args.project_id))
    print('registry_id: {}'.format(
    args.registry_id))
    print('device_id: {}'.format(
    args.device_id))   
    test = create_rs256_device(args.service_account_json, args.project_id, args.cloud_region, args.registry_id, args.device_id,
       args.rsa_certificate_file)
    mqtt_device_demo(args)
    print('Finished.')


if __name__ == '__main__':
    main()
