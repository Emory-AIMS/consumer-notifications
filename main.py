
import json
import boto3
import config
import android_push_notification
import ios_push_notification
from utils_notifications import get_warning_level


def polling_queue():
    sqs_client = boto3.resource('sqs')

    queue_read = sqs_client.Queue(config.get_sqs_url())

    while 1:
        messages = queue_read.receive_messages(WaitTimeSeconds=5, MaxNumberOfMessages=10)
        print('MESSAGE')
        for message in messages:
            
            payload = json.loads(message.body)

            if 'notifications' in payload:
                for notification in payload['notifications']:
                    print(notification)
                    if 'token' in notification and 'platform' in notification and 'data' in notification:
                        d = notification['data']
                        if notification['platform'] == 'ios':
                            ios_push_notification.send_push_notification(notification['token'], d, production=True)
                        else:
                            android_push_notification.send_push_notification(notification['token'], d)

            message.delete()


if __name__ == '__main__':
    polling_queue()