import os
import requests
import uuid

from urllib.parse import urlencode

import json

from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import session


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '123')


class NetatmoClient(object):
    NETATMO_BASE_URL = 'https://api.netatmo.com/{}'
    NETATMO_APP_ID = os.environ['NETATMO_APP_ID']
    NETATMO_CLIENT_SECRET = os.environ['NETATMO_CLIENT_SECRET']
    HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def _get(self, url):
        return requests.get(url)

    def _post(self, url, data):
        return requests.post(url, data=data, headers=self.HEADERS)

    def get_response(self, url, access_token):
        return self._get(self.NETATMO_BASE_URL.format('{}?access_token={}'.format(url, access_token))).json()

    def get_access_token(self, params):
        response = self._post(self.NETATMO_BASE_URL.format('oauth2/token'), data=params)
        try:
            response = response.json()
            return response.get('access_token'), response.get('refresh_token')
        except:
            return None

    def authorize(self, params):
        return self.NETATMO_BASE_URL.format('oauth2/authorize?{}'.format(urlencode(params)))

client = NetatmoClient()


def return_json(response):
    return app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )


@app.route('/', methods=['GET'])
def devices():
    access_token = None
    code = request.args.get('code')
    if code:
        params = {
            'grant_type': 'authorization_code',
            'client_id': client.NETATMO_APP_ID,
            'client_secret': client.NETATMO_CLIENT_SECRET,
            'code': code,
            'redirect_uri': request.url
        }
        access_token, refresh_token = client.get_access_token(params)
        if access_token:
            session['access_token'] = access_token
            session['refresh_token'] = refresh_token

    elif 'access_token' in session:
        access_token = session['access_token']
        refresh_token = session['refresh_token']
    
    if access_token:
        response = client.get_response('api/partnerdevices', access_token)

        if 'error' in response:
            error_code = response.get('error', {}).get('code')
            
            if error_code == 31:
                return return_json(response)

            if error_code == 3:
                return redirect('/refresh')

            return str(response)

    return return_json({
        'message': 'No login identify, click the link for show your devices',
        'link': request.url + 'login'
    })


@app.route('/refresh', methods=['GET'])
def refresh():
    # session['access_token'] = None
    # session['refresh_token'] = None
    return redirect('/')


@app.route('/logout', methods=['GET'])
def logout():
    session['access_token'] = None
    session['refresh_token'] = None
    return redirect('/')


@app.route('/login', methods=['GET'])
def login():
    params = {
        'redirect_uri': request.url.replace(request.path, '/'),
        'client_id': client.NETATMO_APP_ID,
        'scope': 'read_station',
        'state': uuid.uuid4(),
    }
    return redirect(client.authorize(params))


if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT', 8000)))
