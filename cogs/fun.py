import discord
from discord.ext import commands
import random
from utils.database import db
from utils.embeds import create_embed

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or self.bot.user not in message.mentions:
            return
        embed = create_embed("✦ Phantom Daviccino ✦", "**Use slash commands:**\n/roast /ship /coins /play")
        await message.reply(embed=embed)

    @commands.hybrid_command(name="roast")
    async def roast(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        if member.id in [864380109682900992, 1425090711019192434]:
            return await ctx.send("❌ Can't roast royalty!")
        
        roasts = [f"{member.mention}, your rizz so bad even Siri said no 😂"]
        embed = create_embed("🔥 ROASTED", random.choice(roasts), 0xff0000)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(FunCog(bot))
