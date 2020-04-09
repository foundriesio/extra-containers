#!/usr/bin/python3

# Copyright (c) 2020 Foundries.io
# All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0

import argparse
import json
import os
import platform
import psutil
import signal
import sys
import threading
import time
import traceback

from concurrent.futures import Future

from awscrt import io, mqtt
from awsiot import iotshadow, mqtt_connection_builder

# GLOBALS
AWS_CONNECT_ATTEMPTS = 5
AWS_CONNECT_DELAY_SECS = 10
AWS_KEEP_ALIVE_SECS = 15
AWS_PUBLISH_DELAY_SECS = 5


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


###############################################################################
#
#   Misc
#
###############################################################################

def cleanup(msg_or_exception):
    global aws_mqtt

    if isinstance(msg_or_exception, Exception):
        print("[cleanup] Exiting sample due to exception.")
        traceback.print_exception(msg_or_exception.__class__, msg_or_exception, sys.exc_info()[2])
    elif msg_or_exception is not None:
        print("[cleanup] Exit msg: %s" % (msg_or_exception))

    with locked_data.lock:
        if not locked_data.disconnect_called:
            print("[cleanup] Disconnecting...")
            locked_data.disconnect_called = True
            # disconnect from AWS
            disconnect_future = aws_mqtt.disconnect()
            disconnect_future.result()

    sys.exit(0)


def signal_handler(sig, frame):
    print("[sig] handle interrupt")
    cleanup(None)


###############################################################################
#
#   AWS MQTT Handling
#
###############################################################################

# Callback when connection is accidentally lost.
def aws_on_connection_interrupted(connection, error, **kwargs):
    print("[aws] Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def aws_on_connection_resumed(connection, return_code, session_present,
                              **kwargs):
    print("[aws] Connection resumed. return_code: %s session_present: %s"
          % (return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("[aws] Session did not persist. Resubscribing to topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because
        # we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(aws_on_resubscribe_complete)


def aws_on_resubscribe_complete(resubscribe_future):
    resubscribe_results = resubscribe_future.result()
    print("[aws] Resubscribe results: {}".format(resubscribe_results))

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit("[aws] Server rejected resubscribe to topic: %s"
                     % (topic))


def on_shadow_delta_updated(delta):
    # type: (iotshadow.ShadowDeltaUpdatedEvent) -> None
    try:
        if delta.state:
            print("[aws] Delta reported a shadow data change")
        else:
            print("[aws] Delta did not report a change")
    except Exception as e:
        exit(e)


def on_update_shadow_accepted(response):
    # type: (iotshadow.UpdateShadowResponse) -> None
    print("[aws] Reported shadow values: %s" % (json.dumps(response.state.reported)))


def on_update_shadow_rejected(error):
    # type: (iotshadow.ErrorResponse) -> None
    cleanup("[aws] Update request was rejected. code:{} message:'{}'".format(
        error.code, error.message))


def on_get_shadow_accepted(response):
    # type: (iotshadow.GetShadowResponse) -> None
    print("[aws] Finished getting initial shadow state.")


def on_get_shadow_rejected(error):
    # type: (iotshadow.ErrorResponse) -> None
    if error.code == 404:
        print("[aws] Thing has no shadow document.")
    else:
        cleanup("[aws] Get request was rejected. code:{} message:'{}'".format(
            error.code, error.message))


def on_publish_update_shadow(future):
    # type: (Future) -> None
    try:
        future.result()
        print("[aws] Update request published.")
    except Exception as e:
        print("[aws] Failed to publish update request.")
        exit(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AWS IoT Client")
    parser.add_argument("-t", "--thing-name", help='AWS Thing Name',
                        required=True)
    parser.add_argument("-e", "--endpoint", help='AWS ATS Endpoint',
                        default="ats.iot.us-east-1.amazonaws.com")
    parser.add_argument("-p", "--provision-location",
                        help='Device provisioning folder', default="/prov")
    parser.add_argument("-c", "--cert-location", help='Certificates folder',
                        default="/certs")
    args = parser.parse_args()

    # setup interrupt signals
    # signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # setup AWS connection
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    # need a unique client id
    aws_mqtt = mqtt_connection_builder.mtls_from_path(
        endpoint=args.endpoint,
        cert_filepath="%s/device.crt" % (args.provision_location),
        pri_key_filepath="%s/device.key" % (args.provision_location),
        client_bootstrap=client_bootstrap,
        ca_filepath="%s/AmazonRootCA1.pem" % (args.cert_location),
        on_connection_interrupted=aws_on_connection_interrupted,
        on_connection_resumed=aws_on_connection_resumed,
        client_id=args.thing_name,
        clean_session=False,
        keep_alive_secs=AWS_KEEP_ALIVE_SECS)

    # connect loop
    conn_attempt = 1
    connected = False
    while not connected and conn_attempt <= AWS_CONNECT_ATTEMPTS:
        try:
            print("[aws] [%d] Connecting to %s as %s ..."
                  % (conn_attempt, args.endpoint, args.thing_name))
            connect_future = aws_mqtt.connect()
            connect_future.result()
            connected = True
        except:
            print("[aws] Failed connection: %s" % (sys.exc_info()[0]))
        time.sleep(AWS_CONNECT_DELAY_SECS)
        conn_attempt += 1
    if not connected:
        print("[aws] Failed all connection attempts. Restarting.")
        sys.exit(-1)

    print("[aws] Connected!")

    # create shadow client
    shadow_client = iotshadow.IotShadowClient(aws_mqtt)

    try:

        # subscribe to delta updates
        print("[aws] Subscribing to DELTA updates")

        delta_subscribed_future, _ = shadow_client.subscribe_to_shadow_delta_updated_events(
            request=iotshadow.ShadowDeltaUpdatedSubscriptionRequest(args.thing_name),
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=on_shadow_delta_updated)

        # Wait for subscription to succeed
        delta_subscribed_future.result()

        print("[aws] Subscribing to UPDATE responses")

        update_accepted_subscribed_future, _ = shadow_client.subscribe_to_update_shadow_accepted(
            request=iotshadow.UpdateShadowSubscriptionRequest(args.thing_name),
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=on_update_shadow_accepted)

        update_rejected_subscribed_future, _ = shadow_client.subscribe_to_update_shadow_rejected(
            request=iotshadow.UpdateShadowSubscriptionRequest(args.thing_name),
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=on_update_shadow_rejected)

        # Wait for subscriptions to succeed
        update_accepted_subscribed_future.result()
        update_rejected_subscribed_future.result()

        print("[aws] Subscribing to GET responses")
        get_accepted_subscribed_future, _ = shadow_client.subscribe_to_get_shadow_accepted(
            request=iotshadow.GetShadowSubscriptionRequest(args.thing_name),
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=on_get_shadow_accepted)

        get_rejected_subscribed_future, _ = shadow_client.subscribe_to_get_shadow_rejected(
            request=iotshadow.GetShadowSubscriptionRequest(args.thing_name),
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=on_get_shadow_rejected)

        # Wait for subscriptions to succeed
        get_accepted_subscribed_future.result()
        get_rejected_subscribed_future.result()

        # The response will be received by the on_get_accepted() callback
        print("[aws] Requesting current shadow state")
        publish_get_future = shadow_client.publish_get_shadow(
            request=iotshadow.GetShadowRequest(args.thing_name),
            qos=mqtt.QoS.AT_LEAST_ONCE)

        # Ensure that publish succeeds
        publish_get_future.result()

    except Exception as e:
        exit(e)

    publish_count = 1

    # Take initial reading
    psutil.cpu_percent(percpu=False)
    locked_data.thing_name = args.thing_name
    locked_data.before_ts = time.time()
    locked_data.ioBefore = psutil.net_io_counters()
    locked_data.diskBefore = psutil.disk_io_counters()
    psutil.disk_io_counters(perdisk=False, nowrap=True)

    while True:
        time.sleep(AWS_PUBLISH_DELAY_SECS)

        print("[aws] Updating shadow values [%d]" % (publish_count))
        data = locked_data.toJSON()
        request = iotshadow.UpdateShadowRequest(
            thing_name=args.thing_name,
            state=iotshadow.ShadowState(
                reported=data,
                desired=data,
            )
        )
        future = shadow_client.publish_update_shadow(request, mqtt.QoS.AT_LEAST_ONCE)
        future.add_done_callback(on_publish_update_shadow)

        publish_count += 1

# vim: set tabstop=4 shiftwidth=4 expandtab:
