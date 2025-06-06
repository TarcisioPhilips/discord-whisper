import os
import asyncio
from typing import Optional
import discord
import openai
from memory import add_transcript

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Global Discord client reference
_discord_client: Optional[discord.Client] = None

def set_discord_client(client: discord.Client) -> None:
    """
    Set the global Discord client reference.
    
    Args:
        client: The Discord client instance
    """
    global _discord_client
    _discord_client = client

async def transcribe_and_buffer(wav_path: str, user_id: int, guild_id: int) -> None:
    """
    Transcribe an audio file and buffer the result in memory.
    
    Args:
        wav_path: Path to the WAV file to transcribe
        user_id: Discord user ID who sent the audio
        guild_id: Discord guild ID where the audio was sent
    """
    try:
        # Open and transcribe the audio file
        with open(wav_path, "rb") as audio_file:
            response = await openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                response_format="json"
            )
        
        # Get the transcribed text
        text = response["text"].strip()
        
        # If we got non-empty text, add it to the buffer
        if text:
            entry = f"<@{user_id}>: {text}"
            add_transcript(guild_id, entry)
            
    except Exception as e:
        print(f"Erro ao transcrever {wav_path}: {e}")
        
    finally:
        # Clean up the WAV file
        try:
            os.remove(wav_path)
        except Exception as e:
            print(f"Erro ao remover arquivo {wav_path}: {e}") 