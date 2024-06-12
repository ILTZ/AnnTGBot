import BotSrc.BotData as BotData
import BotSrc.Messages as Messages

import telebot
from telebot import types

TG_ART_BOT = telebot.TeleBot(BotData.TG_TOKEN)

########################################################################### {
@TG_ART_BOT.message_handler(commands=['start'])
def StartMessage(message):    

    # markup = types.InlineKeyboardMarkup()    
    # btnReg = types.InlineKeyboardButton("Регистрация", callback_data="Register")    

    markup = types.ReplyKeyboardMarkup()    
    btnReg = types.KeyboardButton("Регистрация")    

    markup.add(btnReg)
    
    TG_ART_BOT.send_message(message.from_user.id, Messages.WELCOME_MESSAGE, reply_markup=markup)    
########################################################################### }

def ToMainMenu(message):

    markup          = types.ReplyKeyboardMarkup(resize_keyboard=True)

    profile         = types.KeyboardButton("Мой профиль")
    galery          = types.KeyboardButton("Моя галерея")
    artistSearch    = types.KeyboardButton("Найти художника")
    reviews         = types.KeyboardButton("Мои отзывы")
    pictureLine     = types.KeyboardButton("Начать просмотр")

    markup.row(profile, galery)
    markup.row(artistSearch, reviews)
    markup.row(pictureLine)    

    TG_ART_BOT.send_message(message.from_user.id, Messages.PROFILE_MESSAGE, reply_markup=markup)    

def ToProfileInfo(message):
    
    markup      = types.ReplyKeyboardMarkup(resize_keyboard=True)

    redactInfo  = types.KeyboardButton("Редактировать")
    back        = types.KeyboardButton("Главное меню")

    markup.row(redactInfo)
    markup.row(back)
    
    TG_ART_BOT.send_message(message.from_user.id, Messages.PROFILE_INFO_MESSAGE, reply_markup=markup)    

def ToPictureLine(message):

    markup  = types.ReplyKeyboardMarkup(resize_keyboard=True)

    next    = types.KeyboardButton("Следующий рисунок")
    ranking = types.KeyboardButton("Оценить рисунок")
    back    = types.KeyboardButton("Главное меню")

    markup.add(next, ranking, back)
        
    TG_ART_BOT.send_message(message.from_user.id, "PictureInfo", reply_markup=markup)

def ToGalery(message):

    markup      = types.ReplyKeyboardMarkup(resize_keyboard=True)    
    back        = types.KeyboardButton("Главное меню")

    markup.add(back)

    TG_ART_BOT.send_message(message.from_user.id, "PictureInfo", reply_markup=markup)    

def ToArtistSearch(message):
    pass

def ToReview(message):

    markup  = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back    = types.KeyboardButton("Главное меню")

    markup.add(back)

    TG_ART_BOT.send_message(message.from_user.id, "Review", reply_markup=markup)    

########################################################################### {
@TG_ART_BOT.message_handler(content_types=['text'])
def ButtonsHandler(message):
    if message.text == 'Регистрация':     
        msg = TG_ART_BOT.send_message(message.from_user.id, Messages.GET_PROFILE_INFO_MESSAGE)           
        TG_ART_BOT.register_next_step_handler(msg, GetProfileInfo)             

    elif message.text == "Главное меню":
        ToMainMenu(message)

    elif message.text == "Мой профиль":
        ToProfileInfo(message)                

    elif message.text == "Моя галерея":
        ToGalery(message)
        
    elif message.text == "Найти художника":
        ToArtistSearch(message)        

    elif message.text == "Мои отзывы":
        ToReview(message)        

    elif (message.text == "Начать просмотр") or (message.text == "Следующий рисунок"):
        ToPictureLine(message)                
    
    else:
        TG_ART_BOT.send_message(message.from_user.id, "Некорректная команда")
########################################################################### }

########################################################################### User register process {
def GetProfileInfo(message):

    msg = TG_ART_BOT.send_message(message.from_user.id, Messages.GET_BIRTHDAY_MESSAGE)    
    TG_ART_BOT.register_next_step_handler(msg, GetBirthday)    

def GetBirthday(message):

    msg = TG_ART_BOT.send_message(message.from_user.id, Messages.GET_CONTENT_MARK)    
    TG_ART_BOT.register_next_step_handler(msg, GetRcontent)    

def GetRcontent(message):


    ToMainMenu(message)

########################################################################### User register process }




    


