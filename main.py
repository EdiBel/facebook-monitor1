
def get_latest_post():
    # סימולציה של פוסט חדש לצורכי בדיקה
    return "פוסט בדיקה 🎯", "https://facebook.com/test_post_123", "test_post_123"

def send_email(subject, body):
    print(f"Subject: {subject}\n{body}")

def main():
    text, link, post_id = get_latest_post()
    subject = "📢 פוסט חדש בקבוצת פואד"
    body = f"{text}\n{link}"
    send_email(subject, body)

if __name__ == "__main__":
    main()
