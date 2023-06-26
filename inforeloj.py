from reloj import Reloj
from config import Conf
from datetime import datetime
from conectDB import sqlDB

class InfoReloj(object):
    _total = 0
    _listrecords = None
    _anviz = None

    def __init__(self):
        config = Conf()
        datosReloj = config.getConfReloj();
        self._anviz = Reloj(device_id=int(1), ip_addr=str(datosReloj.reloj), ip_port=int(datosReloj.puerto))
        self._anviz.set_datetime(datetime.now())
        records = self._anviz.download_all_records()
        self._listrecords = list(records)
        total = len(self._listrecords)
        self._total = total
        print("New Record to Download: "+str(total))

    def getTotal(self):
        return self._total
    
    def resetTable(self,cursor,db):
        sql = "TRUNCATE TABLE `reloj`.`asistencia`;"
    
        try:
            cursor.execute(sql)
            while cursor.nextset():
                pass
            db.commit()
        except:
            print("ERROR: SQL -> "+sql)

    def insertDb(self):
        sql = sqlDB()
        sql.connect()
        self.resetTable(sql.cursor,sql.db)
        for record in self._listrecords:
            strrec = str(record)
            try:
                strrec = strrec.replace("Record(", "").replace(
                    "datetime=datetime.datetime(", "(")
                columns = strrec.replace("code=","").replace("bkp=", "").replace("type=", "").replace("work=", "").replace("(", "").replace(")", "").strip()
                columns = columns.split(",")
                legajo = columns[0].strip()
                anio = columns[1].strip()
                mes = columns[2].strip()
                dia = columns[3].strip()
                hora = columns[4].strip()
                min = columns[5].strip()
                if (int(dia) < 10):
                    dia = "0"+dia
                if (int(mes) < 10):
                    mes = "0"+mes
                if (int(min) < 10):
                    min = "0"+min
                
                if (int(hora) < 10):
                    hora = "0"+hora

                fecha = anio+"-"+mes+"-"+dia
                

                if(len(columns)==10):
                    dtype = columns[8]
                    sec = columns[6].strip()
                else:
                    dtype = columns[7]
                    sec ='0'
                
                if (int(sec) < 10):
                    sec = "0"+sec
                hora = hora +":"+min+":"+sec
                drow = legajo+","+fecha+" "+hora+",TYPE="+dtype
                #print(drow)
                
            except Exception as ex2:
                print("Segundo error:")
                print(ex2)
                print(strrec)
        query = "INSERT INTO `reloj`.`asistencia`(`Legajo`,`Fecha`,`Tipo`) VALUES ("
        query = query+"'"+legajo+"','"+fecha+" "+ hora +"','"+dtype+"');"
        try:
            sql.cursor.execute(query)
            while sql.cursor.nextset():
                pass
               
            sql.db.commit()
        except:
            print("ERROR: SQL -> "+query)
            sql.db.rollback()
        print("Download Completed")
        sql.close()
    
 
r = InfoReloj()
r.insertDb()