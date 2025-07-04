import discord
from discord.ext import commands
import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env file
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    bot.http_session = aiohttp.ClientSession()  # ✅ create shared session for bot
    await load_cogs()
    try:
        await bot.start(TOKEN)
    finally:
        await bot.http_session.close()  # ✅ close session on shutdown

if __name__ == "__main__":
    asyncio.run(main())
