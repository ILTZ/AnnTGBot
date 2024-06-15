from DB.DBHandler import DBHandler
from DB.SQLiteDB import SQLiteDataBase

import sqlite3

USER_TABLE_CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS "User" 
(
    "ID"	INTEGER NOT NULL UNIQUE,
    "TGUserID" INTEGER NOT NULL UNIQUE,
    "UserName"	TEXT NOT NULL UNIQUE,
    "Description"	TEXT,
    "Birthday"	TEXT NOT NULL,
    "Rcontent"	INTEGER NOT NULL,
    "ReviewCounter"	INTEGER NOT NULL,
    "PictureSlots"	INTEGER NOT NULL,
    PRIMARY KEY("ID" AUTOINCREMENT)
)'''

LINK_TABLE_CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS "Link"
(
	"ID"	INTEGER NOT NULL UNIQUE,
	"Link"	TEXT NOT NULL UNIQUE,
	"UserID"	INTEGER NOT NULL,
	CONSTRAINT "UserRef" FOREIGN KEY("UserID") REFERENCES User(ID),
	PRIMARY KEY("ID")
)'''

PICTURE_TABLE_CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS "Picture" 
(
    "ID"	INTEGER NOT NULL UNIQUE,
    "UserID" INTEGER NOT NULL,
    "Description"	TEXT,
    "PictureData"	BLOB,
    "Rcontent"	INTEGER,
    CONSTRAINT "UserPictureID" FOREIGN KEY("UserID") REFERENCES User(ID),
    PRIMARY KEY("ID" AUTOINCREMENT)
)'''

PICTURE_REPORT_TABLE_CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS "PictureReport" 
(
	"ID"	INTEGER NOT NULL UNIQUE,
	"Text"	TEXT,
	"PictureID"	INTEGER NOT NULL,
	"UserID"	INTEGER NOT NULL,
	CONSTRAINT "PictureReportID" FOREIGN KEY("PictureID") REFERENCES Picture(ID),
	PRIMARY KEY("ID" AUTOINCREMENT),
	CONSTRAINT "UserPictureReportID" FOREIGN KEY("UserID") REFERENCES User(ID)
)'''

REVIEW_TABLE_CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS "Review" 
(
	"ID"	INTEGER NOT NULL UNIQUE,
	"UserID"	INTEGER NOT NULL,
	"PictureID"	INTEGER NOT NULL,
	"Text"	TEXT NOT NULL,
	"Rating"	INTEGER NOT NULL,
	"Read"	INTEGER NOT NULL,
	CONSTRAINT "PictureReviewID" FOREIGN KEY("PictureID") REFERENCES Picture(ID),
	PRIMARY KEY("ID" AUTOINCREMENT),
	CONSTRAINT "UserReviewID" FOREIGN KEY("UserID") REFERENCES User(ID)
)'''

REVIEW_REPORT_TABLE_CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS "ReviewReport" 
(
	"ID"	INTEGER NOT NULL UNIQUE,
	"Text"	TEXT,
	"ReviewID"	INTEGER NOT NULL,
	"UserID"	INTEGER NOT NULL,
	CONSTRAINT "ReviewReportID" FOREIGN KEY("ReviewID") REFERENCES Review(ID),
	PRIMARY KEY("ID" AUTOINCREMENT),
	CONSTRAINT "UserReportID" FOREIGN KEY("UserID") REFERENCES User(ID)
)'''

from enum import Enum

class UserInfo(Enum):
    USER_NAME       = 1
    DESCRIPTION     = 2
    LINKS           = 3
    PICTURE_COUNT   = 4
    AVERAGE_RATING  = 5
    REVIEW_COUNT    = 6

class SQLiteDBHandler(DBHandler):

    __dataBase = SQLiteDataBase

    def __init__(self, dataBase):
        super().__init__()
        self.__dataBase = dataBase

        self.__dataBase.ExecQuery(USER_TABLE_CREATE_QUERY)
        self.__dataBase.ExecQuery(LINK_TABLE_CREATE_QUERY)
        self.__dataBase.ExecQuery(PICTURE_TABLE_CREATE_QUERY)
        self.__dataBase.ExecQuery(PICTURE_REPORT_TABLE_CREATE_QUERY)
        self.__dataBase.ExecQuery(REVIEW_TABLE_CREATE_QUERY)
        self.__dataBase.ExecQuery(REVIEW_REPORT_TABLE_CREATE_QUERY)

        pass

    def AddNewUser(self, tgID, userName, description, birthday, rContent, startPictureSlots):              

        query = f'''INSERT INTO User (TGUserID, UserName, Description, Birthday, Rcontent, ReviewCounter, PictureSlots) VALUES
        ({tgID}, "{userName}", "{description}", "{birthday}", {int(rContent)}, 0, {startPictureSlots})'''
        
        self.__dataBase.ExecQuery(query)            

    def AddNewPicture(self, userID, description, picture, rContetMark):

        query = f'''INSERT INTO Picture (UserID, Description, PictureData, Rcontent) VALUES ({userID}, "{description}", {picture}, {rContetMark})'''        
        return self.__dataBase.ExecQuery(query)        

    def AddUserLink(self, userID, link):

        query = f'''SELECT Link from Link WHERE UserID = {userID}'''

        result = self.__dataBase.ExecQuery(query)
        if (len(result) > 0):
            return False

        query = f'''INSERT INTO Link (Link, UserID) VALUES ("{link}", {userID})'''
        self.__dataBase.ExecQuery(query)

    def AddPictureReview(self, reviewerID, pictureID, text, rating):

        query = f'''INSERT INTO Review (UserID, PictureID, Text, Rating, Read) VALUES ({reviewerID}, {pictureID}, "{text}", {rating}, 0)'''

        self.__dataBase.ExecQuery(query)

    def GetUserPictures(self, userID, rContent):

        query = f'''SELECT * FROM Picture WHERE UserID = {userID} AND RContent = {int(rContent)}'''

        return self.__dataBase.ExecQuery(query)

    def GetUserPublishedPictures(self, userID):

        query = f'''SELECT COUNT(ID) as Cnt FROM Picture WHERE UserID = {userID}'''

        return self.__dataBase.ExecQuery(query)

    def GetUserLinks(self, userID):

        query = f'''SELECT * FROM Link WHERE UserID = {userID}'''

        return self.__dataBase.ExecQuery(query)

    def GetUserInfo(self, userID):

        result = self.GetUserLinks(userID)
        if (len(result) > 1):
            links = ', '.join(result)
        elif (len(result) == 1):
            links = result[0]
        else:
            links = 'Нет ссылок'

        userData = {}

        query = f'''SELECT UserName, Description, ReviewCounter FROM User where ID = {userID}'''
        result = list(self.__dataBase.ExecQuery(query)[0])

        userData[UserInfo.USER_NAME]      = result[0]
        userData[UserInfo.DESCRIPTION]    = result[1]
        userData[UserInfo.REVIEW_COUNT]   = result[2]
        userData[UserInfo.LINKS]          = links
        userData[UserInfo.PICTURE_COUNT]  = self.GetUserPublishedPictures(userID)[0][0]
        userData[UserInfo.AVERAGE_RATING] = self.GetAverageRating(userID)
        
        return userData   

    def GetUserPicktureLimit(self, userID):

        query = f'''SELECT PictureSlots FROM User WHERE ID = {userID}'''

        return self.__dataBase.ExecQuery(query)
    
    def GetDBId(self, tgID):

        query = f'''SELECT ID FROM User WHERE TGUserID = {tgID}'''
        
        result = self.__dataBase.ExecQuery(query)
        if (len(result) == 1):
            return result[0][0]

        return 

    def GetPictureReview(self, pictureID):

        query = f'''SELECT * FROM Review WHERE PictureID = {pictureID}'''

        return self.__dataBase.ExecQuery(query)
    
    def GetUserRContentAgree(self, userID):

        query = f'''SELECT Rcontent from User WHERE ID = {userID}'''

        return bool(self.__dataBase.ExecQuery(query)[0][0])

    def GetRandomPicture(self, userID):

        pass

    def GetAverageRating(self, userID):

        query = f'''select AVG(Rating) as AvgRating FROM Review INNER JOIN Picture ON Review.PictureID = Picture.ID WHERE Picture.UserID = {userID}'''

        return self.__dataBase.ExecQuery(query)  

db      = SQLiteDataBase("Test.db")
handler = SQLiteDBHandler(db)