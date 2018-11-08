#!/usr/bin/python3

import json
import logging
import os
import sys

import yaml

import requests
import paho.mqtt.client as paho
from sseclient import SSEClient

logging.basicConfig(
    level=os.environ.get('LOG_LEVEL', 'INFO'),
    format='[%(asctime)s] [%(levelname)s] %(message)s')
log = logging.getLogger('leshan-graphite')


def get_current_endpoints(api_config, endpoints):
    eplist = []
    url = api_config['url']
    if not url.endswith('/'):
        url += '/'
    url += 'api/clients'
    try:
        r = requests.get(url, timeout=0.1)
    except:
        log.error('Bad Things Happening!')
        exit(1)
    if r.status_code != 200:
        log.error('Unable to get client list: %s - %d\n%s',
                  url, r.status_code, r.text)
        exit(1)
    else:
        for client in json.loads(r.content.decode('utf-8')):
            if 'endpoint' in client:
                eplist.append(client['endpoint'])

    for endpoint in eplist:
        if endpoint not in endpoints:
            config = endpoints['default']
            endpoints.update({endpoint: config})

    return endpoints

def sseclient_from_config(subscriptions):
    api = subscriptions['leshan_api']
    url = api['url']
    if not url.endswith('/'):
        url += '/'
    url += 'event'
    try:
        return SSEClient(url, allow_redirects=api.get('allow_redirects'))
    except:
        exit(1)


def create_observations(api_config, endpoint, config):
    if endpoint != 'default':
        for ipso in config.get('observations', {}).keys():
            url = api_config['url']
            if not url.endswith('/'):
                url += '/'
            url += 'api/clients/%s%s/observe?format=TLV' % (endpoint, ipso)
            try:
                r = requests.post(url, headers=api_config.get('headers'), timeout=10)
            except:
                log.error('Bad Things Happening!')
                exit(1)
            if r.status_code != 200:
                log.error('Unable to register observation: %s - %d\n%s',
                          url, r.status_code, r.text)
            else:
                name = config.get('alias', endpoint)
                log.info('%s - created observation for: %s', name, ipso)


def on_notify(api_config, endpoints, client, event):
    epname = event['ep']
    ep = endpoints.get(epname)
    if ep:
        observation = ep.get('observations', {}).get(event['res'])
        if not observation:
            log.warn('%s got an unconfigured observation for: %s',
                     epname, event['res'])
            return
        name = ep.get('alias', epname)
        key = observation.get('alias', event['res'])
        val = event['val']['value']
        type = observation.get('type', 'str')
        if type == 'str':
            pass
        elif type == 'float':
            val = float(val)
        elif type == 'int':
            val = int(val)
        else:
            log.warn('Invalid observation type: %s', type)
        log.info('%s - observed %s = %s', name, key, val)
        mqtt = {}
        mqtt.update({key: val})
        topic = epname + '-' + name + '-' + key
        client.publish(topic, payload=json.dumps(mqtt), qos=0, retain=True)
        log.info('mqtt: %s - %s', topic, mqtt)


def on_updated(api_config, endpoints, client, event):
    endpoints = get_current_endpoints(api_config, endpoints)
    epname = event['endpoint']
    ep = endpoints.get(epname)
    if ep:
        name = ep.get('alias', epname)
        if event['registrationDate'] == event['lastUpdate']:
            log.info('%s - connected', name)
            create_observations(api_config, epname, ep)
        else:
            log.debug('%s - updated', name)


def on_deregistration(api_config, endpoints, client, event):
    epname = event['endpoint']
    ep = endpoints.get(epname)
    if ep:
        log.warn('%s - disconnected', ep.get('alias', epname))


def main(subscriptions):
    handlers = {
        'NOTIFICATION': on_notify,
        'UPDATED': on_updated,
        'REGISTRATION': on_updated,
        'DEREGISTRATION': on_deregistration,
    }
    api_config = subscriptions['leshan_api']
    endpoints = subscriptions['endpoints']
    mqtt = subscriptions['mqtt']
    log.info('Initialization Started')
    try:
        client = paho.Client()
        client.connect(mqtt['host'], mqtt['port'], 60)
        client.loop_start()
        log.info('MQTT Client Started')
    except:
        print("MQTT broker failed to connect, exiting...")
        exit(1)

    endpoints = get_current_endpoints(api_config, endpoints)
    for endpoint, config in endpoints.items():
        create_observations(api_config, endpoint, config)
    log.info('Initial Observations Registered')

    for event in sseclient_from_config(subscriptions):
        cb = handlers.get(event.event)
        if cb:
            cb(api_config, endpoints, client, json.loads(event.data))
    log.info('Server Side Callbacks Registered')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: %s <path to subscriptions.yml>' % sys.argv[0])

    with open(sys.argv[1]) as f:
        subscriptions = yaml.load(f)
    try:
        main(subscriptions)
    except KeyboardInterrupt:
        pass
