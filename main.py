import discord
import requests
from discord.ext import commands
from discord import file
from discord.utils import get
import os

client = commands.Bot(command_prefix='Bot_Prefix')

@client.command()
@commands.cooldown(1, 300, commands.BucketType.user)
@commands.has_any_role("Customer")
async def whitelist(ctx, game: int):
  
  discID = ctx.author.id
  
  r = requests.get(f"Website_Link_Here/data.php?disc={discID}&game={game}")
  result = r.text
  
  if result == 'Success':
       message = (f"Your Game Has Been Successfully Whitelisted!")
       embedVar = discord.Embed(title=message, color=0x00ff00)
       await ctx.channel.send(embed=embedVar)
  else:
       message = (f"That Game ID Is Already Whitelisted!")
       embedVar = discord.Embed(title=message, color=0xFF0000)
       await ctx.channel.send(embed=embedVar)
  
@client.command()
@commands.cooldown(1, 300, commands.BucketType.user)
@commands.has_any_role("Customer")
async def delete(ctx, game: int):
  
  discID = ctx.author.id
  b = requests.get(f"Website_Link_Here/delete.php?game={game}&disc={discID}")
  
  bList = b.text
  
  if bList == 'Invalid DiscordID':
      message = (f"You Do Not Own This Game!")
      embedVar = discord.Embed(title=message, color=0xFF0000)
      await ctx.channel.send(embed=embedVar)
  if bList == 'Invalid Game ID':
      message = (f"Game ID Is Not Listed In Database!")
      embedVar = discord.Embed(title=message, color=0xFF0000)
      await ctx.channel.send(embed=embedVar)
  else:
      if bList == 'Success':
          message = (f"Game ID Successfully Deleted!")
          embedVar = discord.Embed(title=message, color=0x00ff00)
          await ctx.channel.send(embed=embedVar)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Whitelist Bot | Louie'))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        message = (f"You Can Use This Command Again In **{round(error.retry_after, 2)}** Seconds!")
        embedVar = discord.Embed(title=message, color=0xFF0000)
        await ctx.channel.send(embed=embedVar)
    elif isinstance(error, commands.MissingRequiredArgument):
        message = (f"Please Give Me The Game ID!")
        embedVar = discord.Embed(title=message, color=0xFF0000)
        await ctx.channel.send(embed=embedVar)
    elif isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
        message = (f"You Don't Have The Customer Role!")
        embedVar = discord.Embed(title=message, color=0xFF0000)
        await ctx.channel.send(embed=embedVar)
    elif isinstance(error, commands.CommandNotFound):
        message = (f"Command Not Found!")
        embedVar = discord.Embed(title=message, color=0xFF0000)
        await ctx.channel.send(embed=embedVar)
    elif isinstance(error, commands.BadArgument):
        message = (f"Game ID Must Be A Number!")
        embedVar = discord.Embed(title=message, color=0xFF0000)
        await ctx.channel.send(embed=embedVar)
       
client.run(os.environ['token'])