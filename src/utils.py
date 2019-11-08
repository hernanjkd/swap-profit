import os
import re
import hashlib
from flask import jsonify, url_for
from flask_jwt_simple import create_jwt
from datetime import datetime

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

# Raises an exception if required params not in body
def check_params(body, *args):
    msg = ''
    if body is None:
        msg = 'request body as a json object, '
    else:
        for prop in args:
            if prop not in body:
                msg += f'{prop}, '
    if msg:
        msg = re.sub(r'(.*),', r'\1 and', msg[:-2])
        raise Exception('You must specify the ' + msg, 400)

def update_table(table, body, ignore=[]):
    for attr, value in body.items():
        if attr not in ignore:
            if not hasattr(table, attr):
                raise APIException(f'Incorrect parameter in body: {attr}', 400)
            setattr(table, attr, value)

def validation_link(id):
    return os.environ.get('API_HOST') + '/users/validate/' + create_jwt({'id':id, 'role':'validating'})

def sha256(string):
    m = hashlib.sha256()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

def generate_sitemap(app):
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append(url)

    links_html = "".join(["<li>" + y + "</li>" for y in links])
    return """
        <div style="text-align: center;">
        <img src='https://assets.breatheco.de/apis/img/4geeks/rigo-baby.jpg' />
        <h1>Hello Rigo!!</h1>
        This is your api home, remember to specify a real endpoint path like: <ul style="text-align: left;">"""+links_html+"</ul></div>"
