import BotSrc.BotData as BotData
import BotSrc.Messages as Messages

import telebot
from telebot import types
from DB.SQLiteDBHandler import handler
from DB.SQLiteDBHandler import UserInfo

TG_ART_BOT = telebot.TeleBot(BotData.TG_TOKEN)

PICTURE_LIMIT = 5

########################################################################### {
# Return True if user are exists
def CheckUserExists(message, userTelegramID) -> bool:

    id = handler.GetDBId(userTelegramID)

    if len(id) > 0:        
        return True
    else:                           
        msg = TG_ART_BOT.send_message(message.from_user.id, Messages.GET_PROFILE_INFO_MESSAGE)           
        TG_ART_BOT.register_next_step_handler(msg, GetProfileInfo)    

    return False


@TG_ART_BOT.message_handler(commands=['start', 'help'])
def StartMessage(message):    

    if (CheckUserExists(message.from_user.id)):
        TG_ART_BOT.send_message(message.from_user.id, Messages.BOT_DESCRIPTION)    
    else:                
        msg = TG_ART_BOT.send_message(message.from_user.id, Messages.WELCOME_MESSAGE)    
        msg = TG_ART_BOT.send_message(message.from_user.id, Messages.GET_PROFILE_INFO_MESSAGE)           
        TG_ART_BOT.register_next_step_handler(msg, GetProfileInfo)    

########################################################################### User register process {

TemporaryUserData = {}

def AddUserDescription(userID, description):
    TemporaryUserData[userID] = {}
    TemporaryUserData[userID]['Description'] = description

def AddUserBirthday(userID, birthday):
    TemporaryUserData[userID]['Birthday'] = birthday
    
def AddUserRContent(userID, agree):
    TemporaryUserData[userID]['RContent'] = agree

def AddUserUsername(userID, username):
    TemporaryUserData[userID]['Username'] = username

def GoToRegistration(message):    

    msg = TG_ART_BOT.send_message(message.from_user.id, Messages.GET_PROFILE_INFO_MESSAGE)           
    TG_ART_BOT.register_next_step_handler(msg, GetProfileInfo)    
###########################################################################################

def GetProfileInfo(message):

    AddUserDescription(message.from_user.id, message.text)
    AddUserUsername(message.from_user.id, message.from_user.username)

    msg = TG_ART_BOT.send_message(message.from_user.id, Messages.GET_BIRTHDAY_MESSAGE)    
    TG_ART_BOT.register_next_step_handler(msg, GetBirthday)    
###########################################################################################

def GetBirthday(message):

    AddUserBirthday(message.from_user.id, message.text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    y = types.KeyboardButton("Да")
    n = types.KeyboardButton("Нет")

    markup.add(y,n)

    msg = TG_ART_BOT.send_message(message.from_user.id, Messages.GET_CONTENT_MARK, reply_markup=markup)    
    TG_ART_BOT.register_next_step_handler(msg, GetRcontent)    
###########################################################################################

def GetRcontent(message):

    result = 0

    if (message.text == "Да"):
        result = 1
    elif (message.text == "Нет"):
        result = 0
    else:
        msg = TG_ART_BOT.send_message(message.from_user.id, "Данные введены некорректно")    

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        y = types.KeyboardButton("Да")
        n = types.KeyboardButton("Нет")

        markup.add(y,n)

        msg = TG_ART_BOT.send_message(message.from_user.id, Messages.GET_CONTENT_MARK, reply_markup=markup)    
        TG_ART_BOT.register_next_step_handler(msg, GetRcontent)    
        return


    AddUserRContent(message.from_user.id, result)

    ProcessUserData(message.from_user.id)

    ToMainMenu(message)
###########################################################################################

def ProcessUserData(userTelegrammID):
    handler.AddNewUser(userTelegrammID, TemporaryUserData[userTelegrammID]['Username'], TemporaryUserData[userTelegrammID]['Description'], TemporaryUserData[userTelegrammID]['Birthday'], TemporaryUserData[userTelegrammID]['RContent'], PICTURE_LIMIT)    
    del TemporaryUserData[userTelegrammID]
########################################################################### User register process }

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
    
    userID   = handler.GetDBId(message.from_user.id)
    userData = handler.GetUserInfo(userID)

    answer = Messages.FormProfileInfo(userData[UserInfo.USER_NAME], userData[UserInfo.LINKS], userData[UserInfo.REVIEW_COUNT], userData[UserInfo.PICTURE_COUNT], userData[UserInfo.DESCRIPTION], userData[UserInfo.AVERAGE_RATING])

    TG_ART_BOT.send_message(message.from_user.id, answer, reply_markup=markup)    

def ToPictureLine(message):

    markup  = types.InlineKeyboardMarkup(resize_keyboard=True)
    ranking = types.InlineKeyboardButton("Оценить рисунок")

    markup.add(next, ranking, back)
        
    msg = TG_ART_BOT.send_message(message.from_user.id, "PictureInfo", reply_markup=markup)

    kMarkup     = types.ReplyKeyboardMarkup(resize_keyboard=True)
    next        = types.KeyboardButton("Следующий рисунок")    
    back        = types.KeyboardButton("Главное меню")

    kMarkup.row(next)
    kMarkup.row(back)

    TG_ART_BOT.send_message(msg.from_user.id, reply_markup=kMarkup)

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

    if CheckUserExists(message, message.from_user.id):    

        if message.text == "Главное меню":
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

########################################################################### {
def CheckUserPicLimit(userID) -> bool:

    return False

def UploadPicture(picture, userID, description) -> bool:

    return False

@TG_ART_BOT.message_handler(content_types=['photo'])
def PictureHandler(message):

    userID = 0

    if CheckUserPicLimit(userID):
        if UploadPicture(message.photo, userID, message.text):
            TG_ART_BOT.send_message(message.from_user.id, Messages.PICTURE_UPLOAD_SUCCESS)
        else:
            TG_ART_BOT.send_message(message.from_user.id, Messages.PICTURE_UPLOAD_FAILED)
    else:
        TG_ART_BOT.send_message(message.from_user.id, Messages.PICTURE_LIMIT_REACHED)
    
########################################################################### {
