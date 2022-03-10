import telebot

from constants import OutPutMessages


class BotConfiguration:
    def __init__(self):
        self.bot_token = BotConfiguration.load_bot_token()
        self.bot = telebot.TeleBot(self.bot_token)

    @classmethod
    def load_bot_token(cls):
        from decouple import config
        return config('TELEGRAM_BOT_API_TOKEN')


conf = BotConfiguration()

content_types = ['document']


@conf.bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    conf.bot.send_message(chat_id=chat_id, text=OutPutMessages.start_message)


@conf.bot.message_handler(commands=['about_us'])
def about_us_message(message):
    chat_id = message.chat.id
    conf.bot.send_message(chat_id=chat_id, text=OutPutMessages.about_us)


@conf.bot.message_handler(content_types=content_types)
def answer_std(message):
    print(message.chat.id)
    file_details = conf.bot.get_file(message.document.file_id)
    file_url = f"https://api.telegram.org/file/bot{conf.bot_token}/{file_details.file_path}"
    print(file_url)


conf.bot.polling(none_stop=True, interval=10, timeout=1000)
