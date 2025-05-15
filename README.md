# ZeroTTS Bot

A Telegram bot that generates speech audio from user text using ElevenLabs TTS API.

## Features

- Voice selection from available ElevenLabs voices
- Speech generation from text input
- Voice message reply in Telegram
- Logging to both console and log files (`bot.log` and `errors.log`)

## Requirements

- Python 3.11+
- ElevenLabs API key
- Telegram bot token

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ZeroTTS-Bot.git
   cd ZeroTTS-Bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `config.py` with your credentials:
   ```python
   elevenlabs_api_key = "your_elevenlabs_api_key"
   bot_token = "your_telegram_bot_token"
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

## Notes

- This bot uses the synchronous `pyTelegramBotAPI` library.
- Error logs are stored in `errors.log`.

## License

MIT
