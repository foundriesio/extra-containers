# flask-mqtt/app.py
import time
import sys

from flask import Flask
from flask_mqtt import Mqtt

access = 0
app = None
mqtt = None

def create_app():
  print("create_app")
  global app
  app = Flask(__name__)

  app.config['SECRET'] = 'my secret key'
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.config['MQTT_BROKER_URL'] = 'host.docker.internal'
  app.config['MQTT_BROKER_PORT'] = 1883
  app.config['MQTT_USERNAME'] = ''
  app.config['MQTT_PASSWORD'] = ''
  app.config['MQTT_KEEPALIVE'] = 5
  app.config['MQTT_TLS_ENABLED'] = False

  global mqtt
  mqtt = init_mqtt(app)

def init_mqtt(app):
  while True:
    try:
      print("init_mqtt: Connecting to MqTT Broker")
      return Mqtt(app)
    except:
      print("init_mqtt:", sys.exc_info()[0])
      time.sleep(10)

create_app()

@app.route('/')
def hello_world():
  global access
  return ('Number of Access on shellhttpd Container ' + str(access))

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('containers/requests')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
  if message.payload.decode().startswith('ACCESS='):
    value = message.payload.decode().split('=')
    if value[1].isnumeric():
      global access
      access = int(value[1])