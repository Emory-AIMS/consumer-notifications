
import os.path
import time
import json
import jwt
import config
from datetime import datetime
from hyper import HTTPConnection

TOKEN_FILE = os.getcwd() + '/token.json'

ALGORITHM = 'ES256'
APNS_KEY_ID = 'MCV86KYH9U'
TEAM_ID = '652YXNAPUW'
BUNDLE_ID = 'org.covidapp-coronavirus-outbreak-control.ios'
SECONDS_DURATION_TOKEN = 3600

# http://gobiko.com/blog/token-based-authentication-http2-example-apns/
# https://developer.apple.com/documentation/usernotifications/setting_up_a_remote_notification_server/sending_notification_requests_to_apns
# https://developer.apple.com/library/archive/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/CommunicatingwithAPNs.html
# https://developer.apple.com/documentation/usernotifications/setting_up_a_remote_notification_server/handling_notification_responses_from_apns


def generate_token():

    secret = config.get_auth_secret()

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
    token_string = generate_token()
    tkn = {
        'token': token_string,
        'unix_elapsed_time': (datetime.now() - datetime(1970, 1, 1)).total_seconds() + SECONDS_DURATION_TOKEN
    }
    return tkn


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