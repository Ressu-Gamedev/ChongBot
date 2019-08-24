import os, discord, json
from discord.ext import commands

bot = commands.Bot(command_prefix='*')

welcomemsg = \
"""
This server has multiple roles you can freely enable and disable.
Some roles will give you access to their respective channels.
Choose the roles you want by reacting to this message:
    
<:development:613412002479734813> - Game Development

<:smashball:614108654249050123> - Smash Bros
<:ow:614108644736368659> - Overwatch
<:csgo:614108639392825364> - CS:GO
<:ffxiv:614108647840153640> - FFXIV
<:league:614108654949367808> - League of Legends
<:tft:614108654282604567> - League + TFT
<:creeper:614108636230451211> - Minecraft

<:mouse:613413242198294528> - Other PC Games
<:nnid:614109123373694988> - Other Nintendo Games
<:joycons:613412120964366342> - Other Console Games
<:ipsism:613414843734818836> - NSFW

All roles will also give you their sub-roles (e.g. Overwatch will give you the Gamer, PC Gamer, and Overwatch roles)
Have fun!
"""
welcomedm = \
"""
Welcome to the Ressu Gamedev/eSports/Gaming Discord!
Check the <#613446760563474442> channel to get your roles and access new channels.
Please also set your server nickname to your real name, so that everyone gets to know each other.

Game on!
ChongBot:tm:
"""

rolelist = {                 # {emote1ID : [role1ID, role2ID, ...], ...}
    613412002479734813 : [   # Development
        612573197220577282,   # Game Developer
    ],
    614108654249050123 : [   # Smash
        613426397171679272,  # Gamer
        612573407338561546,   # Console Gamer
        614067814084509697,   # Nintendo
        614067488220512256,   # Smash
    ],
    614108644736368659 : [   # Overwatch
        613426397171679272,  # Gamer
        612573326593884160,   # PC Gamer
        614066924414042123,   # Overwatch
    ],
    614108639392825364 : [   # CS:GO
        613426397171679272,  # Gamer
        612573326593884160,   # PC Gamer
        614067014037667851,   # CS:GO
    ],
    614108647840153640 : [   # FFXIV
        613426397171679272,  # Gamer
        612573326593884160,   # PC Gamer
        614067221144272896,   # FFXIV
    ],
    614108654949367808 : [   # League
        613426397171679272,  # Gamer
        612573326593884160,   # PC Gamer
        614066826925572097   # League 
    ],
    614108654282604567 : [   # TFT
        613426397171679272,  # Gamer
        612573326593884160,   # PC Gamer
        614066826925572097,   # League
        614067306750017559,   # TFT
    ],
    614108636230451211 : [   # Creeper
        613426397171679272,  # Gamer
        612573326593884160,   # PC Gamer
        614067866609778708,   # Minecraft
    ],
    613413242198294528 : [   # Mouse (Other PC Gamer)
        613426397171679272,  # Gamer
        612573326593884160,   # PC Gamer
    ],
    613412120964366342 : [   # Joycons (Other Console Gamer)
        613426397171679272,  # Gamer
        612573407338561546,   # Console Gamer
    ],
    614109123373694988 : [   # NNID (Other Nintendo)
        613426397171679272,  # Gamer
        612573407338561546,   # Console Gamer
        614067814084509697,   # Nintendo
    ],
    613414843734818836 : [   # Ipsism
        612736383022530589,   # p
    ],
}


def writeID(id):
    os.environ["welcomeid"] = str(id)


def getID():
    return int(os.environ["welcomeid"])


@bot.event
async def on_ready():
    if not "WELCOMEID" in os.environ:
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
    member.send(welcomedm)


@bot.command()
@commands.has_permissions(administrator=True)
async def welcome(ctx):
    if not getID() == 0:
        await ctx.message.channel.send("There already exists a welcome message. Remove it first with *nowelcome.")
        return
    
    sent = await ctx.message.channel.send(welcomemsg)
    await ctx.message.delete()
    writeID(sent.id)
    
    for emote in rolelist.keys():
        await sent.add_reaction(await ctx.message.guild.fetch_emoji(emote))


@bot.command()
@commands.has_permissions(administrator=True)
async def pingkids(ctx):
    for kid in ctx.guild.members:
        if len(kid.roles) == 1:
            await kid.send(welcomedm)


@bot.command()
@commands.has_permissions(administrator=True)
async def nowelcome(ctx):
    if getID() == 0:
        await ctx.message.channel.send("There is already no welcome message.")
        return
    
    writeID(0)


@bot.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, id):
	writeID(id)


@bot.command()
@commands.has_permissions(administrator=True)
async def printwelcome(ctx):
    await ctx.message.channel.send(getID())


@bot.command()
@commands.has_permissions(administrator=True)
async def speak(ctx, *, msg):
    await ctx.message.channel.send(msg)
    await ctx.message.delete()


@bot.command(aliases=["sd"])
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await bot.close()


if __name__ == "__main__":
    TOKEN = os.environ['token']
    bot.run(TOKEN)