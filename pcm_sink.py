import os
import threading
import wave
import asyncio
import discord
from transcriber import transcribe_and_buffer, _discord_client

# Create recordings directory
RECORDINGS_DIR = "recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)

class UserPCMRecorder(discord.AudioSink):
    def __init__(self, chunk_duration: float, guild_id: int):
        """
        Initialize the PCM recorder.
        
        Args:
            chunk_duration: Duration in seconds for each transcription chunk
            guild_id: Discord guild ID
        """
        super().__init__()
        self.chunk_duration = chunk_duration
        self.guild_id = guild_id
        
        # Calculate bytes needed for chunk_duration seconds
        # 48000 samples/s × 2 bytes/sample × chunk_duration seconds
        self.chunk_size = int(48000 * 2 * chunk_duration)
        
        # Buffer to store PCM data per user
        self.buffers: dict[int, bytearray] = {}
        
    def write(self, data: discord.AudioSinkData):
        """
        Process incoming PCM data and create WAV files when enough data is collected.
        
        Args:
            data: Audio data from Discord
        """
        user_id = data.user.id
        pcm_bytes = data.pcm
        
        # Initialize buffer for new users
        if user_id not in self.buffers:
            self.buffers[user_id] = bytearray()
            
        # Append new PCM data
        self.buffers[user_id].extend(pcm_bytes)
        
        # Check if we have enough data for a chunk
        while len(self.buffers[user_id]) >= self.chunk_size:
            # Get the chunk and remove it from buffer
            chunk = self.buffers[user_id][:self.chunk_size]
            self.buffers[user_id] = self.buffers[user_id][self.chunk_size:]
            
            # Create WAV file
            thread_id = threading.get_ident()
            filename = os.path.join(RECORDINGS_DIR, f"{self.guild_id}_{user_id}_{thread_id}.wav")
            
            # Write WAV file
            with wave.open(filename, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(48000)  # 48 kHz
                wav_file.writeframes(chunk)
            
            # Start transcription in the Discord event loop
            asyncio.run_coroutine_threadsafe(
                transcribe_and_buffer(filename, user_id, self.guild_id),
                _discord_client.loop
            ) 