import discord
from discord.ext import commands
from utils.database import db
from utils.embeds import create_embed

class VIPCog(commands.Cog):
    @commands.hybrid_command(name="say")
    async def say(self, ctx, *, text: str):
        isvip = ctx.user.id == 864380109682900992 or await db.is_vip(ctx.user.id)
        if not isvip:
            return await ctx.send("👑 VIP only!", ephemeral=True)
        await ctx.send(text)
        await ctx.send("✅ Sent!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(VIPCog(bot))
