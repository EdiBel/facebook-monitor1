import os
import smtplib
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup

EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

GROUP_URL = "https://www.facebook.com/groups/fuadex/?sorting_setting=CHRONOLOGICAL"
LAST_POST_FILE = "last_post.txt"

def get_latest_post_url():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": f"c_user={os.environ.get('C_USER')}; xs={os.environ.get('XS')};"
    }
    response = requests.get(GROUP_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href and "/groups/fuadex/permalink/" in href:
            return "https://www.facebook.com" + href.split("?")[0]
    return None

def send_email(subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

def main():
    latest_post = get_latest_post_url()
    if not latest_post:
        print("לא נמצא פוסט")
        return

    last_post = ""
    if os.path.exists(LAST_POST_FILE):
        with open(LAST_POST_FILE, "r") as f:
            last_post = f.read().strip()

    if latest_post != last_post:
        print("פוסט חדש! שולח מייל")
        send_email("📢 פוסט חדש בקבוצת פואד", latest_post)
        with open(LAST_POST_FILE, "w") as f:
            f.write(latest_post)
    else:
        print("אין פוסט חדש")

if __name__ == "__main__":
    main()