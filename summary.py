import os
import openai
import discord
from memory import pop_all_transcripts

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# GPT model to use
GPT_MODEL = "gpt-4"  # or "gpt-3.5-turbo"

async def generate_summary(guild_id: int, channel: discord.TextChannel) -> None:
    """
    Generate a summary of the conversation using GPT.
    
    Args:
        guild_id: Discord guild ID
        channel: Discord text channel to send the summary to
    """
    # Get all transcripts for this guild
    transcripts = pop_all_transcripts(guild_id)
    
    # Check if we have any transcripts
    if not transcripts:
        await channel.send("📝 Não encontrei nada para resumir no momento.")
        return
    
    # Join all transcripts with newlines
    full_text = "\n".join(transcripts)
    
    # Create the prompt for GPT
    prompt = f"""Por favor, analise a seguinte conversa e gere um resumo estruturado:

{full_text}

Gere um resumo com a seguinte estrutura em Markdown:

### Resumo
[2-3 parágrafos resumindo os principais pontos da conversa]

### Principais Pontos
- [Lista de bullet points com os principais tópicos discutidos]

### Action Items
- [Lista de tarefas ou decisões que precisam ser tomadas]

Mantenha o resumo conciso e focado nos pontos mais importantes."""

    try:
        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em resumir conversas de forma clara e estruturada."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        # Extract the summary text
        summary_text = response.choices[0].message.content.strip()
        
        # Send the summary to the channel
        await channel.send(f"**Resumo da conversa:**\n{summary_text}")
        
    except Exception as e:
        await channel.send(f"❌ Erro ao gerar o resumo: {e}")
        return 