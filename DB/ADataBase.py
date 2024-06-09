
class ADataBase:

    _driver     = ""
    _dbFile     = ""
    _login      = ""
    _password   = ""

    def __init__(self, driver, dbFile, login, password):
        self._driver    = driver
        self._dbFile    = dbFile
        self._login     = login
        self._password  = password

        pass
            
    def ExecQuery(query):
        return
    
    def DBFile(self):
        return self._dbFile
    
    def Driver(self):
        return self._driver
    
    def Login(self):
        return self._login
    
    def Password(self):
        return self._password

