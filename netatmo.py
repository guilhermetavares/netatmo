import os
import requests
import uuid
import json

from urllib.parse import urlencode

from flask import Flask, request, redirect, session


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


@app.route('/authenticate', methods=['GET'])
def authenticate():
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
            return redirect('/devices')
    return redirect('/')


@app.route('/devices', methods=['GET'])
def devices():
    if 'access_token' in session:
        access_token = session['access_token']
        refresh_token = session['refresh_token']
    
        response = client.get_response('api/partnerdevices', access_token)

        if 'error' in response:
            error_code = response.get('error', {}).get('code')
            
            if error_code == 31: # no devices
                return return_json(response)

            if error_code in [2, 3]: # reload token
                return redirect('/refresh')
        else:
            return str(response)
    return redirect('/')


@app.route('/refresh', methods=['GET'])
def refresh():
    if 'refresh_token' in session:
        refresh_token = session['refresh_token']
        params = {
            'grant_type': 'refresh_token',
            'client_id': client.NETATMO_APP_ID,
            'client_secret': client.NETATMO_CLIENT_SECRET,
            'refresh_token': refresh_token,
        }
        access_token, refresh_token = client.get_access_token(params)
        if access_token:
            session['access_token'] = access_token
            session['refresh_token'] = refresh_token
            return redirect('/')

    return redirect('/login')


@app.route('/', methods=['GET'])
def home():
    if 'access_token' in session:
        return return_json({
            'message': 'You is logged in with the netatmo account',
            'devices': request.url + 'devices',
            'logout': request.url + 'logout',
        })
    return return_json({
        'message': 'No login identify, click the link for show your devices',
        'link': request.url + 'login'
    })


@app.route('/logout', methods=['GET'])
def logout():
    session['access_token'] = None
    session['refresh_token'] = None
    return redirect('/')


@app.route('/login', methods=['GET'])
def login():
    params = {
        'redirect_uri': request.url.replace(request.path, '/authenticate'),
        'client_id': client.NETATMO_APP_ID,
        'scope': 'read_station',
        'state': uuid.uuid4(), # for futher verification
    }
    return redirect(client.authorize(params))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)))
