import os
from slack_sdk import WebClient

def send(message, channel, username, token):

    # Set up a WebClient with the Slack OAuth token
    client = WebClient(token)

    # Send a message
    client.chat_postMessage(
        channel=channel, 
        text=message, 
        username=username
    )
