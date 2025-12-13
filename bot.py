from flask import Flask, request
import requests
import json

BOT_TOKEN = "8513005164:AAHSB3MEuhcWAZSESON3gc8JfIYgY_dCDIk"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()

    # Sirf channel post handle kare
    if "channel_post" not in update:
        return "ok"

    chat_id = update["channel_post"]["chat"]["id"]
    message_id = update["channel_post"]["message_id"]

    # tumhara reaction url
    reaction_url = f"https://reaction.xo.je/reaction.php?chat_id={chat_id}&msg_id={message_id}"

    try:
        requests.get(reaction_url, timeout=5)
    except:
        pass

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
