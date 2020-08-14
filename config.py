
import os
import sys

KEY_FCM = "XXXXXXX"
SQS_QUE_URL_NOTIFICATIONS = "XXXXXXXXX"


def get_sqs_url():
    return SQS_QUE_URL_NOTIFICATIONS


def get_key_fcm():
    # return sys.argv[1]
    return KEY_FCM


def get_auth_secret():
    secret = sys.argv[2]
    private_value = secret.replace('_', '\n')
    return private_value

