import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "my_secure_verify_token")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "EAAXZBBaT3600BS8fEd7eZCVck060GE7tDGc7KgC2fsk5EBiwIcLZCVFYLEbZBXGZC0QRZCsM6gZC6IUjvPZCVZCyZB6RLHmRZA5Rtv9WIbrHx1fxjuCPU9Mw0GeC49uT5Ve8AOQjWZBMOwZAYvbBq3dAEKA1yCNiAaPccEUHEIDmfuDihxPv8otIFZA1wSVpiuLmUG8h1lxbjkAXBnYYMOg2fUDT5GXuqqURviM60dkWgXDn1E5hcmGHwZCjkqrz9cJ0RYhcxZB6wtAdlqXuZAGXzrjhfDizcdQa8mgZDZD")


@app.route("/webhook", methods=["GET"])
def verify_webhook():
  mode = request.args.get("hub.mode")
  token = request.args.get("hub.verify_token")
  challenge = request.args.get("hub.challenge")

  if mode and token:
    if mode == "subscribe" and token == VERIFY_TOKEN:
      print("WEBHOOK_VERIFIED")
      return challenge, 200
    else:
      return "Verification failed", 403
  return "Invalid request", 400


@app.route("/webhook", methods=["POST"])
def handle_webhook():
  data = request.json
  print("Webhook received:", data)

  try:
    if data.get("object") == "instagram":
      for entry in data.get("entry", []):
        for messaging_event in entry.get("changes", []):
          if messaging_event.get("field") == "comments":
            comment_data = messaging_event.get("value", {})
            text = comment_data.get("text", "").lower()
            from_user = comment_data.get("from", {}).get("id")

            # Yahan apna target keyword set karein (jaise "link" ya "deal")
            target_keyword = "link"

            if target_keyword in text and from_user:
              send_direct_message(from_user)

  except Exception as e:
    print(f"Error: {e}")

  return jsonify({"status": "success"}), 200


def send_direct_message(recipient_id):
  url = f"https://graph.facebook.com/v19.0/me/messages"
  payload = {
      "recipient": {"id": recipient_id},
      "message": {
          "text": (
              "Hey! Yeh lijiye aapka requested link: [Aapka Affiliate Link"
              " Yahan Dalein]"
          )
      },
      "access_token": EAAXZBBaT3600BS8fEd7eZCVck060GE7tDGc7KgC2fsk5EBiwIcLZCVFYLEbZBXGZC0QRZCsM6gZC6IUjvPZCVZCyZB6RLHmRZA5Rtv9WIbrHx1fxjuCPU9Mw0GeC49uT5Ve8AOQjWZBMOwZAYvbBq3dAEKA1yCNiAaPccEUHEIDmfuDihxPv8otIFZA1wSVpiuLmUG8h1lxbjkAXBnYYMOg2fUDT5GXuqqURviM60dkWgXDn1E5hcmGHwZCjkqrz9cJ0RYhcxZB6wtAdlqXuZAGXzrjhfDizcdQa8mgZDZD,
  }
  response = requests.post(url, json=payload)
  print("DM Response:", response.json())


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
