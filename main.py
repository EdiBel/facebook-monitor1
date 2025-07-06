import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")

def main():
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise Exception("❌ יש להגדיר את TELEGRAM_BOT_TOKEN ו־TELEGRAM_CHAT_ID כסודות.")
    
    send_telegram_message("✅ בדיקת טלגרם: זה פוסט דוגמה שנשלח אוטומטית.")

if __name__ == "__main__":
    main()
