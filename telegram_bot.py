import time

import telebot

from constants import OutPutMessages, UserState
from pdf_merger import PDFMergerUtil
from sqlite_utils import SqliteQueryUtils


class BotConfiguration:
    def __init__(self):
        self.bot_token = BotConfiguration.load_bot_token()
        self.bot = telebot.TeleBot(self.bot_token)

    @classmethod
    def load_bot_token(cls):
        from decouple import config
        return config('TELEGRAM_BOT_API_TOKEN')


print('running bot:')
conf = BotConfiguration()
database_utils = SqliteQueryUtils()
content_types = ['document']


@conf.bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    conf.bot.send_message(chat_id=chat_id, text=OutPutMessages.start_message)


@conf.bot.message_handler(commands=['about_us'])
def about_us_message(message):
    chat_id = message.chat.id
    conf.bot.send_message(chat_id=chat_id, text=OutPutMessages.about_us)


@conf.bot.message_handler(commands=['merge'])
def pdf_merge_request(message):
    chat_id = message.chat.id
    username = message.chat.username
    database_utils.change_user_state(username, UserState.WAITING_TO_RECEIVE_PDF_FILE.value)
    conf.bot.send_message(chat_id=chat_id, text=OutPutMessages.pdf_merge_request)


@conf.bot.message_handler(commands=['done'])
def pdf_merge_request(message):
    chat_id = message.chat.id
    username = message.chat.username
    file_ids = database_utils.get_user_pdf_file_ids(username)
    if file_ids != [""]:
        database_utils.change_user_state(username, UserState.DONE.value)
        conf.bot.send_message(chat_id=chat_id, text=OutPutMessages.merging)
        import requests
        file_paths = []
        for file_id in file_ids:
            file_details = conf.bot.get_file(file_id)
            file_url = f"https://api.telegram.org/file/bot{conf.bot_token}/{file_details.file_path}"
            r = requests.get(file_url, allow_redirects=True)
            file_name = f'{file_id}.pdf'
            with open(file_name, 'wb') as file:
                file.write(r.content)
                file_paths.append(file_name)
        result_file_name = f'merged.pdf'
        PDFMergerUtil.merge(file_paths, result_file_name)
        time.sleep(10)
        with open(result_file_name, 'rb') as merged_file:
            conf.bot.send_document(chat_id=chat_id, document=merged_file)
    else:
        conf.bot.send_message(chat_id=chat_id, text=OutPutMessages.no_file)


@conf.bot.message_handler(content_types=content_types)
def handle_pdf_receive(message):
    chat_id = message.chat.id
    username = message.chat.username
    database_utils.add_file_id_for_merge(username, message.document.file_id)
    conf.bot.send_message(chat_id=chat_id, text=OutPutMessages.got_it)


conf.bot.polling(none_stop=True, interval=10, timeout=1000)
