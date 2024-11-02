import discord
import sys, os, shutil, subprocess
from common import bot
from dotenv import load_dotenv
from settings.read_write_data_storage_files import read_editors
import general_commands.qol
import general_commands.file_manipulation
import java_integration.test
import voicechat_integration_files.voicechat_integration
import ai_integration_files.ai_commands
import youtube_integration_files.youtube_commands
import voicechat_integration_files.voicechat_commands
import settings.change_settings_from_bot
import general_commands.games

running_processes = {}

@bot.command()
async def restart(ctx):
    user_id = str(ctx.author.id)
    if not ctx.author.id in read_editors():
        await message.send("Not Authorized.")
        return

    await ctx.send("Restarting bot...")
    os.execv(sys.executable, ['python'] + sys.argv)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot.run(BOT_TOKEN)