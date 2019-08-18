import os, discord, json
from discord.ext import commands

bot = commands.Bot(command_prefix='*')
roles = {}

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
		return

    if message.content.lower().startswith('sigma'):
        await message.channel.send('Simba')
		
	await bot.process_commands(message)


@bot.command
async def debug(ctx):
	global roles
	print(roles)


@bot.command()
async def welcome(ctx, *, data):
	"""Creates a welcome message that will be tracked for reactions.
	Data must be passed in using the format:
	{"msg":"Message to be sent", "emoji1":"role1", "emoji2":"role2", ...}"""

	processed = json.loads(data)
	await welcome = ctx.message.channel.send(processed["msg"])
	processed.pop("msg", None)
	for emoji in processed.keys():
		await welcome.add_reaction(emoji)
	
	global roles
	roles = processed
	await ctx.message.delete()
	

@bot.command()
@commands.has_permissions(administrator=True)
async def shutdown():
	await bot.close()

if __name__ == "__main__":
	TOKEN = os.environ['token']
	bot.run(TOKEN)