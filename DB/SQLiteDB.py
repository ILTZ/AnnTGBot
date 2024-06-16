from DB.ADataBase import ADataBase
import sqlite3

class SQLiteDataBase(ADataBase):    

    def __init__(self, dbFile, login = "", password = ""):
        super().__init__("SQLITE", dbFile, login, password)

        pass
          
    def ExecQuery(self, query):
        try:
            conn = sqlite3.connect(super().DBFile())
            cursor = conn.cursor()

            cursor.execute(query)

            conn.commit()
            conn.close()                                        

            return True
        
        except:            
            return False
        
    def SelectQuery(self, query):

        try:
            conn = sqlite3.connect(super().DBFile())
            cursor = conn.cursor()

            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()                            
        
            return result     
        
        except:
            return None
        
    

    

    