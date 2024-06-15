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

    if id == None: 
        msg = TG_ART_BOT.send_message(message.from_user.id, Messages.REG_GET_PROFILE_INFO_MESSAGE)           
        TG_ART_BOT.register_next_step_handler(msg, GetProfileInfo)                   
    else:                           
        return True

    return False


@TG_ART_BOT.message_handler(commands=['start', 'help'])
def StartMessage(message):    

    if (CheckUserExists(message.from_user.id)):
        TG_ART_BOT.send_message(message.from_user.id, Messages.BOT_DESCRIPTION)    
    else:                
        msg = TG_ART_BOT.send_message(message.from_user.id, Messages.WELCOME_MESSAGE)    
        msg = TG_ART_BOT.send_message(message.from_user.id, Messages.REG_GET_PROFILE_INFO_MESSAGE)           
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

    msg = TG_ART_BOT.send_message(message.from_user.id, Messages.REG_GET_PROFILE_INFO_MESSAGE)           
    TG_ART_BOT.register_next_step_handler(msg, GetProfileInfo)    
###########################################################################################

def GetProfileInfo(message):

    AddUserDescription(message.from_user.id, message.text)
    AddUserUsername(message.from_user.id, message.from_user.username)

    msg = TG_ART_BOT.send_message(message.from_user.id, Messages.REG_GET_BIRTHDAY_MESSAGE)    
    TG_ART_BOT.register_next_step_handler(msg, GetBirthday)    
###########################################################################################

def GetBirthday(message):

    AddUserBirthday(message.from_user.id, message.text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    y = types.KeyboardButton("Да")
    n = types.KeyboardButton("Нет")

    markup.add(y,n)

    msg = TG_ART_BOT.send_message(message.from_user.id, Messages.REG_GET_CONTENT_MARK, reply_markup=markup)    
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

        msg = TG_ART_BOT.send_message(message.from_user.id, Messages.REG_GET_CONTENT_MARK, reply_markup=markup)    
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
            ToMainMenu(message)
########################################################################### }

########################################################################### {
import base64

def DownloadFile(fileID):
    file_info   = TG_ART_BOT.get_file(fileID)
    return  TG_ART_BOT.download_file(file_info.file_path)

def CheckUserPicLimit(userID) -> bool:
    
    published   = handler.GetUserPublishedPictures(userID)
    limit       = handler.GetUserPicktureLimit(userID)

    if (published < limit):
        return True

    return False
    
def UploadPicture(message, **data):
        
    if (message.text == "Да"):
        rContent = 1
    elif(message.text == 'Нет'):
        rContent = 0
    elif(message.text == "Отменить загрузку"):
        ToMainMenu(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        y = types.KeyboardButton("Да")
        n = types.KeyboardButton("Нет")
        c = types.KeyboardButton("Отменить загрузку")

        markup.add(y, n)
        markup.row(c)                

        msg = TG_ART_BOT.send_message(message.from_user.id, Messages.IS_R_CONTENT, reply_markup=markup)
        TG_ART_BOT.register_next_step_handler(msg, UploadPicture, ID = data['ID'], Desc = data['Desc'], PhotoID = data['PhotoID'])

        return
        
    loaded = DownloadFile(data['PhotoID'])

    if (handler.AddNewPicture(data['ID'], data['Desc'], loaded, rContent)):
        msg = TG_ART_BOT.send_message(message.from_user.id, Messages.PICTURE_UPLOAD_SUCCESS)        
    else:
        msg = TG_ART_BOT.send_message(message.from_user.id, Messages.PICTURE_UPLOAD_FAILED)

    ToMainMenu(msg)

from io import BytesIO

@TG_ART_BOT.message_handler(content_types=['photo', 'text'])
def PictureHandler(message):

    userID = handler.GetDBId(message.from_user.id)

    if CheckUserPicLimit(userID) and (message.photo):    
        if handler.GetUserRContentAgree(userID):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            y = types.KeyboardButton("Да")
            n = types.KeyboardButton("Нет")

            markup.add(y, n)

            file_id     = message.photo[-1].file_id                        
            text = message.caption

            msg = TG_ART_BOT.send_message(message.from_user.id, Messages.IS_R_CONTENT, reply_markup=markup)            
            TG_ART_BOT.register_next_step_handler(msg, UploadPicture, PhotoID=file_id, Desc=text, ID=userID)                       
        else:

            file_id = message.photo[-1].file_id                                    
            loaded  = DownloadFile(file_id)

            if handler.AddNewPicture(userID, text, loaded, 0):
                msg = TG_ART_BOT.send_message(message, Messages.PICTURE_UPLOAD_SUCCESS)        
            else:
                msg = TG_ART_BOT.send_message(message, Messages.PICTURE_UPLOAD_FAILED)

            ToMainMenu(msg)
    else:
        TG_ART_BOT.send_message(message.from_user.id, Messages.PICTURE_LIMIT_REACHED)
    
########################################################################### {
