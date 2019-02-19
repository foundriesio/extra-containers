# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from markupsafe import escape

import os
import time
import json
import requests

frontend = Blueprint('frontend', __name__)

headers = { 'Content-Type': 'application/json'}

def post(url):
    response = requests.post(url, headers=headers)
    if response.status_code == 200 or 201:
        return True
    else:
        return False

def put(url, data):
    response = requests.put(url, data=json.dumps(data), headers=headers)
    if response.status_code in (200, 201):
        return True
    else:
        return False

def get(url, raw=False):
    response = requests.get(url, headers=headers)
    if response.status_code in (200, 201):
        try:
            payload = json.loads(response.content)
        except:
            return None
        if raw:
            return payload
        else:
            if 'content' in payload:
                if 'value' in payload['content']:
                    return payload['content']['value']
    else:
        return None

def toggle_state(host, client):
    url = '%s/api/clients/%s/3311/0/5850' % (host, client)
    state = not get(url)
    nextstate = {'id': 5850, 'value': state}
    return put(url, nextstate)

def trigger(host, client):
    url = '%s/api/clients/%s/3340/0/5523' % (host, client)
    return post(url)

# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route("/dispense/", methods=['POST'])
def dispense():
    message = "Dispensing Candy..."
    host = os.environ['HOST']
    client = os.environ['CANDY_CLIENT']
    trigger(host, client)
    return render_template('index.html', message=message)

@frontend.route("/toggle/", methods=['POST'])
def light_toggle():
    message = "Toggling Light..."
    host = os.environ['HOST']
    client = os.environ['LIGHT_CLIENT']
    toggle_state(host, client)
    return render_template('index.html', message=message)
