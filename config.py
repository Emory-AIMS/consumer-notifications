
import os
import sys

KEY_FCM = "XXXXXXX"


def get_sqs_url():
    return 'https://sqs.us-west-1.amazonaws.com/018890560418/potential-infected-notification'


def get_key_fcm():
    # return sys.argv[1]
    return KEY_FCM


def get_auth_secret():
    secret = sys.argv[2]
    private_value = secret.replace('_', '\n')
    return private_value

