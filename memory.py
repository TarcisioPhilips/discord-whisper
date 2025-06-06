from collections import defaultdict
from typing import List

# Dictionary to store transcripts per guild
_transcripts: defaultdict[int, List[str]] = defaultdict(list)

def add_transcript(guild_id: int, text: str) -> None:
    """
    Add a transcript to the guild's transcript list.
    
    Args:
        guild_id: The Discord guild ID
        text: The transcript text to store
    """
    _transcripts[guild_id].append(text)

def pop_all_transcripts(guild_id: int) -> List[str]:
    """
    Get and clear all transcripts for a guild.
    
    Args:
        guild_id: The Discord guild ID
        
    Returns:
        List of all stored transcripts for the guild
    """
    transcripts = _transcripts[guild_id].copy()
    _transcripts[guild_id].clear()
    return transcripts

def peek_all_transcripts(guild_id: int) -> List[str]:
    """
    Get all transcripts for a guild without clearing them.
    
    Args:
        guild_id: The Discord guild ID
        
    Returns:
        List of all stored transcripts for the guild
    """
    return _transcripts[guild_id].copy() 