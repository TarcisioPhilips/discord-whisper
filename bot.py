import os
import discord
from discord.ext import commands
from pcm_sink import UserPCMRecorder
from transcriber import set_discord_client
from summary import generate_summary

# Load environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Constants
VOICE_CHANNEL_IDS = [111111111111111111]  # Example channel ID
SUMMARY_CHANNEL_ID = 222222222222222222  # Example channel ID

# Configure intents
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Set Discord client in transcriber module
set_discord_client(bot)

@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord."""
    print(f"Bot está pronto! Nome: {bot.user.name} (ID: {bot.user.id})")

@bot.command(name="entrar")
async def join_voice(ctx):
    """Join a voice channel and start recording."""
    if not ctx.author.voice:
        await ctx.send("Você precisa estar em um canal de voz primeiro.")
        return

    channel = ctx.author.voice.channel
    if channel.id not in VOICE_CHANNEL_IDS:
        await ctx.send("Este canal não está autorizado.")
        return

    # Connect to voice channel
    vc = await channel.connect()
    
    # Start recording
    recorder = UserPCMRecorder(chunk_duration=5.0, guild_id=ctx.guild.id)
    vc.start_recording(
        sink=recorder,
        callback=lambda e: print(f"Erro no recording: {e}") if e else None
    )
    
    await ctx.send(f"🔊 Bot entrou em {channel.name} e está gravando áudio.")

@bot.command(name="sair")
async def leave_voice(ctx):
    """Stop recording and leave the voice channel."""
    if ctx.voice_client:
        ctx.voice_client.stop_recording()
        await ctx.voice_client.disconnect()
        await ctx.send("Parei de gravar...")
    else:
        await ctx.send("Não estou em nenhum canal de voz agora.")

@bot.command(name="resumir")
async def summarize(ctx):
    """Generate and send a summary of the recorded transcripts."""
    summary_channel = bot.get_channel(SUMMARY_CHANNEL_ID)
    if not summary_channel:
        await ctx.send("Não encontrei o canal de resumo configurado.")
        return

    await ctx.send("⏳ Gerando resumo...")
    await generate_summary(ctx.guild.id, summary_channel)
    await ctx.send(f"✅ Resumo enviado em <#{SUMMARY_CHANNEL_ID}>")

# Run the bot
bot.run(DISCORD_TOKEN) 