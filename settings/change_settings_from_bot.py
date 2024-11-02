from common import bot
from settings.read_write_data_storage_files import *
import discord


@bot.command()
async def joinwithme(ctx):
    add_to_users_to_join_call_with(ctx.author.id)
    await ctx.reply("You have been added.")


@bot.command()
async def hearme(ctx):
    add_to_voice_command_users(ctx.author.id)
    await ctx.reply("You have been added.")


@bot.command()
async def dontjoinwithme(ctx):
    delete_from_users_to_join_call_with(ctx.author.id)
    await ctx.reply("You have been removed.")


@bot.command()
async def donthearme(ctx):
    delete_from_voice_command_users(ctx.author.id)
    await ctx.reply("You have been removed.")


@bot.command()
async def addeditor(ctx, member: discord.Member):
    if ctx.author.id in read_editors():
        add_to_editors(member.id)
        await ctx.reply("User has been added.")
    else:
        await ctx.reply("You cannot use this command.")
