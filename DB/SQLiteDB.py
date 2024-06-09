from ADataBase import ADataBase
import sqlite3

USER_TABLE_CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS "User" 
(
    "ID"	INTEGER NOT NULL UNIQUE,
    "Login"	TEXT NOT NULL UNIQUE,
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

class SQLiteDataBase(ADataBase):    

    def __init__(self, dbFile, login = "", password = ""):
        super().__init__("SQLITE", dbFile, login, password)

        pass
          
    def ExecQuery(self, query):

        conn = sqlite3.connect(super().DBFile())
        cursor = conn.cursor()

        if ("SELECT" in query):
            cursor.execute(query)
            result = cursor.fetchAll()
            conn.close()

            return result            
        else:
            cursor.execute(query)

            conn.commit()
            conn.close()                        
            pass        

        return
    

    

    