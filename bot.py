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

# ========================= FLASK KEEP ALIVE =========================
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
intents.moderation = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

DB_PATH = "phantom.db"
ALMIGHTY_ID = 864380109682900992  # Your ID

# ====================== IMAGE PATHS =========================
IMAGE_PATHS = {
    "ship_perfect": "images/ship_perfect.gif",
    "ship_cute": "images/ship_cute.gif", 
    "ship_tragic": "images/ship_tragic.gif",
    "eightball": "images/eightball.gif",
    "coins": "images/coins.png",
    "daily": "images/daily.gif",
    "gamble_win": "images/gamble_win.gif",
    "gamble_lose": "images/gamble_lose.gif",
    "leaderboard": "images/leaderboard.png",
    "hug": "images/hug.gif",
    "slap": "images/slap.gif",
    "compliment": "images/compliment.gif",
    "dice": "images/dice.gif",
    "rps": "images/rps.gif",
    "vip": "images/vip.png",
    "ban": "images/ban.gif",
    "kick": "images/kick.gif"
}

# ====================== STATUS ROTATION ======================
statuses = [
    "WITH YOUR MOM 👀", "Rizzing up servers", "Daviccino Daddy 🔥",
    "Phantom Daviccino 👑", "Serving Top 1% Energy", "Roasting souls for fun",
    "Collecting L's from you", "Making servers dangerous 😈", "/help • Top Tier Bot"
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
        await db.execute("""CREATE TABLE IF NOT EXISTS economy 
                           (user_id INTEGER PRIMARY KEY, coins INTEGER DEFAULT 0, last_daily TEXT)""")
        await db.execute("""CREATE TABLE IF NOT EXISTS vips (user_id INTEGER PRIMARY KEY)""")
        await db.commit()

# ====================== UTILITY ======================
async def send_with_image(interaction, embed, image_key):
    image_path = IMAGE_PATHS.get(image_key)
    if image_path and os.path.exists(image_path):
        try:
            file = discord.File(image_path, filename=os.path.basename(image_path))
            await interaction.response.send_message(embed=embed, file=file)
            return
        except:
            pass
    await interaction.response.send_message(embed=embed)

def is_owner(interaction: discord.Interaction):
    return interaction.user.id == ALMIGHTY_ID

# ====================== VIP CHECK ======================
async def is_vip(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM vips WHERE user_id = ?", (user_id,)) as cur:
            return await cur.fetchone() is not None

# ========================= EVENTS =========================
@bot.event
async def on_ready():
    await init_db()
    print(f"✅ {bot.user} is fully online!")
    bot.loop.create_task(status_rotation())
    try:
        await tree.sync()
        print("✅ All slash commands synced")
    except Exception as e:
        print(f"Sync error: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        embed = discord.Embed(title="Phantom Daviccino 👑", description="Use `/help`", color=0xFF00FF)
        await message.reply(embed=embed)
    await bot.process_commands(message)

# ========================= VIP COMMANDS =========================
@tree.command(name="vip", description="Add VIP (Owner only)")
@app_commands.describe(member="Member to give VIP")
async def vip(interaction: discord.Interaction, member: discord.Member):
    if not is_owner(interaction):
        return await interaction.response.send_message("❌ Owner only command.", ephemeral=True)
    
    await add_vip(member.id)
    embed = discord.Embed(title="👑 VIP Granted", 
                         description=f"{member.mention} is now a VIP!", 
                         color=0xFFD700)
    await send_with_image(interaction, embed, "vip")

@tree.command(name="say", description="Make the bot say something (VIP only)")
@app_commands.describe(message="Message to say")
async def say(interaction: discord.Interaction, message: str):
    if not await is_vip(interaction.user.id) and not is_owner(interaction):
        return await interaction.response.send_message("❌ VIP only!", ephemeral=True)
    
    await interaction.response.defer()
    await interaction.channel.send(message)

@tree.command(name="dm", description="DM a user (VIP only)")
@app_commands.describe(member="User to DM", message="Message to send")
async def dm(interaction: discord.Interaction, member: discord.Member, message: str):
    if not await is_vip(interaction.user.id) and not is_owner(interaction):
        return await interaction.response.send_message("❌ VIP only!", ephemeral=True)
    
    try:
        await member.send(f"{message}\n\n- Sent by {interaction.user} via Phantom Daviccino")
        await interaction.response.send_message(f"✅ DM sent to {member.mention}", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Could not DM the user (DMs closed).", ephemeral=True)

@tree.command(name="mimic", description="Mimic someone's messages (VIP only)")
@app_commands.describe(member="User to mimic", message="Message to mimic")
async def mimic(interaction: discord.Interaction, member: discord.Member, message: str):
    if not await is_vip(interaction.user.id) and not is_owner(interaction):
        return await interaction.response.send_message("❌ VIP only!", ephemeral=True)
    
    webhook = None
    async for w in interaction.channel.webhooks():
        if w.name == "Phantom Mimic":
            webhook = w
            break
    
    if not webhook:
        webhook = await interaction.channel.create_webhook(name="Phantom Mimic")
    
    await interaction.response.defer(ephemeral=True)
    await webhook.send(
        content=message,
        username=member.display_name,
        avatar_url=member.display_avatar.url
    )

# ====================== ROAST LIST (unchanged) ======================
roasts = [ ... ]  # Keep your list
eightball_responses = [ ... ]
ship_responses = [ ... ]
compliments = [ ... ]

# Keep all your existing commands (roast, ship, 8ball, daily, coins, gamble, leaderboard, hug, slap, compliment, dice, rps)

# ========================= RUN BOT =========================
if __name__ == "__main__":
    # Run Flask in a separate thread
    def run_flask():
        port = int(os.environ.get("PORT", 8080))
        app.run(host="0.0.0.0", port=port)

    threading.Thread(target=run_flask, daemon=True).start()
    
    # Run Discord bot
    bot.run(os.getenv("TOKEN"))  # Put your token in environment variables
