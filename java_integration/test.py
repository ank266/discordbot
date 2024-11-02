from common import bot
from java_integration.integration import addJAVA


@bot.command()
async def java_add(ctx, num1: float, num2: float):
    await ctx.send("running")
    result = addJAVA('AddNumbers.java', num1, num2)
    await ctx.send(result)