import logging
from elevenlabs import save
from elevenlabs.client import ElevenLabs
from elevenlabs.core.api_error import ApiError
import config

logger = logging.getLogger(__name__)
error_logger = logging.getLogger("errors")

# Проверка API ключа сразу при создании клиента
client = ElevenLabs(api_key=config.elevenlabs_api_key)

def get_all_voices():
    try:
        voices = client.voices.get_all()
        logger.info("Fetched all voices")
        return [{'name': v.name, 'id': v.voice_id} for v in voices.voices]
    except ApiError as e:
        error_logger.error(f"Ошибка получения голосов: {e}")
        return []

def generate_audio(text: str, voice_id: str):
    try:
        audio = client.generate(
            text=text,
            voice=voice_id,
            model="eleven_multilingual_v2"
        )
        filename = "audio.mp3"
        save(audio, filename)
        logger.info(f"Audio saved to {filename}")
        return filename
    except ApiError as e:
        error_logger.error(f"Ошибка генерации аудио: {e}")
        raise
