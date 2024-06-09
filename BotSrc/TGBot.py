from BotData import TG_TOKEN

import telebot

TG_ART_BOT = telebot.TeleBot(TG_TOKEN)

@TG_ART_BOT.message_handler(commands=['start'])
def StartMessage(message):    
    WELCOME_MESSAGE =""

    TG_ART_BOT.send_message(message.from_user.id, WELCOME_MESSAGE)    

@TG_ART_BOT.message_handler(commands="regUser")
def RegisterNewUser(message):

    pass


