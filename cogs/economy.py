import discord
from discord.ext import commands
import random
import aiosqlite
from utils.embeds import create_embed

class EconomyCog(commands.Cog):
    @commands.hybrid_command(name="coins")
    async def coins(self, ctx):
        async with aiosqlite.connect("data/database.db") as db:
            async with db.execute("SELECT coins FROM economy WHERE user_id = ?", (ctx.author.id,)) as cursor:
                result = await cursor.fetchone()
                coins = result[0] if result else 100
        embed = create_embed("💰 Balance", f"You have **{coins}** coins")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EconomyCog(bot))
