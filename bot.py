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

def is_vip(user_id):
    return user_id == ALMIGHTY_ID

# ====================== ROAST LIST (160+) ======================
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
    "Face card declined.", "Walking red flag factory.", "Broke boy with rich delusions.",
    "Simp level: legendary.", "Your body count is 0 and your personality is -10.",
    "Certified community toilet.", "The reason birth control was invented.", "You scream 'I have no friends'.",
    "Invisible to baddies.", "Your drip is dry as the Sahara.", "Permanent benchwarmer.",
    "Mid in every universe.", "Your vibes need a restraining order.", "The human version of Comic Sans.",
    "Even your plants fake growing.", "Bro got rejected by life itself.", "Your personality is on airplane mode.",
    "Built like a budget cut.", "The final boss of disappointment.", "Your scalp is visible from space.",
    "Even darkness says 'too black'.", "You make onions cry.", "Negative rizz, negative game.",
    "The 'L' is permanently tattooed on your forehead.", "Your future is loading... 404 error."
]

# ====================== 8BALL RESPONSES (25+) ======================
eightball_responses = [
    "Yes, definitely.", "No way.", "Ask again later.", "Outlook good.", "Very doubtful.",
    "Signs point to yes.", "My sources say no.", "Cannot predict now.", "Yes, 100%.",
    "Absolutely not.", "Without a doubt.", "Don't count on it.", "As I see it, yes.",
    "Better not tell you now.", "Concentrate and ask again.", "Most likely.", 
    "My reply is no.", "You may rely on it.", "Reply hazy, try again.", "It is certain.",
    "It is decidedly so.", "Don't bet on it.", "Yes, but only on Tuesdays.", 
    "The stars say no.", "Hell yeah."
]

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

# ========================= COMMANDS =========================
@tree.command(name="help", description="Show all commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Phantom Daviccino — Top 1% Bot 👑", color=0xFF00FF)
    embed.add_field(name="Economy", value="/daily /coins /gamble /leaderboard", inline=False)
    embed.add_field(name="Fun", value="/roast /ship /8ball /dice /rps", inline=False)
    embed.add_field(name="Social", value="/hug /slap /compliment", inline=False)
    embed.add_field(name="VIP", value="/vip /say /dm /mimic", inline=False)
    embed.add_field(name="Moderation", value="/ban /kick /mute", inline=False)
    await interaction.response.send_message(embed=embed)

# ROAST (Visible)
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

# SHIP (with 20+ variations)
@tree.command(name="ship", description="Ship two people 💞")
@app_commands.describe(user1="First person", user2="Second person")
async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
    if user1.id == user2.id:
        return await interaction.response.send_message("❌ Can't ship the same person!", ephemeral=True)
    
    perc = random.randint(0, 100)
    responses = [
        "Literally soulmates", "They were made for each other", "Power couple vibes", 
        "Cute asf", "They make my heart melt", "10/10 would ship again", "Married in another life",
        "Perfect match", "Rizz recognized", "They complete each other", "Endgame", 
        "Couple goals", "Adorable together", "Chemistry off the charts", "Made in heaven",
        "Unbreakable bond", "OTP", "They glow together", "Main character energy", "Destined"
    ]
    
    if perc >= 90: title, color = "💞 PERFECT MATCH!", 0xFF1493
    elif perc >= 70: title, color = "❤️ Great Ship!", 0xFF69B4
    elif perc >= 50: title, color = "💖 Cute Ship", 0xFFC0CB
    else: title, color = "💔 Tragic...", 0x8B0000
    
    embed = discord.Embed(title=title, description=f"{user1.mention} ❤️ {user2.mention}", color=color)
    embed.add_field(name="Compatibility", value=f"**{perc}%** • {random.choice(responses)}", inline=False)
    await interaction.response.send_message(embed=embed)

# 8BALL
@tree.command(name="8ball", description="Ask the magic 8ball")
@app_commands.describe(question="Your question")
async def eightball(interaction: discord.Interaction, question: str):
    answer = random.choice(eightball_responses)
    await interaction.response.send_message(f"🎱 **Q:** {question}\n**A:** {answer}")

# Say (Invisible)
@tree.command(name="say", description="Make bot say something (invisible)")
@app_commands.describe(message="Message")
async def say(interaction: discord.Interaction, message: str):
    if not (interaction.user.id == ALMIGHTY_ID or is_vip(interaction.user.id)):
        return await interaction.response.send_message("❌ VIP / Almighty only!", ephemeral=True)
    await interaction.channel.send(message)
    await interaction.response.send_message("✅ Sent.", ephemeral=True)

# Mimic (Fixed)
@tree.command(name="mimic", description="Mimic someone (invisible)")
@app_commands.describe(member="Who to mimic", message="Message")
async def mimic(interaction: discord.Interaction, member: discord.Member, message: str):
    if not (interaction.user.id == ALMIGHTY_ID or is_vip(interaction.user.id)):
        return await interaction.response.send_message("❌ VIP / Almighty only!", ephemeral=True)
    
    try:
        if not interaction.channel.permissions_for(interaction.guild.me).manage_webhooks:
            return await interaction.response.send_message("❌ Bot needs **Manage Webhooks** permission!", ephemeral=True)
        
        webhook = await interaction.channel.create_webhook(name=member.display_name)
        await webhook.send(content=message, avatar_url=member.display_avatar.url, username=member.display_name)
        await webhook.delete()
        await interaction.response.send_message("✅ Mimicked!", ephemeral=True)
    except Exception as e:
        print(f"Mimic error: {e}")
        await interaction.response.send_message("❌ Failed. Check bot permissions (Manage Webhooks).", ephemeral=True)

# VIP
@tree.command(name="vip", description="Add VIP (Almighty only)")
@app_commands.describe(member="Member")
async def vip_cmd(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.id != ALMIGHTY_ID:
        return await interaction.response.send_message("❌ Only Almighty!", ephemeral=True)
    await add_vip(member.id)
    await interaction.response.send_message(f"✅ {member.mention} is now VIP!", ephemeral=True)

# DM
@tree.command(name="dm", description="DM someone (VIP+)")
@app_commands.describe(member="Target", message="Message")
async def dm(interaction: discord.Interaction, member: discord.Member, message: str):
    if not (interaction.user.id == ALMIGHTY_ID or is_vip(interaction.user.id)):
        return await interaction.response.send_message("❌ VIP only!", ephemeral=True)
    try:
        embed = discord.Embed(title="Message from Phantom Daviccino", description=message, color=0xFF00FF)
        await member.send(embed=embed)
        await interaction.response.send_message("✅ DM sent!", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Could not send DM.", ephemeral=True)

# Economy Commands
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
    await interaction.response.send_message(f"✅ You received **{reward}** coins!", ephemeral=False)

@tree.command(name="coins", description="Check your coins")
async def coins(interaction: discord.Interaction):
    bal = await get_coins(interaction.user.id)
    await interaction.response.send_message(f"💰 You have **{bal}** coins.", ephemeral=False)

@tree.command(name="leaderboard", description="Top 10 richest")
async def leaderboard(interaction: discord.Interaction):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id, coins FROM economy ORDER BY coins DESC LIMIT 10") as cur:
            rows = await cur.fetchall()
    embed = discord.Embed(title="🏆 Phantom Leaderboard", color=0xFFD700)
    for i, (uid, coins) in enumerate(rows, 1):
        member = interaction.guild.get_member(uid)
        name = member.display_name if member else f"ID {uid}"
        embed.add_field(name=f"#{i}", value=f"{name} — **{coins}** coins", inline=False)
    await interaction.response.send_message(embed=embed)

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
        print("❌ DISCORD_TOKEN not found!")
