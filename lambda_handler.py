
import json
import ios_push_notification
import android_push_notification
from utils_notifications import get_warning_level


# ZIP FUNCTION: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-dependencies


def handle(event, context):
    print('new event received', event)
    for record in event['Records']:
        print("test")
        if "body" not in record:
            print('body not found')
            continue
        payload = json.loads(record["body"])
        print(str(payload))

        if 'notifications' in payload:
            for notification in payload['notifications']:
                if 'device_id' in notification and 'token' in notification \
                        and 'platform' in notification and 'status' in notification and 'data' in notification:
                    d = notification['data']
                    if notification['platform'] == 'ios':
                        ios_push_notification.send_push_notification(notification['token'], d, production=True)
                    else:
                        android_push_notification.send_push_notification(notification['token'], d)
