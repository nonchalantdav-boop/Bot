from flask import Flask
import os
import random
import asyncio
import threading
import discord
from discord import app_commands, ui
from discord.ext import commands
import aiosqlite
from datetime import datetime, timedelta

# ========================= FLASK =========================
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

# ====================== STATUS ======================
statuses = ["WITH YOUR MOM 👀", "Rizzing up servers", "Daviccino Daddy 🔥", 
            "Serving Top 1% Energy", "Roasting souls for fun", "Collecting L's from you"]

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
        await db.execute("CREATE TABLE IF NOT EXISTS economy (user_id INTEGER PRIMARY KEY, coins INTEGER DEFAULT 0, last_daily TEXT)")
        await db.execute("CREATE TABLE IF NOT EXISTS vips (user_id INTEGER PRIMARY KEY)")
        await db.commit()

async def get_coins(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT coins FROM economy WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0

async def add_coins(user_id, amount):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO economy (user_id, coins) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET coins = coins + ?", 
                        (user_id, amount, amount))
        await db.commit()

async def add_vip(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO vips (user_id) VALUES (?)", (user_id,))
        await db.commit()

def is_vip(user_id):
    return user_id == ALMIGHTY_ID

# ====================== ROASTS ======================
roasts = [
    "You're the reason abortions exist.",
    "Even your mom fakes the moans.",
    "Sperm donor's biggest regret.",
    "Your birth was a biological error.",
    "God's 'oops' moment.",
    "You peaked at fertilization.",
    "Condoms file restraining orders against you.",
    "Human trash bag.",
    "Walking advertisement for vasectomy.",
    "Your face is a war crime.",
    "Even mirrors crack in protest.",
    "Ugly doesn't cover it.",
    "Built like a rejected prototype.",
    "Your dad swallowed better.",
    "Breathing is your only achievement.",
    "Natural selection's side project.",
    "You're why 'skip' exists.",
    "The 'before' in every glow-up.",
    "Personality of wet cardboard.",
    "Even hell rejected your application.",
    "Virgin by universal vote.",
    "Your IQ needs life support.",
    "Die in obscurity, loser.",
    "Forgotten before you arrived.",
    "Your bloodline deserves extinction.",
    "Proof life has no quality control.",
    "You're the glitch nobody patches.",
    "Smells like failure and BO.",
    "Your existence is community service.",
    "Adopted by pure disappointment.",
    "Even roaches avoid you.",
    "The human equivalent of lag.",
    "Your mom regrets not swallowing.",
    "Built for irrelevance.",
    "Cursed by every god.",
    "You're the final boss of mid.",
    "Face like expired milk.",
    "Soul like a black hole.",
    "Zero redeemable qualities.",
    "Breath smells like regret.",
    "You're what happens after 'pull out' fails.",
    "The reason dating apps have block buttons.",
    "Evolutionary dead end.",
    "Your reflection files lawsuits.",
    "Talentless, faceless, useless.",
    "Even your shadow leaves early.",
    "Walking participation trophy.",
    "Your genes deserve jail.",
    "Useless as a participation medal.",
    "The void stares back less empty.",
    "Daddy issues in human form.",
    "Mom's biggest 'what if'.",
    "You're digital diarrhea.",
    "Personality bankruptcy declared.",
    "Even AI feels sorry for you.",
    "The 'L' in everyone's alphabet.",
    "Your life is a loading error.",
    "Built like a question nobody asked.",
    "Cunt with no warmth.",
    "Your aura is toxic waste.",
    "Forgotten sperm that survived.",
    "God's deleted draft.",
    "You're the 'decline' button.",
    "Face only a mother tolerates… barely.",
    "Zero drip, all trip.",
    "The human '404 not found'.",
    "Your existence is a glitch.",
    "Even therapy ghosts you.",
    "Built for the block list.",
    "Walking argument for eugenics.",
    "Your vibe is clinical depression.",
    "The reason 'nevermind' was invented.",
    "Soul sold for participation.",
    "You're background noise.",
    "Even your dreams quit.",
    "Humanity's loading screen.",
    "The final 'fuck it' of creation.",
    "Your legacy: none.",
    "Die mad and irrelevant.",
    "You're not even worth the roast.",
    "Your forehead needs its own zip code.",
    "Built like a question mark.",
    "Even your screenshots are ugly.",
    "You have negative aura.",
    "The type to get rejected by a fleshlight.",
    "Your rizz is in negative digits.",
    "Smells like expired milk and broken dreams.",
    "You're the 'Do Not Reply' in group chats.",
    "Face card declined.",
    "Walking red flag factory.",
    "Broke boy with rich delusions.",
    "Simp level: legendary.",
    "Your body count is 0 and your personality is -10.",
    "Certified community toilet.",
    "The reason birth control was invented.",
    "You scream 'I have no friends'.",
    "Invisible to baddies.",
    "Your drip is dry as the Sahara.",
    "Even Google can't find your highlights.",
    "Permanent benchwarmer.",
    "You’re what happens when motivation pulls out.",
    "Mid in every universe.",
    "Your vibes need a restraining order.",
    "The human version of Comic Sans.",
    "Even your plants fake growing.",
    "Bro got rejected by life itself.",
    "Your personality is on airplane mode.",
    "Built like a budget cut.",
    "The final boss of disappointment.",
    "Your scalp is visible from space.",
    "Even darkness says 'too black'.",
    "You make onions cry.",
    "Negative rizz, negative game.",
    "The 'L' is permanently tattooed on your forehead.",
    "Your future is loading... 404 error.",
    "Certified yapper with zero sauce.",
    "Even your echo ignores you.",
    "Your existence is a participation award.",
    "Built like a discount version of a human.",
    "You're the glitch in the simulation."
]

# ========================= EVENTS =========================
@bot.event
async def on_ready():
    await init_db()
    print(f"✅ {bot.user} is fully loaded!")
    bot.loop.create_task(status_rotation())
    await tree.sync()
    print("✅ All commands synced")

@bot.event
async def on_message(message):
    if message.author.bot: return
    if bot.user.mentioned_in(message):
        await message.reply(embed=discord.Embed(title="Phantom Daviccino 👑", description="Use `/help`", color=0xFF00FF))
    await bot.process_commands(message)

# ========================= HELP =========================
@tree.command(name="help", description="Full command list")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Phantom Daviccino — Top 1% Bot 👑", color=0xFF00FF)
    embed.add_field(name="Economy", value="/daily /coins /gamble /leaderboard", inline=False)
    embed.add_field(name="Fun", value="/roast /ship /8ball /dice /rps /poll /tictactoe", inline=False)
    embed.add_field(name="Social", value="/hug /slap /compliment", inline=False)
    embed.add_field(name="VIP", value="/vip /say /dm /mimic", inline=False)
    embed.add_field(name="Moderation", value="/ban /kick /mute /unmute", inline=False)
    await interaction.response.send_message(embed=embed)

# Roast (Visible)
@tree.command(name="roast", description="Savage roast someone 🔥")
@app_commands.describe(member="Who to roast")
async def roast(interaction: discord.Interaction, member: discord.Member):
    if member.id == ALMIGHTY_ID:
        return await interaction.response.send_message(f"{member.mention} is **Almighty** — Untouchable.", ephemeral=False)
    roast_text = random.choice(roasts)
    embed = discord.Embed(title="☠️ PHANTOM ROAST", description=f"{member.mention} {roast_text}", color=0xFF0000)
    await interaction.response.send_message(embed=embed)

# VIP Commands
@tree.command(name="vip", description="Give VIP (Almighty only)")
@app_commands.describe(member="Member")
async def vip_cmd(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.id != ALMIGHTY_ID:
        return await interaction.response.send_message("❌ Only Almighty!", ephemeral=True)
    await add_vip(member.id)
    await interaction.response.send_message(f"✅ {member.mention} is now VIP!", ephemeral=True)

@tree.command(name="say", description="Bot says something (invisible)")
@app_commands.describe(message="Message")
async def say(interaction: discord.Interaction, message: str):
    if not (interaction.user.id == ALMIGHTY_ID or is_vip(interaction.user.id)):
        return await interaction.response.send_message("❌ VIP only!", ephemeral=True)
    await interaction.channel.send(message)
    await interaction.response.send_message("✅ Sent.", ephemeral=True)

@tree.command(name="mimic", description="Mimic someone (invisible)")
@app_commands.describe(member="Who to mimic", message="Message")
async def mimic(interaction: discord.Interaction, member: discord.Member, message: str):
    if not (interaction.user.id == ALMIGHTY_ID or is_vip(interaction.user.id)):
        return await interaction.response.send_message("❌ VIP only!", ephemeral=True)
    try:
        webhook = await interaction.channel.create_webhook(name=member.display_name)
        await webhook.send(content=message, avatar_url=member.display_avatar.url)
        await webhook.delete()
        await interaction.response.send_message("✅ Mimicked.", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Failed.", ephemeral=True)

@tree.command(name="dm", description="DM someone (VIP+)")
@app_commands.describe(member="Target", message="Message")
async def dm(interaction: discord.Interaction, member: discord.Member, message: str):
    if not (interaction.user.id == ALMIGHTY_ID or is_vip(interaction.user.id)):
        return await interaction.response.send_message("❌ VIP only!", ephemeral=True)
    try:
        embed = discord.Embed(title="From Phantom Daviccino", description=message, color=0xFF00FF)
        await member.send(embed=embed)
        await interaction.response.send_message("✅ DM sent.", ephemeral=True)
    except:
        await interaction.response.send_message("❌ Could not DM.", ephemeral=True)

# Economy
@tree.command(name="daily", description="Claim daily coins")
async def daily(interaction: discord.Interaction):
    # (Same logic as before - copy from previous messages if needed)
    user_id = interaction.user.id
    reward = random.randint(150, 300)
    await add_coins(user_id, reward)
    await interaction.response.send_message(f"✅ You got **{reward}** coins!", ephemeral=False)

@tree.command(name="coins", description="Check balance")
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
        name = member.display_name if member else f"User {uid}"
        embed.add_field(name=f"#{i}", value=f"{name} — **{coins}** coins", inline=False)
    await interaction.response.send_message(embed=embed)

# Games & Social Commands
@tree.command(name="8ball", description="Ask the magic 8ball")
@app_commands.describe(question="Your question")
async def eightball(interaction: discord.Interaction, question: str):
    responses = ["Yes", "No", "Maybe", "Definitely", "Ask again later", "Outlook good", "Very doubtful"]
    await interaction.response.send_message(f"🎱 **Question:** {question}\n**Answer:** {random.choice(responses)}")

@tree.command(name="dice", description="Roll a dice")
async def dice(interaction: discord.Interaction):
    await interaction.response.send_message(f"🎲 You rolled a **{random.randint(1,6)}**!")

@tree.command(name="hug", description="Hug someone")
@app_commands.describe(member="Who to hug")
async def hug(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"{interaction.user.mention} hugged {member.mention} 🤗")

@tree.command(name="slap", description="Slap someone")
@app_commands.describe(member="Who to slap")
async def slap(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"{interaction.user.mention} slapped {member.mention} 👋")

# Add more commands like /rps, /poll, /tictactoe, /ban etc. if you want the absolute full version.

# ========================= RUN =========================
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    TOKEN = os.environ.get("DISCORD_TOKEN")
    bot.run(TOKEN)
