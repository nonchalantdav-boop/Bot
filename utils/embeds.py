import discord
from datetime import datetime

def create_embed(title, description, color=0xff3366):
    embed = discord.Embed(title=title, description=description, color=color, timestamp=datetime.utcnow())
    embed.set_footer(text="Phantom Daviccino 🔥")
    return embed
