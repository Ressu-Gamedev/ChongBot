import os, discord, wolframalpha, asyncio
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='=', intents=intents)
wolframclient = wolframalpha.Client(os.environ['wolframid'])

welcomemsg = \
"""
This server has multiple roles you can freely enable and disable.
Some roles will give you access to new channels.
Choose the roles you want by reacting to this message:

<:questionblock:618688348118319124> - Gamer
<:development:613412002479734813> - Game Development
<:anime:853280193845788703> - Anime

<:nnid:614109123373694988> - Nintendo Games
<:smashball:614108654249050123> - Smash Bros

<:amongus:774370024180678686> - Among Us (and other party games, like Jackbox)
<:apex:853259647297388546> - Apex Legends
<:csgo:614108639392825364> - CS:GO
<:hearthstone:853266960917463081> - Hearthstone
<:league:614108654949367808> - League of Legends + TFT
<:creeper:614108636230451211> - Minecraft
<:osu:618694109032349705> - Osu!
<:ow:614108644736368659> - Overwatch
<:r6s:745352944613851136> - Rainbow Six: Siege
<:rocketleague:745354308660363397> - Rocket League
<:tetris:853263337839788042> - Tetris
<:valorant:745352946782306384> - Valorant
<:VR:745352948305100821> - VR Games
<:wow:618712696509956107> - World of Warcraft

<:fortnite:618689756477521920> - Fortnite

All roles will also give you their sub-roles (e.g. Overwatch will give you both the Gamer and Overwatch roles)
Game roles are pingable. Feel free to ping one in <#745344915252314239> to call people to play with you.
Enjoy your stay!
"""
welcomedm = \
"""
Welcome to the Ressu Gamers Discord!
We have channels for both gaming and game development.
Check the <#613446760563474442> channel to get your roles and access new channels.
Please also set your server nickname to your real name, so that everyone gets to know each other :smile:

Have fun!
ChongBot:tm:
"""
welcomegeneral = \
"""
Welcome to the server {}!
Go press the reaction buttons in <#613446760563474442> to get some roles.
"""
kickdm = \
"""
You have been kicked from the Ressu Gamers server for the reason:
NO MORE FORTNITE!

You may rejoin the server using the permanent invite link: https://discord.gg/A635RGS
"""
general_id = 613436762257358878


class Node:
    def __init__(self, emote, role, children=[]):
        self.emote = emote
        self.role = role
        self.children = children


    def add_children(self, *children):
        self.children += children
    

    async def give(self, emote, user, guild):
        if self.emote == emote:
            await user.add_roles(discord.utils.get(guild.roles, name=self.role))
            return True
        
        for child in self.children:
            res = await child.give(emote, user, guild)
            if res and self.role:
                await user.add_roles(discord.utils.get(guild.roles, name=self.role))
                return True
        
        return False
        

    async def remove(self, emote, user, guild):
        if self.emote == emote:
            await user.add_roles(discord.utils.get(guild.roles, name=self.role))
            for child in self.children:
                await child.nuke(user, guild)
            return
        
        for child in self.children:
            child.remove(emote, user, guild)


    async def nuke(self, user, guild):
        await user.add_roles(discord.utils.get(guild.roles, name=self.role))
        for child in self.children:
            await child.nuke()


    async def reactwith(self, fetchedwelcome, guild):
        if self.emote:
            await fetchedwelcome.add_reaction(discord.utils.get(guild.emojis, name=self.emote))

        for child in self.children:
            await child.reactwith(fetchedwelcome, guild)


root = Node(None, None)
root.add_children(
    Node("anime", "Anime"),
    Node("development", "Game Developer"),
    Node("fortnite", ""),
    Node("questionblock", "Gamer", [
        Node("nnid", "Nintendo", [
            Node("smashball", "Smash Bros"),
        ]),
        Node("amongus", "Among Us"),
        Node("apex", "Apex Legends"),
        Node("csgo", "CS:GO"),
        Node("hearthstone", "Hearthstone"),
        Node("league", "League of Legends"),
        Node("creeper", "Minecraft"),
        Node("osu", "Osu!"),
        Node("ow", "Overwatch"),
        Node("r6s", "Rainbow Six Siege"),
        Node("rocketleague", "Rocket League"),
        Node("tetris", "Tetris"),
        Node("valorant", "Valorant"),
        Node("VR", "VR"),
        Node("wow", "World of Warcraft"),
    ]),
)


def writeID(id):
    os.environ["welcomeid"] = str(id)


def getID():
    return int(os.environ["welcomeid"])


@bot.event
async def on_ready():
    if not "welcomeid" in os.environ:
        writeID(0)
    
    print('Logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower().startswith('sigma'):
        await message.channel.send('Simba')
        
    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    if message.id == getID():
        writeID(0)


@bot.event
async def on_raw_reaction_add(data):
    if not data.message_id == getID():
        return
    if data.user_id == bot.user.id:
        return
    
    guild = await bot.fetch_guild(data.guild_id)
    user = await guild.fetch_member(data.user_id)
    
    if data.emoji.name == "fortnite":
        await user.send(kickdm)
        general = bot.get_channel(general_id)
        await general.send("@{}#{} was kicked from the server for playing Fortnite.".format(user.name, user.discriminator))
        await user.kick()
        return
    
    await root.give(data.emoji.name, user, guild)


@bot.event
async def on_raw_reaction_remove(data):
    if not data.message_id == getID():
        return
    if data.user_id == bot.user.id:
        return
    
    guild = await bot.fetch_guild(data.guild_id)
    user = await guild.fetch_member(data.user_id)
    
    await root.remove(data.emoji.name, user, guild)


@bot.event
async def on_member_join(member):
    await member.send(welcomedm)
    general = bot.get_channel(general_id)
    await general.send(welcomegeneral.format(member.mention))


@tasks.loop(minutes=60)
async def game_presence():
    total = len(bot.users)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{total} students"))


@game_presence.before_loop
async def wait():
    await bot.wait_until_ready()


@bot.command()
@commands.has_permissions(administrator=True)
async def welcome(ctx):
    await ctx.message.delete()
    if not getID() == 0:
        await ctx.send(f"There already exists a welcome message. Remove it first with =nowelcome.")
        return
    
    sent = await ctx.send(welcomemsg)
    writeID(sent.id)
    
    await root.reactwith(sent, ctx.guild)


@bot.command()
@commands.has_permissions(administrator=True)
async def nowelcome(ctx):
    await ctx.message.delete()
    if getID() == 0:
        await ctx.send("There is already no welcome message.")
        return
    
    await ctx.send("Unbound welcome message.")
    writeID(0)


@bot.command()
@commands.has_permissions(administrator=True)
async def updatewelcome(ctx):
    await ctx.message.delete()
    if getID() == 0:
        await ctx.send("There is no welcome message.")
        return
    
    fetchedwelcome = await ctx.fetch_message(getID())
    await fetchedwelcome.edit(content=welcomemsg)
    
    await root.reactwith(fetchedwelcome, ctx.guild)


@bot.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, id):
    await ctx.send("Set welcome to new message.")
    writeID(id)


@bot.command()
@commands.has_permissions(administrator=True)
async def printwelcome(ctx):
    await ctx.send(getID())


@bot.command()
@commands.has_permissions(administrator=True)
async def speak(ctx, *, msg):
    await ctx.send(msg)
    await ctx.message.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def fortnite(ctx, user: discord.User, *, message="Fortnite 🤡"):
    await ctx.send("The user {}#{} has been permanently banned for {}.".format(user.name, user.discriminator, message))
    await user.send("You have been permanently banned from Ressu Gamers for {}. This ban is non-negotiable and does not expire.".format(message))
    await ctx.message.delete()
    await ctx.guild.ban(user, reason=message, delete_message_days=0)


@bot.command()
@commands.has_permissions(administrator=True)
async def pingkids(ctx):
    await ctx.message.delete()
    for kid in ctx.guild.members:
        if len(kid.roles) == 1:
            await kid.send(welcomedm)

    await ctx.send("DMed all members with no role.")


@bot.command()
@commands.has_permissions(administrator=True)
async def moveall(ctx, tovc: discord.VoiceChannel = None, fromvc: discord.VoiceChannel = None):
    await ctx.message.delete()
    if fromvc == None:
        fromvc = ctx.author.voice.channel
    if tovc == None:
        tovc = discord.utils.get(ctx.guild.voice_channels, name="General")
    if fromvc == None or tovc == None:  # we go agane
        await ctx.send("Invalid command. Try joining a voice channel. Usage: =moveall [tovc] [fromvc]")
        return
    
    for member in fromvc.members:
        await member.move_to(tovc)


@bot.command(aliases=["sd"])
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await ctx.send("Bye bye")
    await bot.close()


@bot.command()
async def ping(ctx):
    """Test the bot"""
    await ctx.send("Pong")


@bot.command()
@commands.cooldown(1, 7.5)
async def solve(ctx, *, query):
    """Solve mathematical equations and other stuff"""
    
    eastereggs = {"e^pi":"9","e^π":"9",
    "my life":"go study math","world hunger":"make sure to eat!!",
    "corona":"eat HONEY and WILD MUSHROOM","racism":"ahhhhhh please be nice :<",
    "life":"go study math","bullying":"why you do that? stop",
    "poverty":"your grandpa give you one million euro AND bill gates is your neighbour AND you win lottery"}
    if query.lower() in eastereggs:
        await ctx.send(eastereggs[query.lower()])
        return

    async with ctx.channel.typing():
        res = wolframclient.query(query)
        it = 1
        maximages = 2
        try:
            for pod in res["pod"]:
                if it > maximages:
                    return
                it += 1

                await ctx.send("**{}**".format(pod["@title"]))
                if type(pod["subpod"]) == list:  # Multiple images in pod
                    for subp in pod["subpod"]:
                        await ctx.send(subp["img"]["@src"])                    
                else:
                    await ctx.send(pod["subpod"]["img"]["@src"])
        except:
            try:  # Try to display only text, in case something went wrong with images
                await ctx.send("**Input interpretation:** `{}`\n**Result:**{}".format(query, next(res.results).text))
            except:
                await ctx.send("**Input interpretation:** `{}`\nUh oh, something wrong.".format(query))


@solve.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandOnCooldown):
        msg = f"{ctx.message.author.mention} This command was used {error.cooldown.per - error.retry_after:.2f}s ago and is on cooldown. Try again in {error.retry_after:.2f}s."
        await(await ctx.send(msg)).delete(delay=3)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"Usage: `=solve <query>`")
    else:
        raise(error)


if __name__ == "__main__":
    TOKEN = os.environ['token']
    game_presence.start()
    bot.run(TOKEN)
