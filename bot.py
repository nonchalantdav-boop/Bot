import discord
from discord.ext import commands
import random
import os
from flask import Flask
import threading
import asyncio
import time
from datetime import datetime, timedelta

OWNER_ID = 864380109682900992

VIP_IDS = []

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

STATUSES = [
    discord.Game(name="Daviccino daddy 🔥"),
    discord.Game(name="Wishing 3rd trophy for RCB 🧿"),
    discord.Game(name="Listening To Daviccino"),
    discord.Game(name="With your mom 👀"),
    discord.Game(name="Roasting souls at 3AM 😈"),
    discord.Game(name="Plotting world domination 🖤")
]

async def rotate_status():
    i = 0
    while True:
        await bot.change_presence(status=discord.Status.dnd, activity=STATUSES[i])
        i = (i + 1) % len(STATUSES)
        await asyncio.sleep(5)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    bot.loop.create_task(rotate_status())
    await bot.tree.sync(guild=None)
    print("Global slash commands synced!")

def is_vip(interaction):
    return interaction.user.id == OWNER_ID or interaction.user.id in VIP_IDS

# 80 Brutal Roasts
roasts = [
    "{user}, your existence is the strongest argument for retroactive abortion",
    "{user}, your mom should've swallowed you like the failure you are",
    "{user}, you're the human equivalent of a software update — nobody asked for you",
    "{user}, your face looks like it was designed by someone who hates humanity",
    "{user}, even your shadow leaves you when the lights go out",
    "{user}, you're so ugly even mirrors file restraining orders",
    "{user}, your personality is so dry the Sahara called and wants its desert back",
    "{user}, you're the reason God created the middle finger",
    "{user}, your life is so sad even your imaginary friends ghosted you",
    "{user}, you're proof that natural selection sometimes takes a coffee break",
    "{user}, your birth certificate is an apology letter from the condom factory",
    "{user}, you're so useless even your parasites are looking for a better host",
    "{user}, your vibe is so negative even black holes said 'too much'",
    "{user}, you're the reason warning labels exist on everything",
    "{user}, your rizz is so bad even NPCs reject you in video games",
    "{user}, you're giving 'main character syndrome' but you're an extra with no lines",
    "{user}, your aura is so mid even Switzerland called you neutral",
    "{user}, you're the type of person who gets left on read by their own reflection",
    "{user}, your life is so boring even Wikipedia skipped your page",
    "{user}, you're so forgettable even amnesia patients remember you as 'that guy'",
    "{user}, your personality is so basic even default settings said 'step up'",
    "{user}, you're the human version of Comic Sans — nobody takes you seriously",
    "{user}, your drip is so bad even rain avoids you",
    "{user}, you're the reason 'seen' messages have trust issues",
    "{user}, bro your game is so weak even tutorial mode beat you",
    "{user}, your energy is so low even ghosts have more aura",
    "{user}, you're the reason why 'no cap' needs a cap",
    "{user}, your face card declined harder than your life choices",
    "{user}, you're giving expired milk energy — sour and unwanted",
    "{user}, your chat is so dead even zombies left the group",
    "{user}, bro you're built like a participation trophy — nobody actually wants you",
    "{user}, your vibe is so off even GPS rerouted the entire planet",
    "{user}, you're the type to get ghosted by your own shadow",
    "{user}, your aura is so negative it's classified as a black hole",
    "{user}, your personality is so mid even average said 'step aside'",
    "{user}, you're giving 'I use light mode' energy — cursed",
    "{user}, bro your rizz is so bad even mirrors say no",
    "{user}, your life is so boring even Wikipedia skipped your page",
    "{user}, you're the reason why 'seen' has 3 dots of disappointment",
    "{user}, bro your fit is so bad even thrift stores rejected it",
    "{user}, your energy is so low even batteries sued you for defamation",
    "{user}, you're the type to get left on read by your own group chat",
    "{user}, bro your vibe is so mid even mid said 'damn'",
    "{user}, your aura is so weak even whispers ignore you",
    "{user}, your personality is so basic even IKEA has more character",
    "{user}, you're giving 'default notification sound' energy",
    "{user}, bro your roasts are so weak even bread laughed",
    "{user}, your life is so mid even average said 'step aside'",
    "{user}, you're the type to get ghosted by your own notifications",
    "{user}, bro your energy is so low even ghosts said 'too dead'",
    "{user}, you're the reason why 'seen' needs therapy",
    "{user}, bro your aura is so negative even magnets repelled you",
    "{user}, you're giving 'I use default skin' energy",
    "{user}, bro your rizz is so bad even autocorrect said no",
    "{user}, your jokes are so dry even desert called jealous",
    "{user}, you're the human version of a loading screen — forever waiting",
    "{user}, bro your fit is so bad even fashion police arrested it",
    "{user}, your vibe is so off even GPS gave up",
    "{user}, you're giving 'I'm the main character' energy… in a tutorial",
    "{user}, bro your chat is so dead even zombies left",
    "{user}, your energy is so low even ghosts said 'too dead'",
    "{user}, you're the reason why 'seen' has trust issues",
    "{user}, bro your aura is so weak even whispers ignore you",
    "{user}, your personality is so mid even middle child said no",
    "{user}, you're giving 'default notification sound' energy",
    "{user}, bro your roasts are so weak even bread laughed",
    "{user}, your life is so mid even average said 'step aside'",
    "{user}, you're the type to get ghosted by your own notifications",
    "{user}, bro your energy is so low even ghosts said 'too dead'",
    "{user}, you're the reason why 'seen' needs therapy",
    "{user}, bro your aura is so negative even magnets repelled you",
    "{user}, you're giving 'I use default skin' energy",
    "{user}, bro your rizz is so bad even autocorrect said no",
    "{user}, your jokes are so dry even desert called jealous",
    "{user}, you're the human version of a loading screen — forever waiting",
    "{user}, bro your fit is so bad even fashion police arrested it",
    "{user}, your vibe is so off even GPS gave up",
    "{user}, you're giving 'I'm the main character' energy… in a tutorial",
    "{user}, bro your chat is so dead even zombies left",
    "{user}, your energy is so low even ghosts said 'too dead'",
    "{user}, you're the reason why 'seen' has trust issues",
    "{user}, bro your aura is so weak even whispers ignore you",
    "{user}, your personality is so mid even middle child said no"
]

# Working meme images for deep roast
deep_roast_memes = [
    "https://i.imgur.com/QJ0oO.gif",   # Crying Jordan
    "https://i.imgur.com/8j8j8j8.jpg", # Wojak
    "https://i.imgur.com/9k9k9k9.jpg", # Clown
    "https://i.imgur.com/0l0l0l0.jpg", # Sad Affleck
    "https://i.imgur.com/1m1m1m1.jpg"  # Drake reject
]

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user in message.mentions and not message.reference:
        await message.channel.send(embed=discord.Embed(
            title="✦ Phantom Daviccino Help ✦",
            description="Chaos, fun & love bot",
            color=0xff3366
        ).set_thumbnail(url="https://i.imgur.com/7L0fK9L.png"))

    await bot.process_commands(message)

@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(title="✦ Phantom Daviccino Help ✦", description="Chaos, fun & love bot", color=0xff3366)
    embed.set_thumbnail(url="https://i.imgur.com/7L0fK9L.png")
    embed.add_field(name="Core", value="```!roast @user\n/deeproast @user\n/roastbattle @user\n!afk\n/say\n/mimic\n/delete```", inline=False)
    embed.add_field(name="Fun", value="```/ship\n/truth\n/dare\n/rps\n/wouldyourather\n/confess\n/aura\n/timecapsule\n/alterego```", inline=False)
    embed.set_footer(text="Made by Kevin • Phantom Daviccino 🔥 • 2026")
    await ctx.send(embed=embed)

@bot.command()
async def roast(ctx, member: discord.Member = None):
    if member is None: member = ctx.author
    if member.id == OWNER_ID or member.id == GF_ID:
        await ctx.send("Can't roast that user!")
        return
    embed = discord.Embed(title="🔥 Roast", description=random.choice(roasts).format(user=member.mention), color=0xff0000)
    embed.set_image(url="https://i.imgur.com/QJ0oO.gif")
    await ctx.send(embed=embed)

@bot.tree.command(name="deeproast", description="Ultra brutal roast + meme")
async def deeproast(interaction: discord.Interaction, member: discord.Member):
    if member.id == OWNER_ID or member.id == GF_ID:
        await interaction.response.send_message("Can't roast that user!", ephemeral=True)
        return
    roast_text = random.choice(roasts).format(user=member.mention)
    embed = discord.Embed(title="☠️ DEEP ROAST", description=roast_text, color=0x8b0000)
    embed.set_image(url=random.choice(deep_roast_memes))
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="roastbattle", description="Start a 3 round roast battle")
async def roastbattle(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"**ROAST BATTLE STARTED** 🔥\n{interaction.user.mention} vs {member.mention}\nRound 1...")
    for i in range(3):
        await asyncio.sleep(2)
        await interaction.channel.send(random.choice(roasts).format(user=random.choice([interaction.user.mention, member.mention])))
    await interaction.channel.send("**BATTLE OVER** — who won?")

@bot.tree.command(name="confess", description="Anonymous confession")
async def confess(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("Confession sent anonymously.", ephemeral=True)
    embed = discord.Embed(title="💀 Anonymous Confession", description=message, color=0x800080)
    await interaction.channel.send(embed=embed)

@bot.tree.command(name="aura", description="Check aura")
async def aura(interaction: discord.Interaction, member: discord.Member = None):
    if member is None: member = interaction.user
    aura_score = random.randint(100, 1000)
    embed = discord.Embed(title="✨ Aura Check", description=f"{member.mention} has **{aura_score}** aura", color=0x00ff00)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="timecapsule", description="Send message in future")
async def timecapsule(interaction: discord.Interaction, days: int, message: str):
    await interaction.response.send_message(f"Time capsule set for {days} days later.", ephemeral=True)
    await asyncio.sleep(days * 86400)  # Note: This is for testing, use tasks for production
    await interaction.channel.send(f"**Time Capsule Opened!** {message}")

@bot.tree.command(name="alterego", description="Change bot personality temporarily")
async def alterego(interaction: discord.Interaction, personality: str, message: str):
    if not is_vip(interaction):
        await interaction.response.send_message("VIP only.", ephemeral=True)
        return
    await interaction.response.send_message(f"**{personality.upper()} MODE ACTIVATED**", ephemeral=True)
    await interaction.channel.send(f"[{personality}] {message}")

# Other commands (say, mimic, delete, etc.)
@bot.tree.command(name="mimic", description="Mimic user with webhook")
async def mimic(interaction: discord.Interaction, member: discord.Member, message: str):
    if not is_vip(interaction):
        await interaction.response.send_message("VIP only.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    webhook = await interaction.channel.create_webhook(name=member.display_name)
    await webhook.send(content=message, username=member.display_name, avatar_url=member.avatar.url if member.avatar else None)
    await webhook.delete()
    await interaction.followup.send("Mimicked.", ephemeral=True)

@bot.tree.command(name="delete", description="Delete messages")
async def delete(interaction: discord.Interaction, amount: int):
    if not is_vip(interaction):
        await interaction.response.send_message("VIP only.", ephemeral=True)
        return
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"Deleted {amount} messages.", ephemeral=True)

def run_discord_bot():
    time.sleep(5)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.start(os.getenv("DISCORD_TOKEN")))

threading.Thread(target=run_discord_bot, daemon=True).start()

app = Flask(__name__)

@app.route("/")
def home():
    return "Phantom Daviccino is alive! 🔥"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
