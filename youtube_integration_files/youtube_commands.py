from youtube_integration_files.youtube_integration import *
from voicechat_integration_files.voicechat_integration import listen_to_voice
from common import bot

@bot.command()
async def playM(ctx, *, ytvideo: str = None):
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("Please connect to a voice channel to use this command.")
            return
    
    if ytvideo is None:
        await ctx.send("Please provide a youtube video name or url.")
        return

    await play_music(ctx, ytvideo, bot)
    asyncio.create_task(listen_to_voice(ctx))


@bot.command()
async def pauseM(ctx):
    pause_the_music(ctx)

@bot.command()
async def resumeM(ctx):
    resume_the_music(ctx)

@bot.command()
async def stopM(ctx):
    stop_music(ctx)
    asyncio.create_task(listen_to_voice(ctx))

@bot.command()
async def skipM(ctx):
    skip_a_song(ctx)
    asyncio.create_task(listen_to_voice(ctx))

@bot.command()
async def showQ(ctx):
    await ctx.send(get_music_queue(ctx))

@bot.command()
async def clearQ(ctx):
    clear_music_queue()
    await ctx.send("Queue has been cleared.")

@bot.command()
async def replayM(ctx):
    replay_a_song(ctx)
    asyncio.create_task(listen_to_voice(ctx))

@bot.command()
async def skipto(ctx, seconds: int):
    await skip_to_time_in_music(ctx, seconds, bot)
    asyncio.create_task(listen_to_voice(ctx))

@bot.command()
async def forward(ctx, seconds: int):
    await forward_by_seconds(ctx, seconds, bot)
    asyncio.create_task(listen_to_voice(ctx))

@bot.command()
async def changeVolume(ctx, volume: float):
    set_volume_in_settings(volume)
    restore_music_volume(ctx)
    await ctx.send("Volume changed to " + str(volume))

@bot.command()
async def getVolume(ctx):
    volume = get_volume_from_settings()
    await ctx.send("Volume is " + str(volume))