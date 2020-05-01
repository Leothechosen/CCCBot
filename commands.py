import discord
import apirequests
import logging

logger = logging.getLogger(f"CCCBot.{__name__}")

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def cccsearch(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctxd.send("Subcommands are")
    
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
            embed = discord.Embed(title=f"Casting Call Club - {project['name']} by {project['username']}", color=0xA9152B, description=f"https://www.castingcall.club/projects/{project['id']}")
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