import boto3
import format_date
from datetime import datetime, timedelta, timezone

client = boto3.client('ce')

response = client.get_cost_and_usage(
    TimePeriod={
        'Start': str(format_date.start_date),
        'End': str(format_date.end_date)
    },
    Granularity='DAILY',
    Filter={
        'Dimensions': {
            'Key': 'SERVICE',
            'Values': [
                'Amazon Elastic Compute Cloud - Compute',
            ],
        },
    },
    Metrics=[
        'UnblendedCost',
    ],
    GroupBy=[
        {
            'Type': 'DIMENSION',
            'Key': 'LINKED_ACCOUNT'
        },
    ],
)

results = response['ResultsByTime']

# Get most expensive EC2 instances
# TODO: Need to find the instance ID what incurred the cost. Currently, `instance_id` is actually the owner ID (which is still good for accountability purposes)
# uneeded list comprehension: 
# expensive_daily_services = [result['Groups'][0]['Metrics']['UnblendedCost']['Amount'] for result in results if result['Groups']]

instance_cost_dict = {'127214166810': {}}
for result in results:
    end_date = result['TimePeriod']['End']
    formatted_date = format_date.format_date(end_date)
    if result['Groups']:
        instance_id = result['Groups'][0]['Keys'][0]
        instance_cost = result['Groups'][0]['Metrics']['UnblendedCost']['Amount']
        instance_cost_dict[instance_id][formatted_date] = instance_cost

for user_id, nested_date in instance_cost_dict.items():
    print(f"User ID: {user_id}")
    for date, cost in nested_date.items():
        print(f"\t{date}: ${cost}")