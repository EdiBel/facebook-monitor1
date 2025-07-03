import os
import requests
from playwright.sync_api import sync_playwright

def send_telegram_message(message: str):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        print("❌ Bot token or chat ID missing.")
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("📬 הודעה נשלחה בטלגרם")
    else:
        print(f"❌ שגיאה בשליחת הודעה לטלגרם: {response.text}")

def get_latest_post():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies([
            {"name": "c_user", "value": os.environ["C_USER"], "domain": ".facebook.com", "path": "/"},
            {"name": "xs", "value": os.environ["XS"], "domain": ".facebook.com", "path": "/"},
        ])
        page = context.new_page()
        page.goto("https://www.facebook.com/groups/fuadex", timeout=60000)
        page.wait_for_timeout(5000)
        html = page.content()
        if "הצטרף לקבוצה" in html:
raise Exception("❌ נראה שלא בוצע התחברות לחשבון הפייסבוק.")
