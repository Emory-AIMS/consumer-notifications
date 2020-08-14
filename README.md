# How it works

The consumer make a polling on the `potential-infected-notification` queue and send notification to the devices. Make sure the machine have access to the AWS queue

# Deployment instructions

## Requirments 

- Python 3
- Pip 3
- Boto3
- requests
- hyper

## Step 1 - Download repository

Download repository (we will put it on ~/consumer-notifications folder)

## Step 2 - Config.py 

Edit following constants in `/config.py` file:
```
KEY_FCM = "XXXXXXX"
SQS_QUE_URL_NOTIFICATIONS = "XXXXXXX"
```
## Step 3 - Setup service

Get the current user, type `# whoami`

Open `consumer-notifications.service` and edit the `user` value with the name of the current user.

In order to set `consumer-notifications.service` as systemctl service, create a symlink of our service
```bash
sudo ln -s ~/consumer-notifications/consumer-notifications.service /etc/systemd/system/consumer-notifications.service
```
Go in the system directory
```bash
cd /etc/systemd/system/
```
Start the service:
```bash
systemctl start consumer-notifications.service
```
And automatically get it to start at boot:
```bash
systemctl enable ~/consumer-notifications/consumer-notifications.service
```
To test the system, simply type:
```bash
systemctl status consumer-notifications.service
```
The output should be something like:
```bash
 consumer-notifications.service - Consumer Notifications.
   Loaded: loaded
   Active: active (running)
```

