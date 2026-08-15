import os
import sys
import json
import urllib.request

def send_discord_notification(webhook_url, message):
    if not webhook_url:
        print("No DISCORD_WEBHOOK_URL set. Skipping Discord notification.")
        return
    payload = {
        "username": "idktheflag Bot",
        "avatar_url": "https://idktheflag.sh/branding/idktheflag-blank.png",
        "content": message
    }
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(webhook_url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            print("Discord notification sent successfully.")
    except Exception as err:
        print(f"Failed to send Discord notification: {err}")

if __name__ == '__main__':
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    msg = sys.argv[1] if len(sys.argv) > 1 else "🚩 idktheflag CTF stats updated on idktheflag.sh!"
    send_discord_notification(webhook_url, msg)
