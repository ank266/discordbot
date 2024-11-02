from discord import FFmpegPCMAudio, PCMVolumeTransformer
import yt_dlp
import discord
import asyncio
import time
from settings.read_write_data_storage_files import read_volume_from_settings, edit_volume_in_settings_file

music_queue = []
is_playing_youtube = False
current_song = None
song_start_time = None

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

async def get_audio_source(query, start_time=0):
    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
        'max_downloads': 1,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)

        if 'entries' in info:
            video = info['entries'][0]
        else:
            video = info

        audio_url = video['url']
        title = video['title']

        FFMPEG_OPTIONS['before_options'] = f'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -ss {start_time}'

        source = FFmpegPCMAudio(audio_url, executable="C:/ffmpeg/bin/ffmpeg.exe", **FFMPEG_OPTIONS)
        return PCMVolumeTransformer(source, volume=get_volume_from_settings()), title


async def play_next(ctx, bot):
    global is_playing_youtube, current_song, song_start_time

    if len(music_queue) > 0:
        is_playing_youtube = True
        current_song = music_queue.pop(0)
        
        source, title = await get_audio_source(current_song)
        
        song_start_time = time.time()
        
        ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx, bot), bot.loop))
        await ctx.send(f"Now playing: {title}")
    else:
        is_playing_youtube = False
        current_song = None
        await ctx.send("Queue is empty, stopping music.")


async def play_music(ctx, ytvideo, bot):
    global is_playing_youtube
    music_queue.append(ytvideo)

    if not is_playing_youtube:
        await play_next(ctx, bot)


def pause_the_music(ctx):
    try:
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
    except Exception as e:
        print(e)


def resume_the_music(ctx):
    try:
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
    except Exception as e:
        print(e)


def stop_music(ctx):
    global music_queue, is_playing_youtube
    music_queue.clear()

    try:
        if ctx.voice_client.is_playing() and is_playing_youtube:
            ctx.voice_client.stop()
            is_playing_youtube = False
            
    except Exception as e:
        print(e)


def clear_music_queue():
    global music_queue
    music_queue.clear()


def skip_a_song(ctx):
    try:
        if ctx.voice_client.is_playing() and is_playing_youtube:
            ctx.voice_client.stop()
    except Exception as e:
        print(e)


def get_music_queue(ctx):
    queue_list = "\n".join(music_queue)
    if len(music_queue) == 0:
        return "The queue is currently empty."
    else:
        queue_list = "\n".join(music_queue)
        return f"Current queue:\n{queue_list}"


def replay_a_song(ctx):
    global current_song, music_queue

    if current_song:
        music_queue.insert(0, current_song)

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()


async def skip_to_time_in_music(ctx, seconds, bot):
    global current_song, music_queue

    if current_song:
        music_queue.insert(0, current_song)
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            
        source, title = await get_audio_source(current_song, start_time=seconds)
        ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx, bot), bot.loop))


async def forward_by_seconds(ctx, seconds, bot):
    global current_song, music_queue, song_start_time

    if current_song:
        music_queue.insert(0, current_song)

        current_position = time.time() - song_start_time
        skip_to_time = current_position + seconds

        if skip_to_time < 0:
            skip_to_time = 0

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        source, title = await get_audio_source(current_song, start_time=skip_to_time)
        ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx, bot), bot.loop))


def adjust_music_volume(ctx, volume):
    if ctx.voice_client and ctx.voice_client.source:
        ctx.voice_client.source.volume = volume


def lower_music_volume(ctx):
    adjust_music_volume(ctx, 0.1)


def restore_music_volume(ctx):
    volume = get_volume_from_settings()
    adjust_music_volume(ctx, volume)


def get_volume_from_settings():
    volume = read_volume_from_settings()
    return volume


def set_volume_in_settings(volume):
    edit_volume_in_settings_file(volume)
