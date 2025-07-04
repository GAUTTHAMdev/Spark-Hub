import discord
from discord.ext import commands

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def apitest(self, ctx):
        """Test an API call with proper error handling"""
        try:
            async with self.bot.http_session.get("https://httpbin.org/json") as response:
                if response.status != 200:
                    await ctx.send(f"API error: HTTP {response.status}")
                    return
                data = await response.json()
                await ctx.send(f"Success: {data}")
        except Exception as e:
            await ctx.send(f"API request failed: {e}")

async def setup(bot):
    await bot.add_cog(TestCog(bot))
