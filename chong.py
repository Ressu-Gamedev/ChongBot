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
    
<:development:613412002479734813> - Game Development

<:smashball:614108654249050123> - Smash Bros
<:mario:745352948229603389> - Mario Kart
<:isabelle:745353571263971411> - Animal Crossing
<:nnid:614109123373694988> - Other Nintendo Games

<:csgo:614108639392825364> - CS:GO
<:ffxiv:614108647840153640> - FFXIV (and other MMOs)
<:league:614108654949367808> - League of Legends + TFT
<:creeper:614108636230451211> - Minecraft
<:osu:618694109032349705> - Osu!
<:ow:614108644736368659> - Overwatch
<:propeller:745352948304838767> - Among Us
<:r6s:745352944613851136> - Rainbow Six: Siege
<:rocketleague:745354308660363397> - Rocket League
<:valorant:745352946782306384> - Valorant
<:VR:745352948305100821> - VR Games
<:wow:618712696509956107> - World of Warcraft

<:fortnite:618689756477521920> - Fortnite

<:questionblock:618688348118319124> - Other Games
<:ipsism:613414843734818836> - NSFW ||haha, as if||

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
FORTNITE IS BANNED.

You may rejoin the server using the permanent invite link: https://discord.gg/A635RGS
"""

rolelist = {  # {emote1ID : [role1ID, role2ID, ...], ...}
    613412002479734813 : [    # Development
        612573197220577282,  # Game Developer
    ],
    614108654249050123 : [    # Smash
        613426397171679272,  # Gamer
        614067814084509697,  # Nintendo
        614067488220512256,  # Smash
    ],
    745352948229603389 : [    # Mario
        613426397171679272,  # Gamer
        614067814084509697,  # Nintendo
        745343102495096984,  # Mario Kart
    ],
    745353571263971411 : [    # Isabelle
        613426397171679272,  # Gamer
        614067814084509697,  # Nintendo
        745350491457978479,  # Animal Crossing
    ],
    614108644736368659 : [    # Overwatch
        613426397171679272,  # Gamer
        614066924414042123,  # Overwatch
    ],
    614108639392825364 : [    # CS:GO
        613426397171679272,  # Gamer
        614067014037667851,  # CS:GO
    ],
    614108647840153640 : [    # FFXIV
        613426397171679272,  # Gamer
        614067221144272896,  # FFXIV
    ],
    614108654949367808 : [    # League
        613426397171679272,  # Gamer
        614066826925572097   # League 
    ],
    614108636230451211 : [    # Creeper
        613426397171679272,  # Gamer
        614067866609778708,  # Minecraft
    ],
    618694109032349705 : [    # Osu
        613426397171679272,  # Gamer
        618693820778938369,  # Osu!
    ],
    745352948305100821 : [    # VR
        613426397171679272,  # Gamer
        745343430833471598,  # VR
    ],
    745352948304838767 : [    # Propeller
        613426397171679272,  # Gamer
        745342888774336512,  # Among Us
    ],
    745352944613851136 : [    # R6S
        613426397171679272,  # Gamer
        745349350984515775,  # Rainbow Six: Siege
    ],
    745352946782306384 : [    # Valorant
        613426397171679272,  # Gamer
        745349550516207739,  # Valorant
    ],
    745354308660363397 : [    # Rocket league
        613426397171679272,  # Gamer
        745349484652789861,  # Rocket League
    ],
    618712696509956107 : [    # WOW
        613426397171679272,  # Gamer
        618713078204334081,  # World of Warcraft
    ],
    618689756477521920 : [    # Fortnite
                             # Nothing, as it kicks the user
    ],
    618688348118319124 : [    # Mouse (Other Games)
        613426397171679272,  # Gamer
    ],
    614109123373694988 : [    # NNID (Other Nintendo)
        613426397171679272,  # Gamer
        614067814084509697,  # Nintendo
    ],
    613414843734818836 : [    # Ipsism
        612736383022530589,  # p
    ],
}


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
    if not data.emoji.id in rolelist:
        return
    
    guild = await bot.fetch_guild(data.guild_id)
    user = await guild.fetch_member(data.user_id)
    
    await user.add_roles(*[guild.get_role(id) for id in rolelist[data.emoji.id]])
    
    if data.emoji.id == 618689756477521920:  # Fortnite kick
        await user.send(kickdm)
        general = bot.get_channel(613436762257358878)
        await general.send("@{}#{} was kicked from the server for playing Fortnite.".format(user.name, user.discriminator))
        await user.kick()


@bot.event
async def on_raw_reaction_remove(data):
    if not data.message_id == getID():
        return
    if data.user_id == bot.user.id:
        return
    if not data.emoji.id in rolelist:
        return
    
    guild = await bot.fetch_guild(data.guild_id)
    user = await guild.fetch_member(data.user_id)
    
    await user.remove_roles(*[guild.get_role(id) for id in rolelist[data.emoji.id]])


@bot.event
async def on_member_join(member):
    await member.send(welcomedm)
    general = bot.get_channel(613436762257358878)
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
    
    for emote in rolelist.keys():
        await sent.add_reaction(await ctx.message.guild.fetch_emoji(emote))


@bot.command()
@commands.has_permissions(administrator=True)
async def nowelcome(ctx):
    await ctx.message.delete()
    if getID() == 0:
        await ctx.send("There is already no welcome message.")
        return
    
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
    
    for emote in rolelist.keys():
        await fetchedwelcome.add_reaction(await ctx.message.guild.fetch_emoji(emote))


@bot.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, id):
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
@commands.cooldown(1, 7)
async def solve(ctx, *, query):
    """Solve mathematical equations and other stuff"""
    
    eastereggs = {"my life":"go study math","world hunger":"make sure to eat!!",
    "corona":"eat HONEY and WILD MUSHROOM","racism":"ahhhhhh be nice",
    "life":"go study math",
    "poverty":"your grandpa give you one million euro AND bill gates is your neighbour AND you win lottery"}
    if query.lower() in eastereggs:
        await ctx.send(eastereggs[query.lower()])
        return

    async with ctx.channel.typing():
        res = wolframclient.query(query)
        it = 1
        maximages = 2
        try:
            try:
                for pod in res["pod"]:
                    if it > maximages:
                        return
                    it += 1

                    await ctx.send("**{}**".format(pod["@title"]))
                    if type(pod["subpod"]) == list:  # Multiple images in pod
                        imgs = [subp["img"]["@src"] for subp in pod["subpod"]]
                        await ctx.send("\n".join(imgs))
                    else:
                        await ctx.send(pod["subpod"]["img"]["@src"])
            except KeyError:
                await ctx.send("**Input interpretation:** `{}`\n**Result:**{}".format(query, next(res.results).text))
        except (AttributeError, StopIteration):
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
