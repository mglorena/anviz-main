from config import Conf
import MySQLdb

class sqlDB(object):
    _smtp = "170.210.200.2"
    _smtpport = 25

    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        config = Conf()
        datos = config.getConfDB()
        self.db = MySQLdb.connect(str(datos.host), str(datos.usuario), str(datos.contra), str(datos.base))
        self.cursor = self.db.cursor()
     

    def close(self):
        self.db.close()
        
    
