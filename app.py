from flask import Flask, request
import requests, os
from datetime import datetime, timedelta

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

@app.route('/')
def home():
    return "Bot is Live! Approve is OFF"

@app.route('/paystack-webhook', methods=['POST'])
def webhook():
    data = request.json
    if data.get('event') == 'charge.success':
        email = data['data']['customer']['email']
        
        # Create 1-use instant link (Approve OFF)
        expire = int((datetime.now() + timedelta(hours=1)).timestamp())
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/createChatInviteLink"
        payload = {
            "chat_id": CHANNEL_ID,
            "member_limit": 1,
            "expire_date": expire,
            "creates_join_request": False
        }
        res = requests.post(url, json=payload).json()
        print(f"Payment {email}: {res}")
        return "ok", 200
    return "ok", 200

if __name__ == '__main__':
    app.run()
