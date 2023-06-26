import argparse
import os
import configparser

class DatosReloj:
    def __init__(self, reloj, puerto, descripcion):
        self.reloj = reloj
        self.puerto = puerto
        self.descripcion = descripcion
        

class DBData:
    def __init__(self, host, usuario,contra,base):
        self.base = base
        self.usuario = usuario
        self.contra = contra
        self.host = host

class Conf(object):
    _connected = False
    _datosR = {}
    _datosBD = {}

    def __init__(self):
        parser = argparse.ArgumentParser(description='Export Data from Anviz')
        parser.add_argument("ini", help="INI File Configuration", type=str)
        args = parser.parse_args()
        config = configparser.ConfigParser()
        config.add_section('device')
        config.set('device', 'uniqueid', '1')
        config.add_section('file')
        config.set('file', 'filename', 'example.txt')

        config.sections()
        config.read(args.ini)
        filename = config.get('file', 'filename')
        self._datosR = DatosReloj(config.get('device', 'ipaddress'), config.get('device', 'port'), config.get('device', 'description'))
        self._datosBD =  DBData(config.get('database', 'host'),config.get('database', 'username'),config.get('database', 'password'),config.get('database', 'dbname'))
    

    def getConfReloj(self):
        return self._datosR

    def getConfDB(self):
        return self._datosBD

