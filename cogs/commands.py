import discord
import apirequests
import logging
import utils
import asyncio
from discord.ext import commands

logger = logging.getLogger(f"CCCBot.{__name__}")

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def cccsearch(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Subcommands are projects and users")
    
    @cccsearch.command()
    async def projects(self, ctx, *, order):
        original_user = ctx.author.id
        project_num = 0
        msg = None
        if order is None:
            order = "featured"
        if order not in ["featured", "popular", "updated at", "listed at", "rating"]:
            await ctx.send("Sorry, that order is not valid. Valid orders are: ```Featured, Popular, Updated at, Listed at, and Rating```")
            return
        search = await apirequests.ccc_search(ctx, order)
        while True:
            project = search["projects"][project_num]
            embed = discord.Embed(title=f"{project['name']} by {project['username']}", color=0xA9152B, description=f"https://www.castingcall.club/projects/{project['id']}")
            embed.set_thumbnail(url=project["public_image_url"])
            embed.add_field(name="# of Roles Available", value=f"{project['roles_available_count']}", inline=True)
            embed.add_field(name="# of Auditions", value=f"{project['auditions_count']}", inline=True)
            embed.add_field(name="Rating", value=f"{project['rating_in_words']} ({project['rating_display']})", inline=True)
            embed.add_field(name="Deadline", value=f"{project['deadline']}", inline=True)
            embed.add_field(name="Listed at", value=f"{project['listed_at']}", inline=True)
            embed.add_field(name="Last Updated", value=f"{project['project_updated_at']}", inline=True)
            roles1 = ""
            roles2 = ""
            roles3 = ""
            for role in project["roles"]:
                 roles1 += f"{role['name']} - {role['kind']}\n"
                 roles2 +=  f"{role['gender']} - {role['language']}\n"
                 roles3 += f"{role['age']} - {role['accent']}\n"
            embed.add_field(name="Roles", value = roles1, inline=True)
            embed.add_field(name="** **", value = roles2, inline=True)
            embed.add_field(name="** **", value = roles3, inline=True)
            if msg == None:  
                msg = await ctx.send(embed=embed)
            else:
                await discord.Message.edit(msg, embed=embed)
            react = await reaction_check(self, ctx, msg, original_user, project_num)
            if react == False:
                return
            react = react[0]
            if react.emoji == '➡':
                project_num += 1
            elif react.emoji == '⬅️':
                project_num -= 1
            elif react.emoji == '❌':
                await discord.Message.clear_reactions(msg)
                return

    @cccsearch.command()
    async def users(self, ctx, *, ccc_user):
        original_user = ctx.author.id
        user_num = 0
        page_num = 1
        msg = None
        user_list = await apirequests.ccc_users(ctx, ccc_user, page_num)
        while True:
            user = user_list["users"][user_num]
            if user['accents'] == "":
                accents = "N/A"
            else:
                accents = user['accents']
            if user['languages'] == "":
                languages = "N/A"
            else:
                languages = user['languages']
            if user['skills'] == "":
                skills = "N/A"
            else:
                skills = user['skills']
            embed = discord.Embed(title=f"{user['username'].title()} on CCC", color=0xA9152B, description=f"https://www.castingcall.club{user['user_path']}")
            embed.set_thumbnail(url=user["public_audio_url"])
            embed.add_field(name="Accents", value=accents, inline=True)
            embed.add_field(name="Languages", value=languages, inline=True)
            embed.add_field(name="Skills", value=skills, inline=True)
            embed.add_field(name=user['demo_name'], value=f"[Link]({user['public_audio_url']})")
            if msg == None:
                msg = await ctx.send(embed=embed)
            else:
                await discord.Message.edit(msg, embed=embed)
            react = await reaction_check(self, ctx, msg, original_user, user_num)
            if react == False:
                return
            react = react[0]
            if react.emoji == '➡':
                user_num += 1
            elif react.emoji == '⬅️':
                user_num -= 1
            elif react.emoji == '❌':
                await discord.Message.clear_reactions(msg)
                return
    
    @commands.command(name="sendGetRoles", hidden=True)
    @commands.is_owner()
    async def sendGetRoles(self, ctx):
        emojis = await utils.role_reaction_emojis()
        embed = discord.Embed(title="Add/Remove a reaction to add/remove the corresponding role", color = 0xA9152B)
        embed.add_field(name="Voice Type", value=f"Female - {emojis['Female']}\nMale - {emojis['Male']}", inline=True)
        skills_msg = f"Voice Actor - {emojis['VA']}\nArtist - {emojis['Artist']}\nEditor - {emojis['Editor']}\nAnimator - {emojis['Animator']}\nWriter - {emojis['Writer']}\n"
        skills_msg+= f"Singer - {emojis['Singer']}\nComposer - {emojis['Composer']}\nDirector - {emojis['Director']}\nGame Dev - {emojis['GameDev']}\nRapper - {emojis['Rapper']}\n"
        skills_msg+= f"Sound Engineer/Mixer - {emojis['Sound']}"
        embed.add_field(name="Skills", value=skills_msg, inline=True)
        #embed.add_field(name="Miscellanous", value=f"Event Notifications - {emojis['Notice']}", inline=True)
        embed.add_field(name="Server Access", value=f"To get access to the rest of the server, click the ✅ emoji", inline=False)
        getRolesMsg = await ctx.send(embed=embed)
        for emoji in emojis:
            await discord.Message.add_reaction(getRolesMsg, emojis[emoji])
        return


async def reaction_check(self, ctx, msg, original_user, project_num):
    try:
        allowed_reactions = []
        if project_num != 0:
            await discord.Message.add_reaction(msg, '⬅️')
            allowed_reactions.append('⬅️')
        await discord.Message.add_reaction(msg, '➡')
        await discord.Message.add_reaction(msg, '❌')
        allowed_reactions.append('❌')
        allowed_reactions.append('➡')

        def check(reaction, user):
            return user.id == original_user and reaction.emoji in allowed_reactions and reaction.message.id == msg.id

        try:
            react = await self.bot.wait_for(event="reaction_add", timeout=120.0, check=check)
        except asyncio.TimeoutError:
            embed = discord.Embed(title="Timeout", color=0xA9152B)
            embed.add_field(name="Timeout", value="Your request has timed out.", inline=False)
            await discord.Message.edit(msg, embed=embed)
            await discord.Message.clear_reactions(msg)
            return False
        await discord.Message.clear_reactions(msg)
        return react
    except:
        logger.exception("debug shit")
    
    
def setup(bot):
    bot.add_cog(Commands(bot))