import os
from dotenv import load_dotenv
load_dotenv()

OWNER_ID = 864380109682900992
GF_ID = 1425090711019192434
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PORT = int(os.getenv("PORT", 10000))
