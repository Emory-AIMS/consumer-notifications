
import os


def get_sqs_url():
    return 'https://sqs.us-east-1.amazonaws.com/746726732930/potential-infected-notification'


def get_key_fcm():
    # return config['CONFIG']['KEY_FCM']
    return os.environ['KEY_FCM']


def get_auth_secret():
    secret = os.environ['AUTH_SECRET']
    private_value = secret.replace('\\n', '\n')
    return private_value

