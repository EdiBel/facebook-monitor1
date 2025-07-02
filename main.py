import requests

from bs4 import BeautifulSoup

import os



GROUP_URL = "https://www.facebook.com/groups/fuadex/?sorting_setting=CHRONOLOGICAL"



headers = {

    "User-Agent": "Mozilla/5.0"

}



cookies = {

    "c_user": os.environ["C_USER"],

    "xs": os.environ["XS"]

}



def get_latest_post_id():

    response = requests.get(GROUP_URL, headers=headers, cookies=cookies)

    

    # הדפסה של כל תוכן הדף

    print("======= HTML CONTENT START =======")

    print(response.text[:2000])  # מדפיס רק את 2000 התווים הראשונים

    print("======= HTML CONTENT END =======")



    if "You must log in" in response.text or "login" in response.url:

        print("⚠️ לא הצלחנו לגשת לקבוצה — ייתכן שהקוקיז לא תקינים")

        return None



    soup = BeautifulSoup(response.text, "html.parser")



    for a in soup.find_all("a", href=True):

        href = a["href"]

        if "/groups/fuadex/permalink/" in href:

            return href.split("/")[4]



    return None



def send_email(subject, body):

    import smtplib

    from email.message import EmailMessage



    msg = EmailMessage()

    msg.set_content(body)

    msg["Subject"] = subject

    msg["From"] = os.environ["EMAIL_FROM"]

    msg["To"] = os.environ["EMAIL_TO"]



    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(os.environ["EMAIL_FROM"], os.environ["EMAIL_PASS"])

        smtp.send_message(msg)



def main():

    latest_file = "latest_post.txt"

    try:

        with open(latest_file, "r") as f:

            last_post_id = f.read().strip()

    except FileNotFoundError:

        last_post_id = "0"



    current_post_id = get_latest_post_id()

    print(f"last_post_id: {last_post_id}")

    print(f"current_post_id: {current_post_id}")



    if current_post_id and current_post_id != last_post_id:

        print("📢 פוסט חדש זוהה! שליחת מייל...")

        send_email("📢 פוסט חדש בקבוצת פואד", f"https://www.facebook.com/groups/fuadex/permalink/{current_post_id}")

        with open(latest_file, "w") as f:

            f.write(current_post_id)

    else:

        print("❌ לא נמצא פוסט חדש.")



if __name__ == "__main__":

    main()

