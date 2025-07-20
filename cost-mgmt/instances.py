import boto3
from format_date import format_date, start_date, end_date

ec2 = boto3.client('ec2', region_name='us-east-2')
ce = boto3.client('ce')
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
