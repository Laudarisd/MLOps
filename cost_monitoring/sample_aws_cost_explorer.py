# sample_aws_cost_explorer.py
"""
Sample code to fetch AWS cost data using Boto3.
"""
import boto3

client = boto3.client('ce')
response = client.get_cost_and_usage(
    TimePeriod={
        'Start': '2023-09-01',
        'End': '2023-09-30'
    },
    Granularity='MONTHLY',
    Metrics=['UnblendedCost']
)
print(response['ResultsByTime'])
