from BotData import TG_TOKEN

import telebot


TG_ART_BOT = telebot.TeleBot(TG_TOKEN)

@TG_ART_BOT.message_handler(commands=['start'])
def StartMessage(message):
    
    pass


