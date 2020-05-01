import logging
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

logging.basicConfig(
    filename="logging.log",
    level=logging.INFO,
    format="%(asctime)s;%(name)s;%(levelname)s;%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("CCCBot")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=":", owner_id=122919363656286212)

@bot.event
async def on_ready():
    logger.info(f"CCCBot connected to Discord | Discord.py Version {discord.__version__}")

@bot.event
async def on_command(ctx):
    loggger.info(f"Message: {ctx.message.content} - User: {ctx.message.author}")
    bot.startTimer = datetime.now()
    await ctx.trigger_typing()

@bot.event
async def on_command_competion(ctx):
    logger.info(f"Completed in {datetime.now() - bot.startTimer}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("You do not have the proper Permissions to use this command.")
        return
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"You are missing required parameters. Use `-help {ctx.invoked_with}` to check what is required.")
        return
    logger.exception(f"Error in {ctx.command}")
    owner = bot.get_user(bot.owner_id)
    await owner.send(f'Error in {ctx.command}\n{error}')

@bot.event
async def on_guild_join(guild):
    logger.info(f'CCCBot has joined "{guild.name}"" | Guild_ID: {guild.id} | Owner_ID: {guild.owner_id} | # of members: {len(guild.members)}')
    await bot.get_user(bot.owner_id).send(f'CCCBot has joined "{guild.name}" \nGuild_ID: {guild.id}\nOwner_ID: {guild.owner_id}\n# of members: {len(guild.members)}')

@bot.event
async def on_guild_remove(guild):
    logger.info(f'CCCBot was removed from "{guild.name}" | Guild_ID: {guild.id} | Owner_ID: {guild.owner_id}')
    await bot.get_user(bot.owner_id).send(f'CCCBot was removed from "{guild.name}"\nGuild_ID: {guild.id}\nOwner_ID: {guild.owner_id}')

bot.run(TOKEN)