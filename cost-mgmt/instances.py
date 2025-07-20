import boto3
from datetime import datetime, timedelta, timezone

ec2 = boto3.client('ec2', region_name='us-east-2')
instance_id = ''
response = ec2.describe_instances(    
    Filters=[
        {
            'Name': 'tag:cost-center',
            'Values': [
                'lab',
            ]
        },
    ]
)

for instances in response['Reservations']:
    for instance in instances['Instances']:
        instance_id = instance['InstanceId']

print(instance_id)