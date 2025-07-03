import os
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
C_USER = os.getenv("C_USER")
XS = os.getenv("XS")

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

def get_latest_post():
    if not C_USER or not XS:
        raise Exception("❌ יש להגדיר את C_USER ו־XS כסודות.")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies([
            {"name": "c_user", "value": C_USER, "domain": ".facebook.com", "path": "/"},
            {"name": "xs", "value": XS, "domain": ".facebook.com", "path": "/"}
        ])
        page = context.new_page()
        page.goto("https://www.facebook.com/groups/fuadex", timeout=60000)
        page.wait_for_timeout(5000)
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        article = soup.find("div", attrs={"data-ad-preview": "message"})
        link_tag = soup.find("a", href=True)
        browser.close()
        if not article:
            return None, None, None
        text = article.get_text().strip()
        link = "https://www.facebook.com" + link_tag["href"] if link_tag else "https://www.facebook.com/groups/fuadex"
        post_id = hash(text)
        return text, link, post_id

def main():
    latest_path = "latestpost.txt"
    old_post_id = "0"
    if os.path.exists(latest_path):
        with open(latest_path, "r") as f:
            old_post_id = f.read().strip()
    text, link, post_id = get_latest_post()
    if text and str(post_id) != old_post_id:
        send_telegram_message(f"📢 פוסט חדש בקבוצת פואד:\n{text}\n{link}")
        with open(latest_path, "w") as f:
            f.write(str(post_id))
    else:
        print("❌ לא נמצא פוסט חדש.")

if __name__ == "__main__":
    main()
