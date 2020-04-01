
import os
import os.path
import time
import json
import jwt
from datetime import datetime
from hyper import HTTPConnection

TOKEN_FILE = os.getcwd() + '/token.json'
APNS_AUTH_KEY = os.getcwd() + '/AuthKey_MCV86KYH9U.p8'
ALGORITHM = 'ES256'
APNS_KEY_ID = 'MCV86KYH9U'
TEAM_ID = '652YXNAPUW'
BUNDLE_ID = 'org.covidapp-coronavirus-outbreak-control.ios'
SECONDS_DURATION_TOKEN = 3600
__token = None

# http://gobiko.com/blog/token-based-authentication-http2-example-apns/
# https://developer.apple.com/documentation/usernotifications/setting_up_a_remote_notification_server/sending_notification_requests_to_apns
# https://developer.apple.com/library/archive/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/CommunicatingwithAPNs.html
# https://developer.apple.com/documentation/usernotifications/setting_up_a_remote_notification_server/handling_notification_responses_from_apns


def save_token(token_obj):
    with open(TOKEN_FILE, 'w') as f:
        f.write(json.dumps(token_obj))


def read_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, 'r') as f:
        try:
            j = json.load(f)
        except json.JSONDecodeError:
            # empty file
            return None
        if j is None or 'token' not in j:
            return None
        if datetime.fromtimestamp(j['unix_elapsed_time']) < datetime.now():
            return None
        return j


def generate_token():

    f = open(APNS_AUTH_KEY)
    secret = f.read()

    tkn = jwt.encode(
        {
            'iss': TEAM_ID,
            'iat': time.time()
        },
        secret,
        algorithm=ALGORITHM,
        headers={
            'alg': ALGORITHM,
            'kid': APNS_KEY_ID,
        }
    ).decode('ascii')

    return tkn


def get_token():
    global __token

    if __token is None:
        __token = read_token()

    if __token is None:
        token_string = generate_token()
        __token = {
            'token': token_string,
            'unix_elapsed_time': (datetime.now() - datetime(1970, 1, 1)).total_seconds() + SECONDS_DURATION_TOKEN
        }
        save_token(__token)
    return __token


def send_push_notification(device_token, data, production=True, is_retry=False):
    t = get_token()

    path = '/3/device/{0}'.format(device_token)
    token = t['token']
    request_headers = {
        'apns-expiration': '0',
        'apns-priority': '5',
        'apns-topic': BUNDLE_ID,
        'apns-push-type': 'background',
        'authorization': 'bearer {0}'.format(token)
    }
    payload_data = {
        'aps': {
            'content-available': 1
        },
        'data': data
    }

    payload = json.dumps(payload_data).encode('utf-8')

    if production:
        conn = HTTPConnection('api.push.apple.com:443')
    else:
        conn = HTTPConnection('api.sandbox.push.apple.com:443')

    conn.request(
        'POST',
        path,
        payload,
        headers=request_headers
    )

    resp = conn.get_response()
    print(resp.status)
    if resp.status >= 300:
        resp_error = resp.read()
        print(resp_error)
        # remove token
        save_token(None)
        if not is_retry and resp.status == 400:
            j = json.loads(resp_error.decode('ascii'))
            if 'reason' in j and j['reason'] == 'BadDeviceToken':
                print('gonna try development environment iOS')
                send_push_notification(device_token, data, production=not production, is_retry=True)


def test_token():
    print(get_token())

    """
    HOW TO SEND PUSH NOTIFICATION
    """
    device_token = 'e7376a4041d2ddbe1b088895504b5be04847456c4ffdeb61d97dc4edc45fbca2'
    d = {
        'status': 2,
        'warning_level': 1,
        'title': 'Title',
        'message': 'Message',
        'subtitle': None,
        'link': None,
        'language': None
    }
    send_push_notification(device_token, d, production=True)


if __name__ == '__main__':
    test_token()