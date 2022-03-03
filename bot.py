import telebot
import time
import random
from decouple import config
BOT_TOKEN = config('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def say_hello(message):
    bot.reply_to(message, "Hello, you are using from software_eng_lab_bot. thanks for that.")



while True:
    try:
        bot.polling()
    except:
        time.sleep(15)