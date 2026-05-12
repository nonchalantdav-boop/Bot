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
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

DB_PATH = "phantom.db"
ALMIGHTY_ID = 864380109682900992  # Your User ID

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

# ====================== STATUS ======================
statuses = [
    "WITH YOUR MOM 👀", "Rizzing up servers", "Daviccino Daddy 🔥",
    "Phantom Daviccino 👑", "Serving Top 1% Energy", "Roasting souls for fun",
    "Collecting L's from you", "/help • Top Tier Bot"
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

async def get_coins(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT coins FROM economy WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0

async def add_coins(user_id: int, amount: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""INSERT INTO economy (user_id, coins) VALUES (?, ?) 
                           ON CONFLICT(user_id) DO UPDATE SET coins = coins + ?""", 
                         (user_id, amount, amount))
        await db.commit()

async def add_vip(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO vips (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def is_vip(user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM vips WHERE user_id = ?", (user_id,)) as cur:
            return await cur.fetchone() is not None

# ====================== LISTS ======================
roasts = [
    "You're the reason abortions exist.", "Even your mom fakes the moans.", 
    "Sperm donor's biggest regret.", "Your birth was a biological error.",
    "God's 'oops' moment.", "You peaked at fertilization."
]

eightball_responses = [
    "Yes, definitely.", "No way.", "Ask again later.", "Outlook good.",
    "Very doubtful.", "Signs point to yes.", "My sources say no.",
    "Yes, 100%."
]

ship_responses = ["Literally soulmates", "Power couple vibes", "Cute asf", "10/10 would ship again", "Perfect match"]

compliments = [
    "You're absolutely killing it! 🔥", "Your vibe is unmatched ✨",
    "Top 1% energy! 👑", "Rizz level: God tier 😎"
]

# ====================== UTILITY ======================
async def send_with_image(interaction: discord.Interaction, embed: discord.Embed, image_key: str = None):
    if image_key and IMAGE_PATHS.get(image_key):
        path = IMAGE_PATHS[image_key]
        if os.path.exists(path):
            try:
                file = discord.File(path, filename=os.path.basename(path))
                await interaction.response.send_message(embed=embed, file=file)
                return
            except:
                pass
    await interaction.response.send_message(embed=embed)

def is_owner(interaction: discord.Interaction):
    return interaction.user.id == ALMIGHTY_ID

# ========================= EVENTS =========================
@bot.event
async def on_ready():
    await init_db()
    print(f"✅ {bot.user} is fully online!")
    bot.loop.create_task(status_rotation())
    try:
        await tree.sync()
        print("✅ Slash commands synced successfully")
    except Exception as e:
        print(f"Sync warning: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        embed = discord.Embed(title="Phantom Daviccino 👑", description="Use `/help`", color=0xFF00FF)
        await message.reply(embed=embed)
    await bot.process_commands(message)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"⏳ Wait {error.retry_after:.1f}s", ephemeral=True)
    else:
        print(f"Error: {error}")
        try:
            await interaction.response.send_message("❌ Something went wrong!", ephemeral=True)
        except:
            pass

# ========================= COMMANDS =========================

@tree.command(name="help", description="Show all commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Phantom Daviccino — Top 1% Bot 👑", color=0xFF00FF)
    embed.add_field(name="💰 Economy", value="/daily /coins /gamble /leaderboard", inline=False)
    embed.add_field(name="🎮 Fun", value="/roast /ship /8ball /dice /rps", inline=False)
    embed.add_field(name="💕 Social", value="/hug /slap /compliment", inline=False)
    embed.add_field(name="👑 VIP", value="/vip /say /dm /mimic", inline=False)
    embed.add_field(name="🔨 Moderation", value="/ban /kick", inline=False)
    embed.set_footer(text="Made with 🔥 by Phantom Daviccino")
    await interaction.response.send_message(embed=embed)

# === FUN ===
@tree.command(name="roast", description="Savage roast someone")
@app_commands.describe(member="Who to roast")
async def roast(interaction: discord.Interaction, member: discord.Member):
    if member.id == ALMIGHTY_ID:
        embed = discord.Embed(title="☠️ PHANTOM ROAST", description=f"{member.mention} is **Almighty** — Untouchable.", color=0xFFD700)
        return await interaction.response.send_message(embed=embed)
    
    embed = discord.Embed(title="☠️ PHANTOM ROAST", 
                         description=f"{member.mention} {random.choice(roasts)}", 
                         color=0xFF0000)
    await interaction.response.send_message(embed=embed)

@tree.command(name="ship", description="Ship two people")
@app_commands.describe(user1="First person", user2="Second person")
async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
    if user1.id == user2.id:
        return await interaction.response.send_message("❌ Can't ship the same person!", ephemeral=True)
    
    perc = random.randint(0, 100)
    if perc >= 90:
        title, color, key = "💞 PERFECT MATCH!", 0xFF1493, "ship_perfect"
    elif perc >= 60:
        title, color, key = "❤️ Great Ship!", 0xFF69B4, "ship_cute"
    else:
        title, color, key = "💔 Tragic...", 0x8B0000, "ship_tragic"
    
    embed = discord.Embed(title=title, description=f"{user1.mention} ❤️ {user2.mention}", color=color)
    embed.add_field(name="Compatibility", value=f"**{perc}%** • {random.choice(ship_responses)}", inline=False)
    await send_with_image(interaction, embed, key)

@tree.command(name="8ball", description="Ask the magic 8ball")
@app_commands.describe(question="Your question")
async def eightball(interaction: discord.Interaction, question: str):
    embed = discord.Embed(title="🎱 Magic 8Ball", color=0x00FF00)
    embed.add_field(name="Question", value=question, inline=False)
    embed.add_field(name="Answer", value=random.choice(eightball_responses), inline=False)
    await send_with_image(interaction, embed, "eightball")

# === ECONOMY ===
@tree.command(name="daily", description="Claim daily coins")
async def daily(interaction: discord.Interaction):
    user_id = interaction.user.id
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT last_daily FROM economy WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
    
    if row and row[0]:
        last = datetime.fromisoformat(row[0])
        if datetime.now() - last < timedelta(days=1):
            return await interaction.response.send_message("⏳ You already claimed today!", ephemeral=False)
    
    reward = random.randint(150, 300)
    await add_coins(user_id, reward)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE economy SET last_daily = ? WHERE user_id = ?", 
                        (datetime.now().isoformat(), user_id))
        await db.commit()
    
    embed = discord.Embed(title="🎁 Daily Reward!", description=f"You received **+{reward}** coins!", color=0x00FF88)
    await send_with_image(interaction, embed, "daily")

@tree.command(name="coins", description="Check your balance")
async def coins(interaction: discord.Interaction):
    bal = await get_coins(interaction.user.id)
    embed = discord.Embed(title="💰 Your Wallet", description=f"**{bal:,}** coins", color=0xFFD700)
    await send_with_image(interaction, embed, "coins")

@tree.command(name="gamble", description="Gamble your coins")
@app_commands.describe(amount="Amount to gamble (1-5000)")
async def gamble(interaction: discord.Interaction, amount: int):
    if not 1 <= amount <= 5000:
        return await interaction.response.send_message("❌ Bet between 1-5000 coins!", ephemeral=True)
    
    bal = await get_coins(interaction.user.id)
    if amount > bal:
        return await interaction.response.send_message("❌ Not enough coins!", ephemeral=True)
    
    if random.random() < 0.5:  # Win
        win = amount * random.randint(15, 25) // 10
        await add_coins(interaction.user.id, win - amount)
        embed = discord.Embed(title="🎉 JACKPOT!", 
                             description=f"You won **{win-amount}** coins!", color=0xFFEB3B)
        await send_with_image(interaction, embed, "gamble_win")
    else:
        await add_coins(interaction.user.id, -amount)
        embed = discord.Embed(title="💸 You Lost!", 
                             description=f"You lost **{amount}** coins.", color=0xFF5722)
        await send_with_image(interaction, embed, "gamble_lose")

@tree.command(name="leaderboard", description="Top 10 richest players")
async def leaderboard(interaction: discord.Interaction):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id, coins FROM economy ORDER BY coins DESC LIMIT 10") as cur:
            rows = await cur.fetchall()
    
    embed = discord.Embed(title="🏆 Phantom Leaderboard", color=0xFFD700)
    for i, (uid, coins) in enumerate(rows, 1):
        member = interaction.guild.get_member(uid)
        name = member.display_name if member else f"ID: {uid}"
        embed.add_field(name=f"#{i}", value=f"{name} — **{coins:,}** coins", inline=False)
    await send_with_image(interaction, embed, "leaderboard")

# === SOCIAL ===
@tree.command(name="hug", description="Hug someone")
@app_commands.describe(member="Who to hug")
async def hug(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(description=f"{interaction.user.mention} hugged {member.mention} 🥰", color=0xFF69B4)
    await send_with_image(interaction, embed, "hug")

@tree.command(name="slap", description="Slap someone")
@app_commands.describe(member="Who to slap")
async def slap(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(description=f"{interaction.user.mention} slapped {member.mention} 💥", color=0xFF0000)
    await send_with_image(interaction, embed, "slap")

@tree.command(name="compliment", description="Get a random compliment")
async def compliment(interaction: discord.Interaction):
    embed = discord.Embed(title="💖 Compliment", 
                         description=f"{interaction.user.mention} {random.choice(compliments)}", 
                         color=0xFF1493)
    await send_with_image(interaction, embed, "compliment")

# === GAME ===
@tree.command(name="dice", description="Roll a dice")
async def dice(interaction: discord.Interaction):
    roll = random.randint(1, 6)
    embed = discord.Embed(title="🎲 Dice Roll", 
                         description=f"**{interaction.user.display_name}** rolled **{roll}**!", 
                         color=0xFF8C00)
    await send_with_image(interaction, embed, "dice")

@tree.command(name="rps", description="Rock Paper Scissors")
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
    embed.add_field(name="You", value=choice.title(), inline=True)
    embed.add_field(name="Bot", value=bot_choice.title(), inline=True)
    embed.add_field(name="Result", value=result, inline=False)
    await send_with_image(interaction, embed, "rps")

# === VIP COMMANDS ===
@tree.command(name="vip", description="Give VIP (Owner Only)")
@app_commands.describe(member="Member to give VIP")
async def vip(interaction: discord.Interaction, member: discord.Member):
    if not is_owner(interaction):
        return await interaction.response.send_message("❌ Owner only!", ephemeral=True)
    await add_vip(member.id)
    embed = discord.Embed(title="👑 VIP Granted", description=f"{member.mention} is now VIP!", color=0xFFD700)
    await send_with_image(interaction, embed, "vip")

@tree.command(name="say", description="Make bot say something (VIP)")
@app_commands.describe(message="Message")
async def say(interaction: discord.Interaction, message: str):
    if not await is_vip(interaction.user.id) and not is_owner(interaction):
        return await interaction.response.send_message("❌ VIP Only!", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(message)

@tree.command(name="dm", description="DM someone (VIP)")
@app_commands.describe(member="Target", message="Message")
async def dm(interaction: discord.Interaction, member: discord.Member, message: str):
    if not await is_vip(interaction.user.id) and not is_owner(interaction):
        return await interaction.response.send_message("❌ VIP Only!", ephemeral=True)
    try:
        await member.send(f"{message}\n\n- Sent via Phantom Daviccino")
        await interaction.response.send_message(f"✅ DM sent to {member.mention}", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Failed to send DM (User has DMs closed)", ephemeral=True)

@tree.command(name="mimic", description="Mimic a user (VIP)")
@app_commands.describe(member="User to mimic", message="Message")
async def mimic(interaction: discord.Interaction, member: discord.Member, message: str):
    if not await is_vip(interaction.user.id) and not is_owner(interaction):
        return await interaction.response.send_message("❌ VIP Only!", ephemeral=True)
    
    await interaction.response.defer(ephemeral=True)
    webhooks = await interaction.channel.webhooks()
    webhook = discord.utils.get(webhooks, name="Phantom Mimic")
    if not webhook:
        webhook = await interaction.channel.create_webhook(name="Phantom Mimic")
    
    await webhook.send(content=message, username=member.display_name, avatar_url=member.display_avatar.url)

# === MODERATION ===
@tree.command(name="ban", description="Ban a member")
@app_commands.describe(member="Member to ban", reason="Reason")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.ban_members:
        return await interaction.response.send_message("❌ You need Ban Members permission!", ephemeral=True)
    await member.ban(reason=reason)
    embed = discord.Embed(title="🔨 Member Banned", description=f"{member.mention} was banned.\nReason: {reason}", color=0xFF0000)
    await send_with_image(interaction, embed, "ban")

@tree.command(name="kick", description="Kick a member")
@app_commands.describe(member="Member to kick", reason="Reason")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.kick_members:
        return await interaction.response.send_message("❌ You need Kick Members permission!", ephemeral=True)
    await member.kick(reason=reason)
    embed = discord.Embed(title="👢 Member Kicked", description=f"{member.mention} was kicked.\nReason: {reason}", color=0xFF4500)
    await send_with_image(interaction, embed, "kick")

# ========================= RUN =========================
if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        print("❌ ERROR: TOKEN environment variable not set!")
        print("Add TOKEN in Render Dashboard → Environment Variables")
        exit(1)

    def run_flask():
        port = int(os.environ.get("PORT", 8080))
        app.run(host="0.0.0.0", port=port, debug=False)

    threading.Thread(target=run_flask, daemon=True).start()
    
    print("🚀 Starting Phantom Daviccino...")
    bot.run(TOKEN)
