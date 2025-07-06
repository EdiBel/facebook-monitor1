import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    print("Status code:", response.status_code)
    print("Response:", response.text)

def main():
    # פוסט לדוגמה
    post_text = "📢 פוסט חדש לדוגמה מהקבוצה!"
    post_link = "https://www.facebook.com/groups/fuadex/permalink/123456789/"
    message = f"{post_text}\n\n🔗 <a href='{post_link}'>לצפייה בפוסט</a>"

    send_telegram_message(message)

if __name__ == "__main__":
    main()
