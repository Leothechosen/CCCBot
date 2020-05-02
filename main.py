import logging
import os
import discord
import utils
from datetime import datetime
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
    logger.info(f"Message: {ctx.message.content} - User: {ctx.message.author}")
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

@bot.event
async def on_raw_reaction_add(payload):
    pass
    try:
        if payload.message_id != 706011309015171122:
            return
        role_reaction = await utils.role_reaction_emojis(str(payload.emoji))
        role_to_add = await utils.role_reaction_roles(str(role_reaction))
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(role_to_add)
        member = guild.get_member(payload.user_id)
        await member.add_roles(role)
        if role.name == "Member":
            roleless_role = await utils.role_reaction_roles("Roleless")
            roleless_role = guild.get_role(roleless_role)
            await member.remove_roles(roleless_role)
    except:
        logger.exception("Add Role Error")

@bot.event
async def on_raw_reaction_remove(payload):
    try:
        if payload.message_id != 706011309015171122:
            return
        if str(payload.emoji) == "✅":
            return
        role_reaction = await utils.role_reaction_emojis(str(payload.emoji))
        role_to_remove = await utils.role_reaction_roles(str(role_reaction))
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(role_to_remove)
        member = guild.get_member(payload.user_id)
        await member.remove_roles(role)
    except:
        logger.exception("Remove Role Error")
        

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(TOKEN)