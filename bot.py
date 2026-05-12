import asyncio
import os
from flask import Flask
import discord
from discord.ext import commands

app = Flask(__name__)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

roasts = ["{user} so mid 😂", "{user} rizz = 0 💀"]

@bot.event
async def on_ready():
    print(f"🔥 {bot.user} LIVE!")
    await bot.change_presence(activity=discord.Game("Daviccino Daddy 🔥"))

@bot.event
async def on_message(message):
    if bot.user in message.mentions and not message.author.bot:
        await message.reply("**/roast /ship /help**\nTag me anytime! 🔥")
    
    await bot.process_commands(message)

@bot.command()
async def roast(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    roast_text = random.choice(roasts).format(user=member.mention)
    await ctx.send(f"🔥 {roast_text}")

@app.route("/")
def home():
    return "Phantom Daviccino 🔥 ALIVE"

bot.run(os.getenv("DISCORD_TOKEN"))
