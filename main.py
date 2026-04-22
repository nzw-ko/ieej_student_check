import requests
import smtplib
from email.mime.text import MIMEText
import os
import time

# 設定
BASE_URL = "https://www.iee.jp/tokyo/202508{day}student/"
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASS = os.environ.get("GMAIL_PASS")
TO_EMAIL = os.environ.get("TO_EMAIL")

def send_email(found_urls):
    body = "以下のページが見つかりました：\n\n" + "\n".join(found_urls)
    msg = MIMEText(body)
    msg["Subject"] = "【通知】学会リンクが更新されました"
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)

def check_all_links():
    found_urls = []
    
    # 01から31までループ
    for i in range(1, 32):
        day = str(i).zfill(2) # 1 -> "01", 10 -> "10"
        url = BASE_URL.format(day=day)
        
        try:
            # 負荷を考え、各アクセスに少し間隔を置く
            time.sleep(0.5) 
            response = requests.head(url, allow_redirects=True, timeout=5)
            
            if response.status_code == 200:
                print(f"FOUND: {url}")
                found_urls.append(url)
            else:
                print(f"Not found ({day}): {response.status_code}")
                
        except Exception as e:
            print(f"Error checking {day}: {e}")

    # 見つかったURLがあればメール送信
    if found_urls:
        send_email(found_urls)

if __name__ == "__main__":
    check_all_links()
