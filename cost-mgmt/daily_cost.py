import boto3
import format_date
from instances import instance_id
from format_date import format_date, start_date, end_date

ce = boto3.client('ce')
filter_expression = {
    "Tags": {
        "Key": 'cost-center',
        "Values": [instance_id]
    }
}

response = ce.get_cost_and_usage(
    TimePeriod={
        'Start': str(start_date),
        'End': str(end_date)
    },
    Granularity='DAILY',
    Filter=filter_expression,
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

# # Debugging empty results where 'Groups': []
# print(response)

results = response['ResultsByTime']

user_cost_dict = {'127214166810': {}}
for result in results:
    end_date = result['TimePeriod']['End']
    formatted_date = format_date(end_date)
    if result['Groups']:
        instance_id = result['Groups'][0]['Keys'][0]
        instance_cost = result['Groups'][0]['Metrics']['UnblendedCost']['Amount']
        user_cost_dict[instance_id][formatted_date] = instance_cost
    else:
        print(f"No costs have accrued for {end_date}")

for user_id, nested_date in user_cost_dict.items():
    print(f"User ID: {user_id}")
    for date, cost in nested_date.items():
        print(f"\t{date}: ${cost}")