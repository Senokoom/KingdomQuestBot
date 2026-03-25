import requests
from settings import BOT_KEY

API_URL = f"https://api.telegram.org/bot{BOT_KEY}/"

def get_updates(offset=None):
    url = API_URL + "getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()


def send_message(chat_id, text):
    url = API_URL + "sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, data=data)

