import json
import boto3

# Un-Comment below if you want to send slack alerts
#import requests
#import os
# Environment Variables
# SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK')


def get_instance_client(region):
    """
    It will return EC2 client
    """
    client = boto3.client('ec2', region_name=region)
    return client


def stop_instance_client(region, instance_id):
    """
    It will stop the instance
    """
    client = get_instance_client(region)

    try:
        client.stop_instances(InstanceIds=[instance_id])
    except Exception as e:
        print("Instance " + str(instance_id) + " not found.")
        print(e)


def action_main(event):

    region = str(event["region"])
    target_instance_id = event["detail"]["resource"]["instanceDetails"]["instanceId"]

    # stopping instance
    stop_instance_client(region, target_instance_id)

    # Un-Comment block below to enable Slack alerts
'''
    remote_ip = str(event["detail"]["service"]["action"]["networkConnectionAction"]["remoteIpDetails"]["ipAddressV4"])
    headers = {'Content-type': 'application/json'}
    notification = {
            "username": "EC2 C&C Alert",
            "icon_emoji": ":rotating_light:",
            "text": "Instance " + target_instance_id + " is stopped due to Command and Control activity detected from  " + remote_ip
        }

    requests.post(url=SLACK_WEBHOOK, data=json.dumps(notification), headers=headers)
'''
def lambda_handler(event, context):
    """
    Lambda handler
    """
   # print(event)
    action_main(event)
