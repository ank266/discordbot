from common import bot
from datetime import datetime
import discord
import random
from discord.ui import Select, View
from settings.read_write_data_storage_files import read_default_channel_to_send_deleted_message_to


@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(read_default_channel_to_send_deleted_message_to())
    if(len(message.content) == 0):
        display = message.attachments[0]
    else:
        display = message.content

    embed = discord.Embed(
        title=display,
        description=message.created_at,
        color=discord.Colour.green()
    )

    embed.add_field(
        name=message.author.name,
        value='',
        inline=True
    )

    await channel.send(embed=embed)
    


@bot.event
async def on_message_edit(before, after):
    if(before.author.id == bot.user.id):
        return
    
    embed = discord.Embed(
        title="Before: "+before.content,
        description="After: "+after.content,
        color=discord.Colour.green()
    )

    embed.add_field(
        name=before.author.name,
        value='',
        inline=True
    )

    channel = bot.get_channel(read_default_channel_to_send_deleted_message_to())
    await channel.send(embed=embed)



@bot.command()
async def rewind(message,arg):
    channel = bot.get_channel(message.channel.id)
    datetime_str = arg + ' 00:00:00'
    try:
        datetime_object = datetime.strptime(datetime_str, '%d/%m/%y %H:%M:%S')

        messageAtDate = []
        async for message in channel.history(after=datetime_object):
            messageAtDate = message
            break
        
        oldmessage = await message.channel.fetch_message(messageAtDate.id)

        await oldmessage.reply("Gotchu.")
    except:
        await message.reply("It needs to be in dd/mm/yy form.")


@bot.command()
async def commands(ctx):
    embed=discord.Embed(title="Commands List", color=0x8618b9)

    embed.add_field(name="Regular commands", value="$rm = Game of guessing a who sent the random message\n$rewind dd/mm/yy = Reply to old message at that time", inline=False)
    
    embed.add_field(name="Call commands", value="$join = Join call user is in\n$leave = Leave if in call\n$ss = Stop the bot from speaking\n$vCommands = Menu with voice commands", inline=False)
    
    embed.add_field(name="Youtube commands", value="$playM link/title = Play audio in call or if already playing add song to queue\n"+
    "$pauseM = Pause the music/audio\n$resumeM = Resume the music/audio\n$stopM = Stop the music/audio and empty the queue\n"+
    "$skipM = Skip the current song and go to next in queue\n$showQ = Show queue\n$clearQ = Clear Queue\n$replayM = Replay current song\n"+
    "$skipto (seconds) = Skip to a certain point in the current song\n$forward (seconds)= Go forward in the current song by a some seconds\n"+
    "$changeVolume volume(0 to 1.0) = Adjust volume of songs\n$getVolume = Get the volume", inline=False)
    
    embed.add_field(name="AI commands", value="$askGem (question) = Ask bot question\n$clearHistory = Clear the context history", inline=False)
    
    embed.add_field(name="Voice Command Signup(Will need bot to leave and join call back)", value="$joinwithme = Enables the setting for the bot to join call when you join\n"+
    "$hearme = Allows the bot to hear you when you are in the voice chat\n$dontjoinwithme = Disable the bot joining the call with you feature\n"+
    "$donthearme = Disable the bot from hearing you in the call\n$addeditor = Add editors who can access bigger commands(use $ecommands)", inline=False)
    
    await ctx.send(embed=embed)


@bot.command()
async def ecommands(ctx):
    embed=discord.Embed(title="Commands List", color=0x8618b9)

    embed.add_field(name="Alter files(EDITORS ONLY)", value="$create_file (file name) = Create a file\n$delete_file (file name) = delete file\n" +
    "$view_file (file name) = View the File\n$append_to_file (file name) (code/text) (offset:0)\n$find_all (file name) (string to find)\n" +
    "$delete_line (file name) (string to delete) (index to delete)\n$replace (file name) (before) (after) (occurance)\n" +
    "$upload_file = Attach a file and use this command to upload it\n$rc (linux command) = run a linux terminal command\n" +
    "$stop (file name) = If running a random code and it hangs for emergencies", inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def vcommands(ctx):
    embed=discord.Embed(title="Voice Commands List", color=0x8618b9)

    embed.add_field(name="Music commands (must contain the word music or audio or song)", value="If starts with **can you play (song_name)** = Plays the song_name\nIf contains **pause** = Pause the music\n"+
    "If contains **resume** = Resume the song\nIf contains **stop** = Stop the music and clear queue\nIf **can you skip to** = Skip to a given point in the current song (Specify hours,minutes and seconds as needed)\n"+
    "If contains **skip** = Skip the current song\nIf contains **queue** and **show** = Show the current queue\nIf contains **clear** and **queue** = Clear the queue\n"+
    "If contains **replay** = Replay the current song\nIf contains **can you go forward** = go forward in the current song by a given amount (Specify hours,minutes and seconds as needed)\n"+
    "If contains **lower** or **decrease** and **volume** = lower the volume\nIf contains **increase** and **volume** = Increase the volume", inline=False)

    embed.add_field(name="General voice commands", value="If contains **can you leave** = Disconnects the bot from the voice channel\n"+
    "If is **can you disconnect me** or **can you kick me** or **can you kick me out** = Disconnect yourself from the voice channel\n"+
    "If is **can you disconnect all users** or **can you disconnect all the users** or **can you kick all users** or **can you kick the users** or **can you kick all users** or **can you kick out all the users** = Disconnect everyone from the voice channel", inline=False)

    embed.add_field(name="AI voice commands", value="If contains **ask** and **gemini** = Will ask prompt to gemini ai\n"+
    "If contains **stop** and **talking** and **gemini** = Stop the bot from talking\n"+
    "If contains **clear** and **history** and **gemini** = Clear the ai chat history", inline=False)
    
    await ctx.send(embed=embed)