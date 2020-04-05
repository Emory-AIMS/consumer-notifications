
import os
import configparser


def get_key_fcm():
    # return config['CONFIG']['KEY_FCM']
    return os.environ['KEY_FCM']


def get_auth_secret():
    secret = os.environ['AUTH_SECRET']
    private_value = secret.replace('\\n', '\n')
    return private_value

