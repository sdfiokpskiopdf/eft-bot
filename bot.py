import discord
from discord.ext import commands
from wiki import Wiki

bot = commands.Bot(command_prefix="?")
wiki = Wiki()


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! In {round(bot.latency * 1000)}ms")


@bot.command()
async def lookup(ctx, term):
    d = wiki.lookup(term)
    embed = discord.Embed(title=d["title"], url=d["url"], description=d["desc"])
    embed.set_thumbnail(url=d["image"])

    for k, v in d.items():
        if k not in ["title", "url", "desc", "image"]:
            embed.add_field(name=k, value=v, inline=False)

    await ctx.send(embed=embed)


bot.run(open("token.txt", "r").read())
