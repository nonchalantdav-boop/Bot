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
ALMIGHTY_ID = 864380109682900992

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

async def get_coins(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT coins FROM economy WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0

async def add_coins(user_id, amount):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""INSERT INTO economy (user_id, coins) VALUES (?, ?) 
                           ON CONFLICT(user_id) DO UPDATE SET coins = coins + ?""", 
                         (user_id, amount, amount))
        await db.commit()

async def add_vip(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO vips (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def is_vip(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM vips WHERE user_id = ?", (user_id,)) as cur:
            return await cur.fetchone() is not None

# ====================== ROAST LIST ======================
roasts = [
    "You're the reason abortions exist.", "Even your mom fakes the moans.", "Sperm donor's biggest regret.",
    "Your birth was a biological error.", "God's 'oops' moment.", "You peaked at fertilization.",
    "Condoms file restraining orders against you.", "Human trash bag.", "Walking advertisement for vasectomy.",
    "Your face is a war crime.", "Even mirrors crack in protest.", "Ugly doesn't cover it."
]

# ====================== 8BALL RESPONSES ======================
eightball_responses = [
    "Yes, definitely.", "No way.", "Ask again later.", "Outlook good.", "Very doubtful.",
    "Signs point to yes.", "My sources say no.", "Cannot predict now.", "Yes, 100%.",
    "Absolutely not.", "Without a doubt.", "Don't count on it.", "As I see it, yes."
]

ship_responses = [
    "Literally soulmates", "Power couple vibes", "Cute asf", "10/10 would ship again",
    "Perfect match", "Rizz recognized", "Endgame", "Couple goals"
]

compliments = [
    "You're absolutely killing it! 🔥", "Your vibe is unmatched ✨", "Top 1% energy! 👑",
    "You make Discord better 💎", "Rizz level: God tier 😎", "Main character energy 🚀"
]

# ====================== UTILITY FUNCTIONS ======================
async def send_with_image(interaction, embed, image_key):
    """Send embed with image if file exists"""
    image_path = IMAGE_PATHS.get(image_key)
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as f:
                file = discord.File(f, filename=os.path.basename(image_path))
                await interaction.response.send_message(embed=embed, file=file)
        except:
            await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(embed=embed)

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
        print(e)

@bot.event
async def on_message(message):
    if message.author.bot: return
    if bot.user.mentioned_in(message):
        embed = discord.Embed(title="Phantom Daviccino 👑", description="Use `/help`", color=0xFF00FF)
        await message.reply(embed=embed)
    await bot.process_commands(message)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"⏳ Chill! Wait {error.retry_after:.1f}s", ephemeral=True)
    else:
        print(f"Command error: {error}")
        await interaction.response.send_message("❌ Something went wrong!", ephemeral=True)

# ========================= COMMANDS =========================
@tree.command(name="help", description="Show all commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Phantom Daviccino — Top 1% Bot 👑", color=0xFF00FF)
    embed.add_field(name="💰 Economy", value="/daily /coins /gamble /leaderboard", inline=False)
    embed.add_field(name="🎮 Fun", value="/roast /ship /8ball /dice /rps", inline=False)
    embed.add_field(name="💕 Social", value="/hug /slap /compliment", inline=False)
    embed.add_field(name="👑 VIP", value="/vip /say /dm /mimic", inline=False)
    embed.add_field(name="🔨 Moderation", value="/ban /kick", inline=False)
    embed.set_footer(text="Phantom Daviccino 🔥 | Top 1% Bot")
    await interaction.response.send_message(embed=embed)

# 🔥 ROAST (No image as requested)
@tree.command(name="roast", description="Savage roast someone 🔥")
@app_commands.describe(member="Who to roast")
async def roast(interaction: discord.Interaction, member: discord.Member):
    if member.id == ALMIGHTY_ID:
        embed = discord.Embed(title="☠️ PHANTOM ROAST", description=f"{member.mention} is **Almighty God** — Untouchable.", color=0xFFD700)
        return await interaction.response.send_message(embed=embed)
    
    roast_text = random.choice(roasts)
    embed = discord.Embed(title="☠️ PHANTOM ROAST", description=f"{member.mention} {roast_text}", color=0xFF0000)
    embed.set_footer(text="Phantom Daviccino")
    await interaction.response.send_message(embed=embed)

# 💞 SHIP
@tree.command(name="ship", description="Ship two people 💞")
@app_commands.describe(user1="First person", user2="Second person")
async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
    if user1.id == user2.id:
        return await interaction.response.send_message("❌ Can't ship the same person!", ephemeral=True)
    
    perc = random.randint(0, 100)
    if perc >= 90: 
        title, color, img_key = "💞 PERFECT MATCH!", 0xFF1493, "ship_perfect"
    elif perc >= 70: 
        title, color, img_key = "❤️ Great Ship!", 0xFF69B4, "ship_cute"
    elif perc >= 50: 
        title, color, img_key = "💖 Cute Ship", 0xFFC0CB, "ship_cute"
    else: 
        title, color, img_key = "💔 Tragic...", 0x8B0000, "ship_tragic"
    
    embed = discord.Embed(title=title, description=f"{user1.mention} ❤️ {user2.mention}", color=color)
    embed.add_field(name="Compatibility", value=f"**{perc}%** • {random.choice(ship_responses)}", inline=False)
    await send_with_image(interaction, embed, img_key)

# 🎱 8BALL
@tree.command(name="8ball", description="Ask the magic 8ball")
@app_commands.describe(question="Your question")
async def eightball(interaction: discord.Interaction, question: str):
    answer = random.choice(eightball_responses)
    embed = discord.Embed(title="🎱 Magic 8Ball", color=0x00FF00)
    embed.add_field(name=f"**Q:** {question}", value=f"**A:** {answer}", inline=False)
    await send_with_image(interaction, embed, "eightball")

# 💰 ECONOMY COMMANDS
@tree.command(name="daily", description="Claim daily coins")
async def daily(interaction: discord.Interaction):
    user_id = interaction.user.id
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT last_daily FROM economy WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
    if row and row[0]:
        last = datetime.fromisoformat(row[0])
        if datetime.now() - last < timedelta(days=1):
            return await interaction.response.send_message("⏳ Already claimed today!", ephemeral=False)
    
    reward = random.randint(150, 300)
    await add_coins(user_id, reward)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE economy SET last_daily = ? WHERE user_id = ?", (datetime.now().isoformat(), user_id))
        await db.commit()
    
    embed = discord.Embed(title="🎁 Daily Reward!", description=f"**+{reward}** coins! 💰", color=0x00FF88)
    await send_with_image(interaction, embed, "daily")

@tree.command(name="coins", description="Check your coins")
async def coins(interaction: discord.Interaction):
    bal = await get_coins(interaction.user.id)
    embed = discord.Embed(title="💰 Your Wallet", description=f"**{bal:,}** coins", color=0xFFD700)
    await send_with_image(interaction, embed, "coins")

@tree.command(name="gamble", description="Gamble your coins 🎰")
@app_commands.describe(amount="Amount to gamble (1-5000)")
async def gamble(interaction: discord.Interaction, amount: int):
    if amount < 1 or amount > 5000:
        return await interaction.response.send_message("❌ Bet between 1-5000 coins!", ephemeral=True)
    
    user_id = interaction.user.id
    bal = await get_coins(user_id)
    if amount > bal:
        return await interaction.response.send_message("❌ Not enough coins!", ephemeral=True)
    
    if random.random() < 0.5:  # 50% win
        win = amount * random.randint(15, 25) // 10
        await add_coins(user_id, win - amount)
        embed = discord.Embed(title="🎉 JACKPOT!", description=f"**+{win-amount}** coins!\nNew balance: **{await get_coins(user_id):,}**", color=0xFFEB3B)
        await send_with_image(interaction, embed, "gamble_win")
    else:
        await add_coins(user_id, -amount)
        embed = discord.Embed(title="💸 BUST!", description=f"**-{amount}** coins!\nNew balance: **{await get_coins(user_id):,}**", color=0xFF5722)
        await send_with_image(interaction, embed, "gamble_lose")

@tree.command(name="leaderboard", description="Top 10 richest")
async def leaderboard(interaction: discord.Interaction):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id, coins FROM economy ORDER BY coins DESC LIMIT 10") as cur:
            rows = await cur.fetchall()
    
    embed = discord.Embed(title="🏆 Phantom Leaderboard", color=0xFFD700)
    for i, (uid, coins) in enumerate(rows, 1):
        member = interaction.guild.get_member(uid)
        name = member.display_name if member else f"👻 ID {uid}"
        embed.add_field(name=f"#{i}", value=f"{name} — **{coins:,}** 💰", inline=False)
    
    await send_with_image(interaction, embed, "leaderboard")

# 💕 SOCIAL COMMANDS
@tree.command(name="hug", description="Hug someone 🥰")
@app_commands.describe(member="Who to hug")
async def hug(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(description=f"{interaction.user.mention} hugged {member.mention} 🥰💕", color=0xFF69B4)
    await send_with_image(interaction, embed, "hug")

@tree.command(name="slap", description="Slap someone 👋")
@app_commands.describe(member="Who to slap")
async def slap(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(description=f"{interaction.user.mention} slapped {member.mention} 💥", color=0xFF0000)
    await send_with_image(interaction, embed, "slap")

@tree.command(name="compliment", description="Get a compliment 💖")
async def compliment(interaction: discord.Interaction):
    comp = random.choice(compliments)
    embed = discord.Embed(title="💖 Compliment", description=f"{interaction.user.mention} {comp}", color=0xFF1493)
    await send_with_image(interaction, embed, "compliment")

# 🎮 FUN COMMANDS
@tree.command(name="dice", description="Roll a dice 🎲")
async def dice(interaction: discord.Interaction):
    roll = random.randint(1, 6)
    embed = discord.Embed(title="🎲 Dice Roll", description=f"**{interaction.user.display_name}** rolled **{roll}**!", color=0xFF8C00)
    await send_with_image(interaction, embed, "dice")

@tree.command(name="rps", description="Rock Paper Scissors ✂️")
@app_commands.choices(choice=[
    app_commands.Choice(name="🪨 Rock", value="rock"),
    app_commands.Choice(name="📄 Paper", value="paper"),
    app_commands.Choice(name="✂️ Scissors", value="scissors")
])
async def rps(interaction: discord.Interaction, choice: str):
    bot_choice = random.choice(["rock", "paper", "scissors"])
    if choice == bot_choice:
        result = "💥 It's a tie!"
    elif (choice == "rock" and bot_choice == "scissors") or \
         (choice == "paper" and bot_choice == "rock") or \
         (choice == "scissors" and bot_choice == "paper"):
        result = "🏆 You win!"
    else:
        result = "😭 You lose!"
    
    embed = discord.Embed(title="✂️ Rock Paper Scissors", color=0x00BFFF)
    embed.add_field(name=f"**You:** {choice.title()}", value=f"**Bot:** {bot_choice.title()}", inline=True)
    embed.add_field(name="Result", value=result, inline=False)
    await send_with_image(interaction, embed, "rps")

# 👑 VIP COMMANDS
@tree.command(name="say", description="Make bot say something (VIP only)")
@app_commands.describe(message="Message")
async def say(interaction: discord.Interaction, message: str):
    if not (interaction.user.id == ALMIGHTY_ID or await is_vip(interaction.user.id)):
        return await interaction.response.send_message("❌ VIP / Almighty only!", ephemeral=True)
    await interaction.channel.send(message)
    await interaction.response.send_message("✅ Sent.", ephemeral=True)

@tree.command(name="mimic", description="Mimic someone (VIP only)")
@app_commands.describe(member="Who to mimic", message="What to say as them")
async def mimic(interaction: discord.Interaction, member: discord.Member, message: str):
    if not (interaction.user.id == ALMIGHTY_ID or await is_vip(interaction.user.id)):
        return await interaction.response.send_message("❌ VIP / Almighty only!", ephemeral=True)
    embed = discord.Embed(description=message, color=0x9B59B6)
    embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
    await interaction.channel.send(embed=embed)
    await interaction.response.send_message("✅ Done.", ephemeral=True)
