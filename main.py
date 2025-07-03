import os
import time
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# הגדרות טלגרם
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# הגדרות קוקיז
C_USER = os.getenv("C_USER")
XS = os.getenv("XS")

def send_telegram_message(message: str):
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
print("❌ טלגרם לא מוגדר, מדלג על שליחה.")
return
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
data = {
"chat_id": TELEGRAM_CHAT_ID,
"text": message
}
try:
res = requests.post(url, data=data)
if res.status_code == 200:
print("✅ נשלחה הודעה בטלגרם.")
else:
print(f"⚠️ שגיאה בשליחת הודעת טלגרם: {res.text}")
except Exception as e:
print(f"⚠️ שגיאת טלגרם: {e}")

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
print("🌐 טוען את קבוצת פואד...")
page.goto("https://www.facebook.com/groups/fuadex", timeout=60000)
time.sleep(5)
html = page.content()
soup = BeautifulSoup(html, "html.parser")
posts = soup.find_all("div", attrs={"data-ad-comet-preview": "message"})
browser.close()

if not posts:
raise Exception("❌ נראה שלא בוצע התחברות לחשבון הפייסבוק.")

first_post = posts[0]
post_text = first_post.get_text(strip=True)
link_tag = first_post.find("a", href=True)
post_link = "https://www.facebook.com" + link_tag["href"] if link_tag else ""

post_id = first_post.get("id", "no-id")

return post_text, post_link, post_id

def main():
try:
text, link, post_id = get_latest_post()
print("📢 פוסט חדש מזוהה לבדיקה...")
if not os.path.exists("latest_post.txt"):
with open("latest_post.txt", "w") as f:
f.write(post_id)
send_telegram_message(f"📢 פוסט חדש בקבוצת פואד:\n{text}\n{link}")
else:
with open("latest_post.txt", "r") as f:
last_post_id = f.read().strip()
if post_id != last_post_id:
with open("latest_post.txt", "w") as f:
f.write(post_id)
send_telegram_message(f"📢 פוסט חדש בקבוצת פואד:\n{text}\n{link}")
else:
print("ℹ️ אין פוסט חדש.")
except Exception as e:
print(str(e))

if __name__ == "__main__":
main()
