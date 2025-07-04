from discord.ext import commands

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def apitest(self, ctx):
        # Reuse the shared session stored in bot
        async with self.bot.http_session.get("https://api.github.com") as response:
            data = await response.json()
            await ctx.send(f"GitHub API says: {data.get('current_user_url', 'no response')}")

async def setup(bot):
    await bot.add_cog(TestCog(bot))
