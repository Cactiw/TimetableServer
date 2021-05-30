
from config import NOTIFY_BOT_TOKEN

import requests
import logging


def send_notify(user_id: int, text: str):
    telegram_response = requests.post(
        "https://api.telegram.org/bot{}/sendMessage".format(NOTIFY_BOT_TOKEN),
        json={
            "chat_id": user_id,
            "text": text,
            "parse_mode": "HTML"
        }
    )
    logging.info("Telegram response: {}".format(telegram_response))

