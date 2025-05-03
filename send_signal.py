import requests

TOKEN = '7947328586:AAGhTyJ8bSMU0BrfcXrIPx9SFocZJk9u5WQ'
CHAT_ID = '5879164044'

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        return response.json()
    except Exception as e:
        print(f"Ошибка Telegram: {e}")
