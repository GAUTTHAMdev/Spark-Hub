import os
import discord
from discord.ext import commands
import asyncio
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID', '1268491866542833755'))

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix='/',
    intents=intents,
    owner_id=OWNER_ID,
    case_insensitive=True
)

# Load cogs function
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('_'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded cog: {filename[:-3]}')
            except Exception as e:
                print(f'Failed to load cog {filename[:-3]}: {e}')

# Main bot events
@bot.event
async def on_ready():
    print(f'\nLogged in as: {bot.user.name} - {bot.user.id}')
    print(f'Discord.py version: {discord.__version__}')
    print(f'Owner ID: {OWNER_ID}')
    print('------')
    
    # Set custom status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="your server 👀"
        )
    )

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("This command is reserved for the bot owner.")
    else:
        print(f'Error in command {ctx.command}: {error}')

# Graceful startup with rate limit handling
async def main():
    async with bot:
        await load_cogs()
        while True:
            try:
                await bot.start(TOKEN)
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after if hasattr(e, 'retry_after') else 30
                    print(f"Rate limited. Retrying in {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                else:
                    raise
            except Exception as e:
                print(f"Unexpected error: {e}. Restarting in 30 seconds...")
                await asyncio.sleep(30)

if __name__ == '__main__':
    asyncio.run(main())
