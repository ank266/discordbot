from common import bot
from integrations import addJAVA


@bot.command()
async def java_add(ctx, num1: float, num2: float):
    await ctx.send("running")
    result = addJAVA('AddNumbers.java', num1, num2)
    await ctx.send(result)

@bot.command()
async def hello(ctx):
    await ctx.send('hello')

print("hello")