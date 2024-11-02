from voicechat_integration_files.voicechat_integration import listen_to_voice, speak, stop_talking, send_text_response_to_channel
from common import bot
import asyncio
from discord.ext import voice_recv
from youtube_integration_files.youtube_integration import *
from discord.ext.voice_recv import VoiceRecvClient
import re

@bot.command(pass_context=True)
async def join(ctx, channel=None):
    if ctx.author.voice is None:
        await ctx.send("You're not in a voice channel!")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect(cls=voice_recv.VoiceRecvClient)

    asyncio.create_task(listen_to_voice(ctx))

@bot.command(name="join_automatically", pass_context=True)
async def join_automatically(ctx, channel=None):
    if channel is None:
        channel = ctx.author.voice.channel

    try:
        if ctx.voice_client is None:
            ctx.voice_client = await channel.connect(cls=VoiceRecvClient)
        elif ctx.voice_client.channel != channel:
            await ctx.voice_client.move_to(channel)
    except Exception as e:
        await send_text_response_to_channel(e)
        return

    await listen_to_voice(ctx)


@bot.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()


@bot.command()
async def ss(ctx):
    stop_talking(ctx)


async def voice_commands(ctx, text, user):
    print(text)
    if "can" in text and "leave" in text and "you" in text:
        stop_music(ctx)
        await speak(ctx, "Ok, bye!")
        await ctx.voice_client.disconnect()
    elif "can you play" in text:
        ytvideo = text.split("can you play", 1)[1].strip()
        await play_music(ctx, ytvideo, bot)
    elif "gemini" in text and "ask" in text:
        aiResponse = gemini_AI_Response(text)
        await send_text_response_to_channel(aiResponse)
        await speak(ctx, aiResponse)
    elif "stop" in text and "talking" in text and "gemini" in text:
        stop_talking(ctx)
    elif "clear" in text and "history" in text and "gemini" in text:
        clear_AI_Chat_History()
        await speak(ctx, "History cleared.")
    elif "audio" in text or "music" in text or "song" in text:
        await music_voice_commands(ctx, text)
    elif "can you disconnect me" == text or "can you kick me" == text or "can you kick me out" == text:
        await speak(ctx, "Ok, bye!")
        await user.move_to(None)
    elif "can you disconnect all users" == text or "can you disconnect all the users" == text or "can you kick all users" == text or "can you kick all the users" == text or "can you kick out all users" == text or "can you kick out all the users" == text:
        await speak(ctx, "Ok, bye everyone!")
        for member in ctx.author.voice.channel.members:
            await member.move_to(None)
    else:
        pass


async def music_voice_commands(ctx, text):
    if "pause" in text:
        pause_the_music(ctx)
    elif "resume" in text:
        resume_the_music(ctx)
    elif "stop" in text:
        stop_music(ctx)
        asyncio.create_task(listen_to_voice(ctx))
    elif "can you skip to" in text:
        time_in_seconds = extract_time_from_string(text)
        await skip_to_time_in_music(ctx, time_in_seconds, bot)
        asyncio.create_task(listen_to_voice(ctx))
    elif "skip" in text:
        skip_a_song(ctx)
        asyncio.create_task(listen_to_voice(ctx))
    elif "queue" in text and "show" in text:
        await send_text_response_to_channel(get_music_queue(ctx))
    elif "clear" in text and "queue" in text:
        clear_music_queue()
    elif "replay" in text:
        replay_a_song(ctx)
        asyncio.create_task(listen_to_voice(ctx))
    elif "can you go forward" in text:
        time_in_seconds = extract_time_from_string(text)
        await forward_by_seconds(ctx, time_in_seconds, bot)
        asyncio.create_task(listen_to_voice(ctx))
    elif ("lower" in text or "decrease" in text) and "volume" in text:
        volume = re.findall(r'\d+', text)
        volume.append(10)
        volume = int(volume[0]) / 100
        set_volume_in_settings(volume)
        restore_music_volume(ctx)
    elif "increase" in text and "volume" in text:
        volume = re.findall(r'\d+', text)
        volume.append(100)
        volume = int(volume[0]) / 100
        set_volume_in_settings(volume)
        restore_music_volume(ctx)
    else:
        pass


def extract_time_from_string(text):
    time_pattern = r'[0-9]+\shour[s]?|[0-9]+\sminute[s]?|[0-9]+\ssecond[s]?'
    matches = re.findall(time_pattern, text.lower())
    hours = minutes = seconds = 0

    for match in matches:
        value, unit = match.split()
        value = int(value)

        if 'hour' in unit:
            hours = value
        elif 'minute' in unit:
            minutes = value
        elif 'second' in unit:
            seconds = value

    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    return total_seconds