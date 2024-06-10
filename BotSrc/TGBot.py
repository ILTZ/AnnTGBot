import BotSrc.BotData as BotData
import BotSrc.Messages as Messages

import telebot
from telebot import types

TG_ART_BOT = telebot.TeleBot(BotData.TG_TOKEN)

########################################################################### {
@TG_ART_BOT.message_handler(commands=['start'])
def StartMessage(message):    

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btnYes = types.KeyboardButton("Регистрация")    
    markup.add(btnYes)
    
    TG_ART_BOT.send_message(message.from_user.id, Messages.WELCOME_MESSAGE, reply_markup=markup)    
########################################################################### }

def ToMainMenu(message):

    markup          = types.ReplyKeyboardMarkup(resize_keyboard=True)

    profile         = types.KeyboardButton("Мой профиль")
    galery          = types.KeyboardButton("Моя галерея")
    artistSearch    = types.KeyboardButton("Найти художника")
    reviews         = types.KeyboardButton("Мои отзывы")
    pictureLine     = types.KeyboardButton("Начать просмотр")

    markup.add(profile, galery, artistSearch, reviews, pictureLine)

    TG_ART_BOT.send_message(message.from_user.id, Messages.PROFILE_MESSAGE, reply_markup=markup)    

def ToProfileInfo(message):
    
    markup      = types.ReplyKeyboardMarkup(resize_keyboard=True)

    redactInfo  = types.KeyboardButton("Редактировать")
    back        = types.KeyboardButton("В главное меню")

    markup.add(redactInfo, back)

    TG_ART_BOT.send_message(message.from_user.id, Messages.PROFILE_INFO_MESSAGE, reply_markup=markup)    

def ToPictureLine(message):

    markup  = types.ReplyKeyboardMarkup(resize_keyboard=True)

    next    = types.KeyboardButton("Следующий рисунок")
    ranking = types.KeyboardButton("Оценить рисунок")
    back    = types.KeyboardButton("В главное меню")

    markup.add(next, ranking, back)
        
    TG_ART_BOT.send_message(message.from_user.id, "PictureInfo", reply_markup=markup)

def ToGalery(message):
    pass

def ToArtistSearch(message):
    pass

def ToReview(message):
    pass

########################################################################### {
@TG_ART_BOT.message_handler(commands=["button"])
def RegisterNewUser(message):
    if message.text == "Регистрация":                
        TG_ART_BOT.register_next_step_handler(Messages.GET_PROFILE_INFO_MESSAGE, GetProfileInfo)             

    elif message.text == "Мой профиль":
        ToProfileInfo(message)                

    elif message.text == "Моя галерея":
        ToGalery(message)
        
    elif message.text == "Найти художника":
        ToArtistSearch(message)        

    elif message.text == "Мои отзывы":
        ToReview(message)        

    elif message.text == "Начать просмотр":
#        ToPictureLine()        
        pass

    TG_ART_BOT.send_message(message.from_user.id, "Некорректная команда")
########################################################################### }


########################################################################### User register process {
def GetProfileInfo(message):

    TG_ART_BOT.register_next_step_handler(Messages.GET_BIRTHDAY_MESSAGE, GetBirthday)    

def GetBirthday(message):

    TG_ART_BOT.register_next_step_handler(Messages.GET_CONTENT_MARK, GetRcontent)    

def GetRcontent(message):


    pass

########################################################################### User register process }




    


