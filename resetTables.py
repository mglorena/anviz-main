#!/usr/bin/python

"""
    anviz
"""


import MySQLdb
import pandas as pd
from datetime import datetime
from collections import namedtuple

def updateInfoArticulos(cursor_remote,cursor_local):
    anio = datetime.now().date().strftime("%Y")
    # Seleccionar los datos de la tabla Personas
    sql = "SELECT * FROM transArticuloPersona WHERE YEAR(Fecha)="+anio+";"
    cursor_remote.execute(sql)
    data = cursor_remote.fetchall()

        # Crear un DataFrame de pandas con los datos seleccionados
    columns = [i[0] for i in cursor_remote.description]
    df = pd.DataFrame(data, columns=columns)
        
        # Actualizar la tabla existente con los datos del DataFrame
    for index, row in df.iterrows():
        sql = f"INSERT INTO transArticuloPersona (`PersonaId`,`ArticuloId`,`Fecha`) VALUES ({row['PersonaId']},{row['ArticuloId']},'{row['Fecha']}')"
        #print(sql,"\n")
        cursor_local.execute(sql)

def updateInfoPersonas(cursor_remote,cursor_local):
    
    # Seleccionar los datos de la tabla Personas
    sql = "SELECT PersonaId,Apellido,Nombre,Legajo,TipoDNI,CargoDesc,Categoria, true as Active,IFNULL(FechaNac,'0000-00-00 00:00:00') as FechaNac, IFNULL(FechaNac,'0000-00-00 00:00:00') as FechaIngreso,DNI,Turno FROM Personas WHERE Active=1;"
    cursor_remote.execute(sql)
    data = cursor_remote.fetchall()

        # Crear un DataFrame de pandas con los datos seleccionados
    columns = [i[0] for i in cursor_remote.description]
    df = pd.DataFrame(data, columns=columns)
        
        # Actualizar la tabla existente con los datos del DataFrame
    for index, row in df.iterrows():
        sql = f"INSERT INTO  `reloj`.`Personas` (`PersonaId`,`Apellido`,`Nombre`,`Legajo`,`TipoDNI`,`CargoDesc`,`Categoria`,`Active`,`FechaNac`,`FechaIngreso`,`DNI`,`Turno`) VALUES"
        sql+= f"({row['PersonaId']},'{row['Apellido']}','{row['Nombre']}',{row['Legajo']},'{row['TipoDNI']}','{row['CargoDesc']}',{row['Categoria']},{row['Active']},'{row['FechaNac']}','{row['FechaIngreso']}','{row['DNI']}','{row['Turno']}');"
        #print(sql)
        cursor_local.execute(sql)

def importDataTape():
        # Conectar a la base de datos remota
        db_remote = MySQLdb.connect("170.210.200.20","tape","oysadmin","tape")
        cursor_remote = db_remote.cursor()
        # Conectar a la base de datos local
        db_local = MySQLdb.connect("170.210.202.5", "reloj","reloj2021", "reloj")
        cursor_local = db_local.cursor()
        updateInfoArticulos(cursor_remote,cursor_local)
        updateInfoPersonas(cursor_remote,cursor_local)
        # Guardar los cambios en la base de datos local
        db_local.commit()

        # Cerrar las conexiones
        cursor_remote.close()
        db_remote.close()
        cursor_local.close()
        db_local.close()

def resetTable():
    # Conectar a la base de datos local
    db_local = MySQLdb.connect("170.210.202.5", "reloj","reloj2021", "reloj")
    cursor_local = db_local.cursor()
    sql = "TRUNCATE TABLE `reloj`.`transArticuloPersona`;"
    sql += "TRUNCATE TABLE `reloj`.`Personas`;"
       
    
    try:
        cursor_local.execute(sql)
        while cursor_local.nextset():
            pass
        db_local.commit()
    except Exception as ex2:
        print("ERROR: SQL -> "+sql)
        print("ERROR: SQL -> "+str(ex2))
    cursor_local.close()
    db_local.close()
                                    


if __name__ == '__main__':
    resetTable()
    importDataTape()
  