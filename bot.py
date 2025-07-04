import discord
from discord.ext import commands
import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def main():
    # Create a shared aiohttp session and attach it to the bot
    bot.http_session = aiohttp.ClientSession()

    # Start the bot
    try:
        await bot.start(TOKEN)
    finally:
        # Ensure the session is closed when the bot stops
        await bot.http_session.close()

if __name__ == "__main__":
    asyncio.run(main())
