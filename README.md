# Discord Whisper Bot

Um bot Discord que transcreve conversas de voz em tempo real usando OpenAI Whisper e gera resumos com GPT-4.

## Funcionalidades

- 🎙️ Gravação de áudio em canais de voz autorizados
- 📝 Transcrição automática usando OpenAI Whisper
- 📊 Geração de resumos estruturados com GPT-4
- 🔒 Controle de acesso por ID de canal
- 💾 Armazenamento temporário de transcrições por servidor

## Requisitos

- Python 3.8+
- Conta no Discord Developer Portal
- Chave de API da OpenAI
- [uv](https://github.com/astral-sh/uv) (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/discord-whisper.git
cd discord-whisper
```

2. Instale as dependências usando uv:
```bash
uv venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate  # Windows
uv pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env-example .env
```
Edite o arquivo `.env` com suas credenciais:
- `DISCORD_TOKEN`: Token do seu bot Discord
- `OPENAI_API_KEY`: Sua chave de API da OpenAI

4. Configure os IDs dos canais:
Edite `bot.py` e atualize:
- `VOICE_CHANNEL_IDS`: Lista de IDs dos canais de voz autorizados
- `SUMMARY_CHANNEL_ID`: ID do canal onde os resumos serão enviados

## Uso

1. Inicie o bot:
```bash
python bot.py
```

2. Comandos disponíveis:
- `!entrar`: Bot entra no canal de voz e começa a gravar
- `!sair`: Bot para de gravar e sai do canal
- `!resumir`: Gera um resumo das transcrições

## Estrutura do Projeto

- `bot.py`: Configuração e comandos do bot Discord
- `memory.py`: Gerenciamento de transcrições em memória
- `pcm_sink.py`: Gravação e processamento de áudio
- `transcriber.py`: Integração com OpenAI Whisper
- `summary.py`: Geração de resumos com GPT-4

## Formato do Resumo

Os resumos gerados incluem:
- Resumo geral (2-3 parágrafos)
- Principais pontos discutidos
- Action items/tarefas

## Limitações

- O bot só funciona em canais de voz autorizados
- Transcrições são mantidas apenas em memória
- Requer conexão estável com a internet
- Consome créditos da API da OpenAI

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes. 