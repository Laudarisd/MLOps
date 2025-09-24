# sample_slack_alert.py
"""
Sample code to send an alert to Slack using a webhook.
"""
import requests

webhook_url = 'https://hooks.slack.com/services/your/webhook/url'
data = {'text': '🚨 MLOps Alert: High job failure rate!'}
requests.post(webhook_url, json=data)
