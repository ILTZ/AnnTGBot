from DBHandler import DBHandler
from SQLiteDB import SQLiteDataBase

import os
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

REVIEW_TABLE_CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS "ReviewReport" 
(
	"ID"	INTEGER NOT NULL UNIQUE,
	"Text"	TEXT,
	"ReviewID"	INTEGER NOT NULL,
	"UserID"	INTEGER NOT NULL,
	CONSTRAINT "ReviewReportID" FOREIGN KEY("ReviewID") REFERENCES Review(ID),
	PRIMARY KEY("ID" AUTOINCREMENT),
	CONSTRAINT "UserReportID" FOREIGN KEY("UserID") REFERENCES User(ID)
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

        # query = f'''INSERT INTO User (UserName, Description, Birthday, Rcontent, ReviewCounter, PictureSlots) VALUES
        # ({tgID}, "{userName}", "{description}", "{birthday}", {int(rContent)}, 0, {startPictureSlots})'''
        
        # self.__dataBase.Execute(query)        

        return

    def AddNewPicture(self, userID, description, picture, rContetMark):

        # query = f'''INSERT INTO Picture (UserID, Description, PictureData, Rcontent) VALUES ({userID}, "{description}", {sqlite3.Binary(picture)}, {int(rContetMark)})'''        
        # self.__dataBase.Execute(query)        

        return

    def AddUserLink(self, userID, link):

        # query = f'''SELECT Link from Link WHERE UserID = {userID}'''

        # result = self.__dataBase.ExecQuery(query)
        # if (len(result) > 0):
        #     return False

        # query = f'''INSERT INTO Link (Link, UserID) VALUES ("{link}", {userID})'''
        # self.__dataBase.ExecQuery(query)

        return 

    def AddPictureReview(self, reviewerID, pictureID, text, rating):

        # query = f'''INSERT INTO Review (UserID, PictureID, Text, Rating, Read) VALUES ({reviewerID}, {pictureID}, "{text}", {rating}, 0)'''

        # self.__dataBase.ExecQuery(query)

        return

    def GetUserPictures(self, userID, rContent):

        # query = f'''SELECT * FROM Picture WHERE UserID = {userID} AND RContent = {int(rContent)}'''

        # return self.__dataBase.ExecQuery(query)

        return

    def GetUserLinks(self, userID):

        # query = f'''SELECT * FROM Link WHERE UserID = {userID}'''

        # return self.__dataBase.ExecQuery(query)

        return

    def GetUserInfo(self, tgLogin):

        # query = f'''SELECT * FROM User WHERE Login = "{tgLogin}"'''

        # return self.__dataBase.ExecQuery(query)

        return

    def GetPictureReview(self, pictureID):

        # query = f'''SELECT * FROM Review WHERE PictureID = {pictureID}'''

        # return self.__dataBase.ExecQuery(query)

        return
    
    def GetRandomPicture(self, userID):

        pass
