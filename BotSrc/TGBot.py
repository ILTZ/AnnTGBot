import BotSrc.BotData as BotData
import BotSrc.Messages as Messages

import telebot
from telebot import types
from DB.SQLiteDBHandler import handler

from DB.SQLiteDBHandler import UserInfo
from DB.SQLiteDBHandler import PictureInfo
from DB.SQLiteDBHandler import PictureReview

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

    TG_ART_BOT.send_message(message.from_user.id, Messages.BOT_DESCRIPTION)    

    if (CheckUserExists(message.from_user.id) == False):
        TG_ART_BOT.send_message(message.from_user.id, Messages.BOT_DESCRIPTION)    
        GoToRegistration(message)

########################################################################### User register process {

def GoToRegistration(message):    

    msg = TG_ART_BOT.send_message(message.from_user.id, Messages.REG_GET_PROFILE_INFO_MESSAGE)           
    TG_ART_BOT.register_next_step_handler(msg, GetProfileInfo)    
###########################################################################################

def GetProfileInfo(message):

    msg = TG_ART_BOT.send_message(message.from_user.id, Messages.REG_GET_BIRTHDAY_MESSAGE)    
    TG_ART_BOT.register_next_step_handler(msg, GetBirthday, message.from_user.username, message.text)    
###########################################################################################

def GetBirthday(message, *argv):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    y = types.KeyboardButton("Да")
    n = types.KeyboardButton("Нет")

    markup.add(y,n)

    msg = TG_ART_BOT.send_message(message.from_user.id, Messages.REG_GET_CONTENT_MARK, reply_markup=markup)    
    TG_ART_BOT.register_next_step_handler(msg, GetUserLinks, argv[0], argv[1], message.text)    
###########################################################################################

def GetUserLinks(message, *argv):

    msg = TG_ART_BOT.send_message(message.from_user.id, Messages.REG_GET_LINKS)
    TG_ART_BOT.register_next_step_handler(msg, GetRcontent, argv[0], argv[1], argv[2])    
###########################################################################################

def GetRcontent(message, *argv):

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
        TG_ART_BOT.register_next_step_handler(msg, GetRcontent, argv[0], argv[1], argv[2], argv[3])    
        return
        
    if ProcessUserData(message.from_user.id, argv[0], argv[1], argv[2], result, argv[3]):
        ToMainMenu(message)
    else:
        TG_ART_BOT.send_message(message.from_user.id, Messages.PROCESS_FAILED)
        TG_ART_BOT.send_message(message.from_user.id, Messages.PROCESS_RESTART)
        GoToRegistration(message)
###########################################################################################

def ProcessUserData(userTelegrammID, username, descripiton, birthday, rContent, links):
    if handler.AddNewUser(userTelegrammID, username, descripiton, birthday, rContent, PICTURE_LIMIT):
        userID = handler.GetDBId(userTelegrammID)

        if (len(links) == 0):
            handler.AddUserLink(userID, links)
        else:
            handler.AddUserLink(userID, "Пусто....")
        
        return True
    
    return False
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
    back        = types.KeyboardButton("Главное меню")    
    markup.row(back)
    
    TG_ART_BOT.send_message(message.from_user.id, Messages.PROFILE_INFO_MESSAGE, reply_markup=markup)    

    userID   = handler.GetDBId(message.from_user.id)
    userData = handler.GetUserInfo(userID)

    answer = Messages.FormProfileInfo(userData[UserInfo.USER_NAME], userData[UserInfo.LINKS], userData[UserInfo.REVIEW_COUNT], userData[UserInfo.PICTURE_COUNT], userData[UserInfo.DESCRIPTION], round(userData[UserInfo.AVERAGE_RATING], 1))

    iMarkup = types.InlineKeyboardMarkup()
    links   = types.InlineKeyboardButton("Редактировать ссылки",   callback_data=f"RedLinks:{userID}")
    profile = types.InlineKeyboardButton("Редактировать описание", callback_data=f"RedDesc:{userID}")
    delete  = types.InlineKeyboardButton("УДАЛИТЬ ПРОФИЛЬ",        callback_data=f"DelProfile:{userID}")

    iMarkup.row(links)
    iMarkup.row(profile)
    iMarkup.row(delete)

    TG_ART_BOT.send_message(message.from_user.id, answer, reply_markup=iMarkup)


def ToPictureLine(message):    
    
    userID = handler.GetDBId(message.from_user.id)
    pic = handler.GetRandomPicture(0, handler.GetUserRContentAgree(userID))

    if (len(pic) < 1):
        TG_ART_BOT.send_message(message.from_user.id, Messages.NO_PICTURE_FOR_USER)
        ToMainMenu(message)

        return
    
    info = pic[0]

    text = Messages.FormPictureCaption(description=info[PictureInfo.DESCRIPTION], userName=info[PictureInfo.AUTOR_USERNAME])

    markup  = types.InlineKeyboardMarkup()
    ranking = types.InlineKeyboardButton("Оценить",      callback_data=f"RatingPic:{info[PictureInfo.ROW_ID]}")
    report  = types.InlineKeyboardButton("Пожаловаться", callback_data=f"RepPic:{info[PictureInfo.ROW_ID]}")

    markup.row(ranking)    
    markup.row(report)

    TG_ART_BOT.send_photo(message.from_user.id, photo=info[PictureInfo.TG_FILE_ID], caption=text, reply_markup=markup)        
    
def ToGalery(message):
    
    userID = handler.GetDBId(message.from_user.id)
    pictures = handler.GetUserPictures(userID)

    markup      = types.ReplyKeyboardMarkup(resize_keyboard=True)        
    back        = types.KeyboardButton("Главное меню")
    markup.add(back)

    TG_ART_BOT.send_message(message.from_user.id, text=Messages.GALERY_MESSAGE, reply_markup=markup)    

    for pictureData in pictures:
        
        markup = types.InlineKeyboardMarkup()
        delete = types.InlineKeyboardButton("Удалить изображение", callback_data=f"DelPic:{pictureData[PictureInfo.ROW_ID]}")
        markup.add(delete)

        text = Messages.FormPictureCaption(pictureData[PictureInfo.DESCRIPTION], pictureData[PictureInfo.AVERAGE_RATING])

        TG_ART_BOT.send_photo(chat_id=message.from_user.id, photo=pictureData[PictureInfo.TG_FILE_ID], caption=text, reply_markup=markup)                    

def ToArtistSearch(message):
    pass

def ToReview(message):

    markup  = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back    = types.KeyboardButton("Главное меню")

    markup.add(back)

    userID   = handler.GetDBId(message.from_user.id)
    pictures = handler.GetUserPictures(userID)

    TG_ART_BOT.send_message(message.from_user.id, "Ваши отзывы", reply_markup=markup)    

    for row in pictures:
                
        TG_ART_BOT.send_photo(message.from_user.id, photo=row[PictureInfo.TG_FILE_ID])                    

        reviews = handler.GetPictureReview(row[PictureInfo.ROW_ID])

        if (len(reviews) > 0):
            for rev in reviews:

                markup = types.InlineKeyboardMarkup()
                report = types.InlineKeyboardButton("Пожаловаться", callback_data=f"RepRev:{rev[PictureReview.ID]}")
                markup.add(report)

                TG_ART_BOT.send_message(message.from_user.id, rev[PictureReview.TEXT], reply_markup=markup)            
    
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

        elif (message.text == "Начать просмотр"):
            
            kMarkup     = types.ReplyKeyboardMarkup(resize_keyboard=True)
            next        = types.KeyboardButton("Следующий рисунок")    
            back        = types.KeyboardButton("Главное меню")

            kMarkup.row(next)
            kMarkup.row(back)
            
            TG_ART_BOT.send_message(message.from_user.id, text=Messages.SWITCH_TO_PICTURE_LINE, reply_markup=kMarkup)
            
            ToPictureLine(message)   

        elif (message.text == "Следующий рисунок"):           
            ToPictureLine(message)   

        else:
            ToMainMenu(message)

    else:
        GoToRegistration(message)
########################################################################### }

########################################################################### {

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

    if (handler.AddNewPicture(data['ID'], data['Desc'], data['PhotoID'], rContent)):
        TG_ART_BOT.send_message(message.from_user.id, Messages.PICTURE_UPLOAD_SUCCESS)                
    else:
        TG_ART_BOT.send_message(message.from_user.id, Messages.PROCESS_FAILED)

    ToMainMenu(message)

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

            if handler.AddNewPicture(userID, text, file_id, 0):
                msg = TG_ART_BOT.send_message(message, Messages.PICTURE_UPLOAD_SUCCESS)        
            else:
                msg = TG_ART_BOT.send_message(message, Messages.PICTURE_UPLOAD_FAILED)

            ToMainMenu(msg)
    else:
        TG_ART_BOT.send_message(message.from_user.id, Messages.PICTURE_LIMIT_REACHED)
    
########################################################################### {

########################################################################### {
@TG_ART_BOT.callback_query_handler(func=lambda call: True)
def cbHandler(call):

    comand, data = call.data.split(':')

    if (comand == 'DelPic'):
        if handler.RemovePicture(data):
            TG_ART_BOT.send_message(call.from_user.id, Messages.PICTURE_DELETE_SUCCESS)
        else:
            TG_ART_BOT.send_message(call.from_user.id, Messages.PROCESS_FAILED)

    elif(comand == 'RatingPic'):
        
        markup = types.InlineKeyboardMarkup()
                
        for i in range (1, 6):
            btn = types.InlineKeyboardButton(text=f'{i}', callback_data=f'RatePic:{i}-{data}')
            markup.add(btn)        

        TG_ART_BOT.send_message(call.from_user.id, Messages.RATE_PICTURE_MSG, reply_markup=markup)        

    elif(comand == 'RatePic'):
        rating, picID = data.split('-')

        msg = TG_ART_BOT.send_message(call.from_user.id, Messages.DESCRIBE_PICTURE_RATE_MSG)
        TG_ART_BOT.register_next_step_handler(msg, reviewData, picID, rating)
        
    elif(comand == 'RepPic'):
        
        msg = TG_ART_BOT.send_message(call.from_user.id, Messages.REPORT_MESSAGE)
        TG_ART_BOT.register_next_step_handler(msg, reportPicture, data)                

    elif(comand == 'RepRev'):

        msg = TG_ART_BOT.send_message(call.from_user.id, Messages.REPORT_MESSAGE)
        TG_ART_BOT.register_next_step_handler(msg, reportReview, data)     

    elif(comand == 'RedLinks'):
        
        msg = TG_ART_BOT.send_message(call.from_user.id, Messages.REDACT_LINKS_MSG)
        TG_ART_BOT.register_next_step_handler(msg, updateLinks, data)             

    elif(comand == 'RedDesc'):

        msg = TG_ART_BOT.send_message(call.from_user.id, Messages.REDACT_DESCRIPTION_MSG)
        TG_ART_BOT.register_next_step_handler(msg, updateDescription, data)             

    elif(comand == 'DelProfile'):

        mu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        y = types.KeyboardButton("Да")
        n = types.KeyboardButton("Нет")
        mu.add(y, n)

        msg = TG_ART_BOT.send_message(call.from_user.id, Messages.DELETE_PROFILE_MSG, reply_markup=mu)
        TG_ART_BOT.register_next_step_handler(msg, deleteProfile, data)                     

def updateLinks(message, *argv):
    
    if (message.text == 'Главное меню'):
        ToMainMenu(message)

    userID = handler.GetDBId(message.from_user.id)

    if handler.UpdateLinks(userID, message.text):
        TG_ART_BOT.send_message(message.from_user.id, Messages.UPDATE_SUCCES_MSG)
    else:
        TG_ART_BOT.send_message(message.from_user.id, Messages.PROCESS_FAILED)

    ToProfileInfo(message)
####################################################################################


def updateDescription(message, *argv):

    if (message.text == 'Главное меню'):
        ToMainMenu(message)

    userID = handler.GetDBId(message.from_user.id)

    if handler.UpdateDescription(userID, message.text):
        TG_ART_BOT.send_message(message.from_user.id, Messages.UPDATE_SUCCES_MSG)
    else:
        TG_ART_BOT.send_message(message.from_user.id, Messages.PROCESS_FAILED)    

    ToProfileInfo(message)
####################################################################################


def deleteProfile(message, *argv):    

    if (message.text == 'Да'):
        if handler.DeleteUser(argv[0]):
            TG_ART_BOT.send_message(message.from_user.id, Messages.PROFILE_WAS_DELETED)
        else:
            TG_ART_BOT.send_message(message.from_user.id, Messages.PROCESS_FAILED)

    elif(message.text == 'Нет'):
        TG_ART_BOT.send_message(message.from_user.id, Messages.PROFILE_WAS_SAVED)
        ToProfileInfo(message)
####################################################################################        

def reportReview(message, *argv):

    if (message.text == 'Главное меню'):
        ToMainMenu(message)    

    userID = handler.GetDBId(message.from_user.id)
    if handler.AddReviewReport(argv[0], userID, message.text):
        TG_ART_BOT.send_message(message.from_user.id, Messages.REPORT_ADDED_SUCCESS)
    else:
        TG_ART_BOT.send_message(message.from_user.id, Messages.PROCESS_FAILED)    

def reportPicture(message, *argv):

    if (message.text == 'Главное меню'):
        ToMainMenu(message)
    elif(message.text == 'Следующий рисунок'):
        ToPictureLine(message)

    userID = handler.GetDBId(message.from_user.id)
    if handler.AddPictureReport(userID, argv[0], message.text):
        TG_ART_BOT.send_message(message.from_user.id, Messages.REPORT_ADDED_SUCCESS)
    else:
        TG_ART_BOT.send_message(message.from_user.id, Messages.PROCESS_FAILED)        

def reviewData(message, *argv):

    if (message.text == 'Главное меню'):
        ToMainMenu(message)
    elif(message.text == 'Следующий рисунок'):
        ToPictureLine(message)

    userID = handler.GetDBId(message.from_user.id)
    
    if handler.AddPictureReview(userID, argv[0], message.text, argv[1]):
        text = Messages.REVIEW_SUCCESS_ADDED
        handler.UpdateAverageRating(argv[0])
        handler.IncreaseUserReviewCounter(userID)
    else:
        text = Messages.REVIEW_FAILED_ADDED
               
    TG_ART_BOT.send_message(message.from_user.id, text=text)

