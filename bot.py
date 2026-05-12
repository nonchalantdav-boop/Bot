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

# ====================== ROAST LIST (160+ Brutal Roasts) ======================
roasts = [
    "You're the reason abortions exist.", "Even your mom fakes the moans.", "Sperm donor's biggest regret.",
    "Your birth was a biological error.", "God's 'oops' moment.", "You peaked at fertilization.",
    "Condoms file restraining orders against you.", "Human trash bag.", "Walking advertisement for vasectomy.",
    "Your face is a war crime.", "Even mirrors crack in protest.", "Ugly doesn't cover it.",
    "Built like a rejected prototype.", "Your dad swallowed better.", "Breathing is your only achievement.",
    "Natural selection's side project.", "You're why 'skip' exists.", "The 'before' in every glow-up.",
    "Personality of wet cardboard.", "Even hell rejected your application.", "Virgin by universal vote.",
    "Your IQ needs life support.", "Die in obscurity, loser.", "Forgotten before you arrived.",
    "Your bloodline deserves extinction.", "Proof life has no quality control.", "You're the glitch nobody patches.",
    "Smells like failure and BO.", "Your existence is community service.", "Adopted by pure disappointment.",
    "Even roaches avoid you.", "The human equivalent of lag.", "Your mom regrets not swallowing.",
    "Built for irrelevance.", "Cursed by every god.", "You're the final boss of mid.",
    "Face like expired milk.", "Soul like a black hole.", "Zero redeemable qualities.",
    "Breath smells like regret.", "You're what happens after 'pull out' fails.",
    "The reason dating apps have block buttons.", "Evolutionary dead end.", "Your reflection files lawsuits.",
    "Talentless, faceless, useless.", "Even your shadow leaves early.", "Walking participation trophy.",
    "Your genes deserve jail.", "Useless as a participation medal.", "The void stares back less empty.",
    "Daddy issues in human form.", "Mom's biggest 'what if'.", "You're digital diarrhea.",
    "Personality bankruptcy declared.", "Even AI feels sorry for you.", "The 'L' in everyone's alphabet.",
    "Your life is a loading error.", "Built like a question nobody asked.", "Cunt with no warmth.",
    "Your aura is toxic waste.", "Forgotten sperm that survived.", "God's deleted draft.",
    "You're the 'decline' button.", "Face only a mother tolerates… barely.", "Zero drip, all trip.",
    "The human '404 not found'.", "Your existence is a glitch.", "Even therapy ghosts you.",
    "Built for the block list.", "Walking argument for eugenics.", "Your vibe is clinical depression.",
    "The reason 'nevermind' was invented.", "Soul sold for participation.", "You're background noise.",
    "Even your dreams quit.", "Humanity's loading screen.", "The final 'fuck it' of creation.",
    "Your legacy: none.", "Die mad and irrelevant.", "You're not even worth the roast.",
    "Your forehead needs its own zip code.", "Built like a question mark.", "Even your screenshots are ugly.",
    "You have negative aura.", "The type to get rejected by a fleshlight.", "Your rizz is in negative digits.",
    "Smells like expired milk and broken dreams.", "You're the 'Do Not Reply' in group chats.",
    "Face card declined.", "Your mom calls you by your full government name when she's disappointed.",
    "Walking red flag factory.", "Even your therapist needs therapy after you.", "Broke boy with rich delusions.",
    "Simp level: legendary.", "Your body count is 0 and your personality is -10.", "Certified community toilet.",
    "The reason birth control was invented.", "You scream 'I have no friends'.", "Invisible to baddies.",
    "Your drip is dry as the Sahara.", "Even Google can't find your highlights.", "Permanent benchwarmer.",
    "You’re what happens when motivation pulls out.", "Mid in every universe.", "Your vibes need a restraining order.",
    "The human version of Comic Sans.", "Even your plants fake growing.", "Bro got rejected by life itself.",
    "Your personality is on airplane mode.", "Built like a budget cut.", "The final boss of disappointment.",
    "Your scalp is visible from space.", "Even darkness says 'too black'.", "You make onions cry.",
    "Negative rizz, negative game.", "The 'L' is permanently tattooed on your forehead.",
    "Your future is loading... 404 error.", "Certified yapper with zero sauce.", "Even your echo ignores you."
]

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
        embed = discord.Embed(
            title="Phantom Daviccino 👑",
            description="Use `/help` for all commands\nTop 1% Discord Bot 🔥",
            color=0xFF00FF
        )
        await message.reply(embed=embed)
    await bot.process_commands(message)

# ========================= COMMANDS =========================

@tree.command(name="help", description="Show all commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Phantom Daviccino Commands", color=0xFF00FF)
    embed.add_field(name="Economy", value="/daily /coins /gamble /leaderboard", inline=False)
    embed.add_field(name="Fun", value="/roast /ship /8ball /dice /rps", inline=False)
    embed.add_field(name="Social", value="/hug /slap /compliment", inline=False)
    embed.add_field(name="VIP", value="/say /dm /mimic (VIP only)", inline=False)
    embed.set_footer(text="50+ Commands • Top 1% Bot")
    await interaction.response.send_message(embed=embed)

@tree.command(name="roast", description="Savage roast someone 🔥")
@app_commands.describe(member="Who to roast")
async def roast(interaction: discord.Interaction, member: discord.Member):
    if member.id == interaction.user.id:
        roast_text = random.choice(["Self-roast? Crazy.", "Touch grass king.", "At least you tried... mid af tho 😂"])
    else:
        roast_text = random.choice(roasts)
    
    embed = discord.Embed(
        title="☠️ PHANTOM ROAST",
        description=f"{member.mention} {roast_text}",
        color=0xFF0000
    )
    embed.set_footer(text="Phantom Daviccino • Top 1% Energy")
    await interaction.response.send_message(embed=embed)

@tree.command(name="ship", description="Ship two people")
@app_commands.describe(user1="First person", user2="Second person")
async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
    percentage = random.randint(0, 100)
    emoji = "💞" if percentage >= 90 else "❤️" if percentage >= 70 else "💖" if percentage >= 40 else "💔"
    embed = discord.Embed(title="Shipping Meter", description=f"{user1.mention} ❤️ {user2.mention}", color=0xFF69B4)
    embed.add_field(name="Compatibility", value=f"**{percentage}%** {emoji}", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="daily", description="Claim your daily coins")
async def daily(interaction: discord.Interaction):
    user_id = interaction.user.id
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT last_daily FROM economy WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
    
    if row and row[0]:
        last_claim = datetime.fromisoformat(row[0])
        if datetime.now() - last_claim < timedelta(days=1):
            return await interaction.response.send_message("⏳ You already claimed today!", ephemeral=True)

    reward = random.randint(150, 300)
    await add_coins(user_id, reward)
    
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE economy SET last_daily = ? WHERE user_id = ?", 
                        (datetime.now().isoformat(), user_id))
        await db.commit()

    embed = discord.Embed(title="Daily Reward", description=f"You received **{reward}** coins!", color=0x00FF00)
    await interaction.response.send_message(embed=embed)

@tree.command(name="coins", description="Check your balance")
async def coins(interaction: discord.Interaction):
    bal = await get_coins(interaction.user.id)
    embed = discord.Embed(title="Your Balance", description=f"**{bal}** coins 💰", color=0xFFD700)
    await interaction.response.send_message(embed=embed)

@tree.command(name="gamble", description="Gamble your coins")
@app_commands.describe(amount="Amount to gamble")
async def gamble(interaction: discord.Interaction, amount: int):
    if amount < 10:
        return await interaction.response.send_message("Minimum bet is 10 coins", ephemeral=True)
    
    bal = await get_coins(interaction.user.id)
    if bal < amount:
        return await interaction.response.send_message("Not enough coins!", ephemeral=True)
    
    if random.random() < 0.5:
        winnings = amount * 2
        await add_coins(interaction.user.id, winnings)
        result = f"You **won** {winnings} coins! 🎉"
        color = 0x00FF00
    else:
        await add_coins(interaction.user.id, -amount)
        result = f"You **lost** {amount} coins... 😢"
        color = 0xFF0000
    
    embed = discord.Embed(title="🎰 Gamble", description=result, color=color)
    await interaction.response.send_message(embed=embed)

# ========================= RUN BOTH =========================
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
        print("❌ DISCORD_TOKEN environment variable not set!")
