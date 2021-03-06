#!/usr/bin/env python

from os import getenv

import bottle
from bottle import response, request, HTTPError

from meeseeks import Meeseeks

app = application = bottle.Bottle()
_config = {
    'auth_token': getenv('MEESEEKS_AUTH_TOKEN')
}
_meeseeks = Meeseeks()


def _get_meeseeks():
    return _meeseeks


def _validate_auth(req):
    is_valid = False
    if _config['auth_token'] is None:
        is_valid = True
    elif 'auth_token' in req.query:
        is_valid = req.query['auth_token'] == _config['auth_token']
    if not is_valid:
        raise HTTPError(401)


def _set_default_response_type():
    response.content_type = 'application/json'
    response.set_header('Content-Language', 'en')
    response.set_header('Cache-control', 'private')


@app.post('/webhook/')
def post_webhook():
    _set_default_response_type()
    _validate_auth(request)
    if not request.json:
        raise HTTPError(400, 'Content-Type application/json required')

    if 'item' not in request.json:
        raise HTTPError(400, 'Missing item')
    return _get_meeseeks().handle_room_message_item(request.json['item'])


@app.get('/descriptor/')
def get_descriptor():
    _set_default_response_type()
    _validate_auth(request)
    return _get_meeseeks().get_descriptor('%s://%s' % (request.urlparts.scheme, request.urlparts.hostname),
                                          _config['auth_token'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8070)
