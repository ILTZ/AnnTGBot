from ADataBase import ADataBase
import sqlite3

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
    

    

    