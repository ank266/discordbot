import discord
from common import bot
import speech_recognition as sr
import asyncio
import gtts
import os
from ai_integration_files.ai_integration import *
from concurrent.futures import ThreadPoolExecutor
from discord.ext import voice_recv
from youtube_integration_files.youtube_integration import lower_music_volume, restore_music_volume
import wave
from settings.read_write_data_storage_files import read_voice_command_users, read_users_to_join_call_with, read_default_channel_to_message_to


recognizer = sr.Recognizer()

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

executor = ThreadPoolExecutor()

class SpeechRecognitionSink(voice_recv.AudioSink):
    def __init__(self, ctx, music_source):
        super().__init__()
        self.ctx = ctx
        self.music_source = music_source
        self.audio_buffer = b""
        self.sample_rate = 48000
        self.sample_width = 4
        self.recording_active = False
        self.target_users = read_voice_command_users()

    def wants_opus(self) -> bool:
        """Specify that we want PCM (decoded) audio."""
        return False

    def write(self, user, data):
        """Accumulate audio data only when recording is active."""
        if self.recording_active and data.pcm:
            if user.id in self.target_users:
                self.audio_buffer += data.pcm

    @voice_recv.AudioSink.listener()
    def on_voice_member_speaking_start(self, member: discord.Member):
        """Triggered when a user starts speaking."""
        lower_music_volume(self.ctx)
        if member.id in self.target_users:
            # print(f"{member.name} started speaking.")
            self.recording_active = True

    @voice_recv.AudioSink.listener()
    def on_voice_member_speaking_stop(self, member: discord.Member):
        """Triggered when a user stops speaking."""
        restore_music_volume(self.ctx)
        if member.id in self.target_users:
            # print(f"{member.name} stopped speaking.")
            self.recording_active = False

            if self.audio_buffer:
                audio_data = sr.AudioData(self.audio_buffer, self.sample_rate, self.sample_width)
                self.process_audio(member, audio_data)
                self.audio_buffer = b""


    def process_audio(self, user, audio_data):
        """Process the accumulated audio for speech recognition."""
        try:
            if audio_data.get_wav_data().strip():
                text = convert_audio_to_text_using_google_speech(audio_data)
                # print(f"Recognized from {user.name}: {text}")
                select_action_to_take_based_on_text(self.ctx, text, user)
        except sr.UnknownValueError:
            print(f"Could not understand audio from {user.name}")
        except Exception as e:
            print(f"Error processing audio from {user.name}: {e}")


    def cleanup(self):
        print("AudioSink cleanup complete.")


async def listen_to_voice(ctx):
    if ctx.voice_client:
        ctx.voice_client.listen(SpeechRecognitionSink(ctx, ctx.voice_client.source))


async def speak(ctx, message):
    try:
        convert_text_to_audio_using_gtts_and_save_file(message)
        play_the_audio_file(ctx)
        await wait_for_audio_to_finish_playing_and_remove_file(ctx)
    except Exception as e:
        print(f"Error: {e}")


def convert_audio_to_text_using_google_speech(audio):
    command_text = recognizer.recognize_google(audio)
    return command_text.lower()


def select_action_to_take_based_on_text(ctx, text, user):
    from voicechat_integration_files.voicechat_commands import voice_commands
    asyncio.run_coroutine_threadsafe(voice_commands(ctx, text, user), bot.loop)


def convert_text_to_audio_using_gtts_and_save_file(text):
    tts = gtts.gTTS(text)
    tts.save("response.mp3")


def play_the_audio_file(ctx):
    audio_source = discord.FFmpegPCMAudio("response.mp3", executable="C:/ffmpeg/bin/ffmpeg.exe")
    if not ctx.voice_client.is_playing():
        ctx.voice_client.play(audio_source)


async def wait_for_audio_to_finish_playing_and_remove_file(ctx):
    while ctx.voice_client.is_playing():
        await asyncio.sleep(1)
    os.remove("response.mp3")


def check_if_response_mp3_exists():
    return os.path.isfile('response.mp3')


def stop_talking(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing() and check_if_response_mp3_exists():
        ctx.voice_client.stop()


async def send_text_response_to_channel(message):
    channel_id = read_default_channel_to_message_to()
    channel = bot.get_channel(channel_id)
    await channel.send(message)


@bot.event
async def on_voice_state_update(member, before, after):
    from voicechat_integration_files.voicechat_commands import join_automatically
    if (member.id in read_users_to_join_call_with()) and after.channel is not None:
        try:
            class FakeContext:
                def __init__(self, guild, voice_client, author):
                    self.guild = guild
                    self.voice_client = voice_client
                    self.author = author

            ctx = FakeContext(member.guild, member.guild.voice_client, member)
            await join_automatically(ctx, after.channel)
        except Exception as e:
            print(f"Error joining the voice channel: {e}")