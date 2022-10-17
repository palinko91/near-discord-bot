import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
from datetime import datetime
from near_price import get_data

load_dotenv()

FOOTER_LOGO_URL = "https://i.imgur.com/U94yOf5.png"

bot = discord.Bot()

@bot.event
async def on_ready():
  sync_data.start()
  print(f"{bot.user} is ready and online!")

# Price update task
@tasks.loop(seconds=300)
async def sync_data():
  global near_data
  near_data = get_data() #Updating the price information
  #Converting the time to nicer format
  global timestamp
  timestamp = datetime.strptime(near_data['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z').strftime("%Y-%B-%d - %H : %M : %S")
  # Setting `Watching ` status
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Near price at {:0.2f} $".format(near_data['price'])))

# /help
@bot.slash_command(name="help", description="Access the command list")
async def help(ctx):
  embed = discord.Embed(
    title="Help",
    description="You can use the following commands with this bot:",
    color=discord.Colour.blurple(
    ),  # Pycord provides a class with default colors you can choose from
  )
  embed.add_field(
    name="/stake",
    value="The bot will help you a little how you can stake your Near!",
    inline=False)
  embed.add_field(
    name="/utility",
    value="The bot will guide you where you can find Near's utility!",
    inline=False)
  embed.add_field(name="/event",
                  value="The bot will telling you where can you find events!",
                  inline=False)
  embed.add_field(name="/market",
                  value="The bot will telling you the actual market data of Near!",
                  inline=False)
  embed.set_footer(text="Near Discord Bot", icon_url=FOOTER_LOGO_URL)

  await ctx.respond(embed=embed)


# /stake
@bot.slash_command(name="stake", description="Help for staking")
async def stake(ctx):
  embed = discord.Embed(
    title="Stake",
    description="This is a short guide which will help you with staking!",
    color=discord.Colour.blurple(
    ),  # Pycord provides a class with default colors you can choose from
  )
  embed.add_field(
    name="Where to stake?",
    value=
    "You can start staking in your Near wallet: https://wallet.near.org/staking",
    inline=False)
  embed.add_field(
    name="How to choose validator?",
    value=
    "This website is useful to choose your validator: https://near-staking.com/stats",
    inline=False)
  embed.add_field(
    name="What should I consider when I'm choosing a validator?",
    value=
    "-Make sure the fees are low, around 0-3%\n\n-The uptime is 100% or very close to it\n\n-Deleg factor is important too, make sure to choose someone who delegated Near for his own validator too!\n\nThe best practice to check least in every few weeks that your validator node is still active and not overallocated with Near and their fees are still good!",
    inline=False)
  embed.set_footer(text="Near Discord Bot", icon_url=FOOTER_LOGO_URL)
  await ctx.respond(embed=embed)


# /utility
@bot.slash_command(name="utility", description="Help for finding utility")
async def utility(ctx):
  embed = discord.Embed(
    title="Near's Utility",
    description=
    "You can explore Near's utlity if you checking out these websites!",
    color=discord.Colour.blurple(
    ),  # Pycord provides a class with default colors you can choose from
  )
  embed.add_field(
    name="Awesome Near",
    value=
    "You can find many Near projects at Awesome Near site ordered in categories: https://awesomenear.com/projects",
    inline=False)
  embed.add_field(
    name="DAOs",
    value=
    "DAO stand for Decentralized Autonomous Organization, find a DAO which suits you the best at: https://app.astrodao.com/all/daos",
    inline=False)
  embed.set_footer(text="Near Discord Bot", icon_url=FOOTER_LOGO_URL)
  await ctx.respond(embed=embed)


# /event
@bot.slash_command(name="event", description="Help for finding events")
async def event(ctx):
  embed = discord.Embed(
    title="Near Upcoming Events",
    description=
    "You can explore Near's upcoming events here: https://near.events/",
    color=discord.Colour.blurple(
    ),  # Pycord provides a class with default colors you can choose from
  )
  embed.set_footer(text="Near Discord Bot", icon_url=FOOTER_LOGO_URL)
  await ctx.respond(embed=embed)

# /market
@bot.slash_command(name="market", description="Access the market data")
async def market(ctx):
  embed = discord.Embed(
    title="Market",
    description="The latest market data is the following",
    color=discord.Colour.blurple(
    ),  # Pycord provides a class with default colors you can choose from
  )
  embed.add_field(
    name="Price",
    value="{:0.2f} $".format(near_data['price']),
    inline=True)
  embed.add_field(
    name="Price % change 24h",
    value="{:0.2f} %".format(near_data['price_change_24h']),
    inline=True)
  embed.add_field(
    name="Volume 24h",
    value=f"{int(near_data['volume_24h']):,} $",
    inline=True)
  embed.add_field(
    name="Volume change 24h",
    value="{:0.2f} %".format(near_data['volume_change_24h']),
    inline=True)
  embed.add_field(
    name="Near total supply",
    value=f"{int(near_data['total_supply']):,} Ⓝ",
    inline=True)
  embed.add_field(
    name="Near circulating supply",
    value=f"{int(near_data['circulating_supply']):,} Ⓝ",
    inline=True)
  embed.add_field(
    name="Near available supply",
    value=f"{int(near_data['total_supply'] - near_data['circulating_supply']):,} Ⓝ",
    inline=True)
  embed.add_field(
    name="Near market cap",
    value=f"{int(near_data['market_cap']):,} $",
    inline=True)
  embed.add_field(
    name="Data's taken",
    value=timestamp,
    inline=True)
  
  embed.set_footer(text="Near Discord Bot", icon_url=FOOTER_LOGO_URL)

  await ctx.respond(embed=embed)


bot.run(os.getenv('TOKEN'))  # run the bot with the token
