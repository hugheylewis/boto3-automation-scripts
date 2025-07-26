import boto3
import format_date
from instances import instance_id
from format_date import format_date, start_date, end_date

ce = boto3.client('ce')
tag_key = 'cost-center'


filter_expression = {
    "Tags": {
        "Key": tag_key,
        "Values": ["*"]
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
            'Type': 'TAG',
            'Key': tag_key
        },
        {
            'Type': 'DIMENSION',
            'Key': 'SERVICE'  # breaks down costs by service
        },
    ],
)

# # Debugging empty results where 'Groups': []
# print(response)

results = response['ResultsByTime']
print(results)
tag_cost = {}

for result in results:
    formatted_date = format_date(result['TimePeriod']['End'])
    for group in result['Groups']:
        tag_value = group['Keys'][0].replace('TAG$', '') or 'Untagged'
        service = group['Keys'][1]
        cost = group['Metrics']['UnblendedCost']['Amount']
        if tag_value not in tag_cost:
            tag_cost[tag_value] = {}
        if formatted_date not in tag_cost[tag_value]:
            tag_cost[tag_value][format_date] = {}

        tag_cost[tag_value][format_date][service] = float(cost)

for tag_value, dates in tag_cost.items():
    print(f"Tag Value: {tag_value}")
    for date, services in dates.items():
        for service, cost in services.items():
            print(f"\t{date} - {service}: ${cost:.4f}")