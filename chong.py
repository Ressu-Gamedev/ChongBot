import os, discord, json
from discord.ext import commands

bot = commands.Bot(command_prefix='*')

welcomemsg = \
"""
This server has multiple roles you can freely enable and disable.
These roles will give you access to their respective channels.
Choose the roles you want by reacting to this message:
    
<:development:613412002479734813> - Game Development
<:mouse:613413242198294528> - PC gamer
<:joycons:613412120964366342> - Console Gamer
<:ipsism:613414843734818836> - NSFW

More roles (including per-game roles) will be added later as needed. Have fun!
"""
welcomedm = \
"""
Welcome to the Ressu Gamedev/eSports/Gaming Discord!
Check the <#613446760563474442> channel to get your roles and access new channels.
Please also set your server nickname to your real name.

Game on!
ChongBot:tm:
"""
welcomeid = 0


def writeID():
    with open("welcome.id", "w+") as f:
        f.write(str(welcomeid))


@bot.event
async def on_ready():
    global welcomeid
    
    try:
        open("welcome.id", "x").close()
    except:
        pass
    
    with open("welcome.id", "r+") as f:
        welcomeid = f.read()
        if welcomeid == "":
            welcomeid = 0
        else:
            welcomeid = int(welcomeid)
    
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
    global welcomeid
    if message.id == welcomeid:
        welcomeid = 0
    writeID()


@bot.event
async def on_raw_reaction_add(data):
    if not data.message_id == welcomeid:
        return
    if data.user_id == bot.user.id:
        return
    
    guild = await bot.fetch_guild(data.guild_id)
    user = await guild.fetch_member(data.user_id)
    
    if data.emoji.id == 613412002479734813:  # Development
        await user.add_roles(guild.get_role(612573197220577282))  # Game Developer
    elif data.emoji.id == 613413242198294528:  # Mouse
        await user.add_roles(guild.get_role(613426397171679272))  # Gamer
        await user.add_roles(guild.get_role(612573326593884160))  # PC Gamer
    elif data.emoji.id == 613412120964366342:  # Joycons
        await user.add_roles(guild.get_role(613426397171679272))  # Gamer
        await user.add_roles(guild.get_role(612573407338561546))  # Console Gamer
    elif data.emoji.id == 613414843734818836:  # Ipsism
        await user.add_roles(guild.get_role(612736383022530589))  # p


@bot.event
async def on_raw_reaction_remove(data):
    if not data.message_id == welcomeid:
        return
    
    guild = await bot.fetch_guild(data.guild_id)
    user = await guild.fetch_member(data.user_id)
    
    if data.emoji.id == 613412002479734813:  # Development
        await user.remove_roles(guild.get_role(612573197220577282))  # Game Developer
    elif data.emoji.id == 613413242198294528:  # Mouse
        await user.remove_roles(guild.get_role(613426397171679272))  # Gamer
        await user.remove_roles(guild.get_role(612573326593884160))  # PC Gamer
    elif data.emoji.id == 613412120964366342:  # Joycons
        await user.remove_roles(guild.get_role(613426397171679272))  # Gamer
        await user.remove_roles(guild.get_role(612573407338561546))  # Console Gamer
    elif data.emoji.id == 613414843734818836:  # Ipsism
        await user.remove_roles(guild.get_role(612736383022530589))  # p


@bot.command()
@commands.has_permissions(administrator=True)
async def welcome(ctx):
    global welcomeid
    if not welcomeid == 0:
        await ctx.message.channel.send("There already exists a welcome message. Remove it first with *nowelcome.")
        return
    
    sent = await ctx.message.channel.send(welcomemsg)
    welcomeid = sent.id
    writeID()
    
    await sent.add_reaction(await ctx.message.guild.fetch_emoji(613412002479734813))
    await sent.add_reaction(await ctx.message.guild.fetch_emoji(613413242198294528))
    await sent.add_reaction(await ctx.message.guild.fetch_emoji(613412120964366342))
    await sent.add_reaction(await ctx.message.guild.fetch_emoji(613414843734818836))


@bot.command()
@commands.has_permissions(administrator=True)
async def pingkids(ctx):
	for kid in ctx.guild.members:
		if kid.roles == []:
			await kid.create_dm()
			await kid.dm_channel.send(welcomedm)


@bot.command()
@commands.has_permissions(administrator=True)
async def nowelcome(ctx):
    global welcomeid
    if welcomeid == 0:
        await ctx.message.channel.send("There is already no welcome message.")
        return
    
    welcomeid = 0
    writeID()


@bot.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, id):
	global welcomeid
	welcomeid = int(id)
	writeID()


@bot.command()
@commands.has_permissions(administrator=True)
async def speak(ctx, *, msg):
    await ctx.message.channel.send(msg)
    await ctx.message.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await bot.close()


if __name__ == "__main__":
    TOKEN = os.environ['token']
    bot.run(TOKEN)