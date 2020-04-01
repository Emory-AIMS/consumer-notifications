
import json
import requests
import config

# https://firebase.google.com/docs/cloud-messaging/send-message
# https://medium.com/android-school/test-fcm-notification-with-postman-f91ba08aacc3

KEY_FCM = config.get_key_fcm()


def send_push_notification(device_token, data):
    payload_data = {
        'to': device_token,
        'data': data
    }

    res = requests.post('https://fcm.googleapis.com/fcm/send',
                        headers={
                            'Content-type': 'application/json',
                            'Authorization': 'key=' + KEY_FCM
                        },
                        data=json.dumps(payload_data))

    print('android response code', res.status_code)


def test():
    """
    HOW TO SEND PUSH NOTIFICATION
    """
    device_token = 'c2kplQP0TT63LmjJVAFQO4:APA91bFidizNVdIsu32ele3rh_YATwTnn9YP_uzWpX02c7K8Qs9Q0DCybvWmWurosN1E1mzvESJlGggj2EAoFTUIPjwoY2cnZvvJIMBNCVotB31oIyOeSZuf3TKTQq8ur1wEv-5WXvwY'
    d = {
        'status': 2,
        'warning_level': 1,
        'title': 'Title',
        'message': 'Message',
        'subtitle': None,
        'link': None,
        'language': None
    }
    send_push_notification(device_token, d)


if __name__ == '__main__':
    test()
