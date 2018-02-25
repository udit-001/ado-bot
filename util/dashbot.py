import json

import requests

import config


def track_user(update):
    url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=incoming&apiKey={0}'.format(config.dashbot_token)

    data = {
        "text": update.message.text,
        "userId": update.effective_user.id,
    }

    requests.post(url, data=json.dumps(data), headers={'Content-type':'application/json'})