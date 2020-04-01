
import json
import boto3
import config
import android_push_notification
import ios_push_notification

BULK_SIZE = 1000


def get_warning_level(status):
    if status == 0:
        return 0
    if status == 1:
        return 4
    if status == 2:
        return 2
    if status == 3:
        return 1
    return 3


def polling_queue():
    sqs_client = boto3.client('sqs',
                      aws_access_key_id=config.get_aws_key(),
                      aws_secret_access_key=config.get_aws_secret())

    queue_read = sqs_client.get_queue_by_name(QueueName=config.get_sqs_notifications_name())

    while 1:
        messages = queue_read.receive_messages(WaitTimeSeconds=20)

        for message in messages:
            print("Message received: {0}".format(message.body))

            body = json.loads(message.body)

            '''
            {
                'device_id': id_inter,
                'token': interaction2info[id_inter]['token'],
                'platform': interaction2info[id_inter]['platform'].lower(),
                'status': 3
            }
            '''
            if 'device_id' in body and 'token' in body and 'platform' in body and 'status' in body:
                d = {
                    'status': body['status'],
                    'warning_level': get_warning_level(body['status']),
                    'title': None,
                    'message': None,
                    'subtitle': None,
                    'link': None,
                    'language': None
                }
                if body['platform'] == 'ios':
                    ios_push_notification.send_push_notification(body['token'], d, production=True)
                else:
                    android_push_notification.send_push_notification(body['token'], d)

            message.delete()


if __name__ == '__main__':
    polling_queue()