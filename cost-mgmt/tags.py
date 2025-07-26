import boto3
from datetime import datetime, date, timedelta

ce = boto3.client('ce')

first = date.today().replace(day=1)
last_month = first - timedelta(days=1)
today = date.today()

response = ce.get_tags(
    TimePeriod={
        'Start': str(last_month),
        'End': str(today)
    },
    TagKey=''
)

print(response)
