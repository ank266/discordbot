from ai_integration_files.ai_integration import *
from common import bot


@bot.command()
async def askGem(ctx, question:str):
    response = gemini_AI_Response(question)
    await ctx.reply(response)

@bot.command()
async def clearHistory(ctx):
    clear_AI_Chat_History()
    await ctx.reply("Cleared History.")