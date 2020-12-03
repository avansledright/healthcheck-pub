import logging
logging.basicConfig(level=logging.DEBUG)

import os
from slack import WebClient
from slack.errors import SlackApiError


slack_token = os.environ["slackBot"]
client = WebClient(token=slack_token)

def lambda_handler(event, context):
    detail = event['Records'][0]['Sns']['Message']
    response_string = f"{detail}"
    try:
        response = client.chat_postMessage(
            channel="YOUR CHANNEL HERE",
            text="SERVER DOWN",
            blocks = [{"type": "section", "text": {"type": "plain_text", "text": response_string}}]
        )   

    except SlackApiError as e:
        assert e.response["error"]
    return