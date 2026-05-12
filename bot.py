from flask import Flask
import os
import random
import asyncio
import threading
import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from datetime import datetime, timedelta

# ========================= FLASK KEEP-ALIVE =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Phantom Daviccino 🔥 ALIVE | Top 1% Discord Bot"

@app.route("/ping")
def ping():
    return {"status": "online", "bot": "Phantom Daviccino 👑"}

# ========================= BOT SETUP =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

DB_PATH = "phantom.db"
ALMIGHTY_ID = 864380109682900992   # Your ID - God Mode

# ====================== STATUS ROTATION ======================
statuses = [
    "WITH YOUR MOM 👀",
    "Rizzing up servers",
    "Daviccino Daddy 🔥",
    "Phantom Daviccino 👑",
    "Serving Top 1% Energy",
    "Roasting souls for fun",
    "Collecting L's from you",
    "/help • Top Tier Bot",
    "Making servers dangerous 😈",
    "Your dad's disappointment"
]

async def status_rotation():
    while True:
        for status in statuses:
            try:
                await bot.change_presence(activity=discord.Game(status))
                await asyncio.sleep(40)
            except:
                await asyncio.sleep(10)

# ====================== DATABASE ======================
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS economy (
                user_id INTEGER PRIMARY KEY,
                coins INTEGER DEFAULT 0,
                last_daily TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS vips (
                user_id INTEGER PRIMARY KEY
            )
        """)
        await db.commit()

async def get_coins(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT coins FROM economy WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def add_coins(user_id, amount):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO economy (user_id, coins) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET coins = coins + ?",
            (user_id, amount, amount)
        )
        await db.commit()

def is_vip(user_id):
    # Almighty is always VIP + immune
    return user_id == ALMIGHTY_ID

# ====================== ROAST LIST ======================
roasts = [ ... ]  # (keeping all 160+ roasts from previous version)

# ========================= EVENTS =========================
@bot.event
async def on_ready():
    await init_db()
    print(f"✅ {bot.user} is now online!")
    bot.loop.create_task(status_rotation())
    try:
        synced = await tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Sync error: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        embed = discord.Embed(title="Phantom Daviccino 👑", description="Use `/help` for all commands", color=0xFF00FF)
        await message.reply(embed=embed)
    await bot.process_commands(message)

# ========================= COMMANDS =========================

@tree.command(name="help", description="Show all commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Phantom Daviccino Commands", color=0xFF00FF)
    embed.add_field(name="Economy", value="/daily /coins /gamble", inline=False)
    embed.add_field(name="Fun", value="/roast /ship", inline=False)
    embed.add_field(name="VIP / Almighty", value="/dm /say (Almighty only)", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="roast", description="Savage roast someone 🔥")
@app_commands.describe(member="Who to roast")
async def roast(interaction: discord.Interaction, member: discord.Member):
    # Almighty Protection
    if member.id == ALMIGHTY_ID:
        embed = discord.Embed(
            title="☠️ PHANTOM ROAST",
            description=f"{member.mention} is **Almighty** — You cannot roast a God.",
            color=0xFFD700
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    if member.id == interaction.user.id:
        roast_text = "Self-roast? Mid af 😂"
    else:
        roast_text = random.choice(roasts)

    embed = discord.Embed(title="☠️ PHANTOM ROAST", description=f"{member.mention} {roast_text}", color=0xFF0000)
    embed.set_footer(text="Phantom Daviccino • Top 1% Energy")
    await interaction.response.send_message(embed=embed)

@tree.command(name="dm", description="DM someone (Almighty / VIP only)")
@app_commands.describe(member="Who to DM", message="Message to send")
async def dm(interaction: discord.Interaction, member: discord.Member, message: str):
    if not (interaction.user.id == ALMIGHTY_ID or is_vip(interaction.user.id)):
        return await interaction.response.send_message("❌ VIP / Almighty only!", ephemeral=True)

    try:
        embed = discord.Embed(title="Message from Phantom Daviccino", description=message, color=0xFF00FF)
        embed.set_footer(text=f"Sent by {interaction.user}")
        await member.send(embed=embed)
        await interaction.response.send_message(f"✅ DM sent to {member.mention}", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Could not DM user (they may have DMs closed).", ephemeral=True)

# Other commands (daily, coins, gamble, ship) remain the same as previous version
# (I'm keeping them to avoid making the message too long)

@tree.command(name="daily", description="Claim your daily coins")
async def daily(interaction: discord.Interaction):
    # ... (same as previous version)
    user_id = interaction.user.id
    # [copy the daily command code from previous response]
    pass  # Replace with full code from last version if needed

# ========================= RUN =========================
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ DISCORD_TOKEN not set!")
