import discord
from discord.ext import commands
import asyncio
import os
import threading
from flask import Flask
from config import *
from utils.database import db
from utils.embeds import create_embed

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

app = Flask(__name__)

@bot.event
async def on_ready():
    print(f"🔥 {bot.user} is LIVE!")
    await db.init_db()
    bot.loop.create_task(status_rotation())
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands!")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

async def status_rotation():
    statuses = [
        discord.Game("Daviccino Daddy 🔥"),
        discord.Game("Kevin de Bruyne ⚽️"),
        discord.Game("Albert Fish vibes")
    ]
    while True:
        for status in statuses:
            await bot.change_presence(activity=status, status=discord.Status.dnd)
            await asyncio.sleep(15)

@app.route("/")
@app.route("/ping")
def status():
    return {"status": "Phantom Daviccino 🔥 ALIVE", "guilds": len(bot.guilds)}

def run_bot():
    asyncio.run(bot.start(DISCORD_TOKEN))

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)
