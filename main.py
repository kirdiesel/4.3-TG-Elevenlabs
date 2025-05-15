import logging
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from tqdm import tqdm
import voice
import config

# Основной лог
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Лог ошибок
error_logger = logging.getLogger("errors")
fh = logging.FileHandler("errors.log", encoding="utf-8")
fh.setLevel(logging.ERROR)
error_logger.addHandler(fh)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(config.bot_token)
voices = voice.get_all_voices()

keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
for v in tqdm(voices, desc="Creating keyboard buttons"):
    keyboard.add(KeyboardButton(v["name"]))

selected_voice = {}

@bot.message_handler(commands=['start'])
def start(message):
    logger.info(f"User {message.from_user.id} started bot")
    bot.send_message(message.chat.id, "Выберите голос:", reply_markup=keyboard)

@bot.message_handler(func=lambda msg: msg.text in [v["name"] for v in voices])
def voice_chosen(message):
    selected_voice[message.from_user.id] = message.text
    logger.info(f"User {message.from_user.id} selected voice {message.text}")
    bot.send_message(message.chat.id, f"Выбран голос: {message.text}. Введите текст для озвучки.")

@bot.message_handler(func=lambda msg: True)
def synthesize(message):
    uid = message.from_user.id
    if uid in selected_voice:
        voice_id = next(v["id"] for v in voices if v["name"] == selected_voice[uid])
        logger.info(f"Generating audio for user {uid} with voice {voice_id}")
        try:
            audio_file = voice.generate_audio(message.text, voice_id)
            with open(audio_file, 'rb') as f:
                bot.send_voice(uid, f)
        except Exception as e:
            error_logger.error(f"Не удалось сгенерировать аудио: {e}")
            bot.send_message(uid, "Произошла ошибка при генерации аудио.")
    else:
        bot.send_message(message.chat.id, "Сначала выберите голос командой /start")

bot.polling(none_stop=True)
