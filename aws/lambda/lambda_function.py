# lambda_function.py
"""
Sample AWS Lambda function.
"""
def handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }
