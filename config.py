
import os
import sys


def get_sqs_url():
    return 'https://sqs.us-east-1.amazonaws.com/746726732930/potential-infected-notification'


def get_key_fcm():
    return sys.argv[1]


def get_auth_secret():
    secret = sys.argv[2]
    private_value = secret.replace('_', '\n')
    return private_value

