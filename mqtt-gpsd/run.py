import gpsd
import time
import json
import paho.mqtt.client as paho

try:
    gpsd.connect(host="127.0.0.1", port=2947)
except:
    print("GPSD failed to connect, exiting...")
    exit(1)

try:
    client = paho.Client()
    client.connect("127.0.0.1", 1883, 60)
except:
    print("MQTT broker failed to connect, exiting...")
    exit(1)

try:
    while True:
        mqtt = {}
        packet = gpsd.get_current()
        position = packet.position()
        speed = packet.speed()
        mqtt.update({'latitude': position[0]})
        mqtt.update({'longitude': position[1]})
        mqtt.update({'speed': speed})
        mqtt.update({'time': packet.time})
        mqtt.update({'sats': packet.sats})
        client.publish("rpi3-02-gps", payload=json.dumps(mqtt), qos=0, retain=True)
        print(mqtt)
        time.sleep(5)
except KeyboardInterrupt:
    print("Exiting...")
except:
    print("No GPS lock, spinning...")
