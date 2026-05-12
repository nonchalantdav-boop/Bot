from flask import Flask
import os
import random
import requests
import asyncio

app = Flask(__name__)

roasts = ["Mid af 😂", "Rizz = 0 💀", "Cope harder"]

@app.route("/")
def home():
    return "Phantom Daviccino 🔥 ALIVE"

@app.route("/roast")
def roast():
    return {"roast": random.choice(roasts)}

@app.route("/ping")
def ping():
    return {"status": "alive"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
