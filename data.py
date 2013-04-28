from os.path import expanduser, join, exists
import re
import hashlib
import configparser

class data():
    def __init__(self, usuario= None):
        self.logo = "Img/logo.png"
        self.nombre = "Buapman"
        self.urlBase = "http://webserver1.siiaa.siu.buap.mx"
        self.ruta = "/autoservicios"
        self.fragmentoLogin = self.ruta + "/twbkwbis.P_ValLogin"
        self.reMatricula = re.compile("^2[0-9]{8}$")
        self.elementosLogin = {
            "logo" : True,
            "guardarPassword": False,
            "extra": True, 
            "passwordLongitud": 32,
            "passwordEcho": "Password"
        }

        if usuario and self.reMatricula.search(usuario):
            print("get imagen")
            self.cabecera = self.getImagen(usuario)
        else:
            self.cabecera = "https://pbs.twimg.com/media/BIvE31lCcAAkirY.png:large"


    def setImagen(self, url, usuario):
        hash = "." + hashlib.md5(usuario.encode()).hexdigest()
        home = expanduser('~')
        configverif = join(home,hash)
        config = configparser.RawConfigParser()
        
        if exists(configverif):
            config.read(configverif)
        else:
            config.add_section('Cabecera')
        
        config.set('Cabecera', 'urlImagen', url)

        with open(configverif, "w") as configArchivo:
            config.write(configArchivo)

        self.cabecera = url

    def getImagen(self, usuario):
        hash = "." + hashlib.md5(usuario.encode()).hexdigest()
        home = expanduser('~')
        configverif = join(home,hash)
        config = configparser.RawConfigParser()
        
        if exists(configverif):
            config.read(configverif)
            print(config.get('Cabecera', 'urlImagen'))
        
            return config.get('Cabecera', 'urlImagen')
        else:
            return "https://pbs.twimg.com/media/BIvE31lCcAAkirY.png:large"
            

manejadorDatos = data()
