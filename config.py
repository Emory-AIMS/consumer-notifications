
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def get_aws_key():
    return config['CONFIG']['AWS_ACCESS_KEY']


def get_aws_secret():
    return config['CONFIG']['AWS_SECRET_KEY']


def get_sqs_notifications_name():
    return config['CONFIG']['SQS_QUE_NAME_NOTIFICATIONS']


def get_key_fcm():
    return config['CONFIG']['KEY_FCM']
