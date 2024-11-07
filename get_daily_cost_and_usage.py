import boto3
from datetime import datetime, timedelta, timezone

def format_date(date_str):
    """Function to format the date with the day of the week and suffix (st, nd, rd, and th)"""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    day_of_week = date_obj.strftime('%A')
    day = date_obj.day

    if 10 <= day <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

    formatted_date = date_obj.strftime(f'{day_of_week}, %B {day}{suffix}, %Y')
    return formatted_date

client = boto3.client('ce')
end_date = datetime.now(timezone.utc).date()
start_date = (datetime.now(timezone.utc) - timedelta(days=14)).date()

response = client.get_cost_and_usage(
    TimePeriod={
        'Start': str(start_date),
        'End': str(end_date)
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

for result in response['ResultsByTime']:
    if result['Groups']:
        amount = result['Groups'][0]['Metrics']['UnblendedCost']['Amount']
        end_date = result['TimePeriod']['End']
        formatted_date = format_date(end_date)
        print(f"Daily cost for {formatted_date}: {amount} USD")
    else:
        end_date = result['TimePeriod']['End']
        formatted_date = format_date(end_date)
        print(f"Daily cost for {formatted_date}: No data available")

