#!/usr/bin/python

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *
from PySide import QtGui 
import data
from login import *

view = {
    "h2":"#F55",
    "time": "#55F",
    "link": "#000",
    "linkVisited": "#FF0",
    "color": "#FF0"
}
def makeCookie(Name, Value):
    '''
    @param: 
        Name: Name cookie
        Value: Value cookie
    '''
    cookie = QNetworkCookie()
    cookie.setName(Name)
    cookie.setValue(Value)
    cookie.setPath('/autoservicios')
    cookie.setDomain('webserver1.siiaa.siu.buap.mx')
    return cookie


class Buapman(QtGui.QWidget):
    def __init__(self, padre, usuario, password):
        super(Buapman, self).__init__(padre)
        manejadorDatos = data.data(usuario)


        web = QWebView()
        self.usuario = usuario
        password = password
        url = data.manejadorDatos.urlBase + data.manejadorDatos.fragmentoLogin
        curl = url+"?sid="+ usuario+"&PIN="+password

        self.botonAvanza = QPushButton(padre)
        self.botonRetrocede = QPushButton(padre)
        self.botonRecargar = QPushButton(padre)
        self.botonSalir = QPushButton(padre)
        self.botonConfig = QPushButton(padre)
        self.padre = padre
        
        def salir():
            web.load("http://webserver1.siiaa.siu.buap.mx:81/autoservicios/twbkwbis.P_Logout")
            self.padre.login()

    
        self.botonAvanza.setIcon(QIcon("Img/go-next.png"))
        self.botonRetrocede.setIcon(QIcon("Img/go-previous"))
        self.botonRecargar.setIcon(QIcon("Img/view-refresh"))
        self.botonSalir.setIcon(QIcon("Img/user-offline"))
        self.botonConfig.setIcon(QIcon("Img/system-run"))
        self.botonesAccion = self.empaquetaHorizontal(self.botonRetrocede, 
                                                      self.botonAvanza,
                                                      self.botonRecargar,
                                                      self.botonConfig,
                                                      self.botonSalir)

        self.botonAvanza.clicked.connect(web.forward)
        self.botonRetrocede.clicked.connect(web.back)
        self.botonRecargar.clicked.connect(web.reload)
        self.botonConfig.clicked.connect(self.Config)
        self.botonSalir.clicked.connect(salir)
        
        jar = QNetworkCookieJar(web)
        request = QNetworkAccessManager(web)

        cookieValid = QNetworkCookie()

        request.setCookieJar(jar)

        cookie = makeCookie('TESTID', 'set')
        jar.setAllCookies([cookie])

        load=request.createRequest(QNetworkAccessManager.GetOperation, QNetworkRequest(QUrl(curl)))
        self.contador = 0
        def progreso(progreso):
            if self.padre.LoginEstatus == True:
                self.padre.loginVentana.ui.progreso.setValue(progreso)
            

        web.loadProgress.connect(progreso)
        web.load(load.request())

        page = web.page()
        page.loadFinished.connect(lambda x : x and finishpage(x) )

        mainFrame=page.mainFrame()


        def finishpage(finish):
            imagen = data.manejadorDatos.getImagen(self.usuario)
            if self.padre.LoginEstatus == True:
                self.padre.stack.setCurrentWidget(self.padre.Web)

            self.padre.LoginEstatus = False
            # print(mainFrame.documentElement().document().findFirst('body ').tagName())
    
            # print(mainFrame.documentElement().document().findFirst('DIV.').tagName())
            document = mainFrame.documentElement().document()
            # dddefault = document.findAll('.dddefault')
            # if dddefault.count() > 0:
            #     for i in range(dddefault.count()):
            #         print(dddefault.at(i).firstChild().toPlainText())
            document.evaluateJavaScript('''
            h2=document.getElementsByTagName('H2')
            h2[0].style.color = "{h2}";
            body=document.getElementsByTagName('body')
            body[0].style.backgroundImage = "url({url})";
            body[0].style.color = "{color}";
            body[0].style.backgroundSize= "1425px 110px";
            div = document.getElementsByClassName('pldefault')
            for (i=0; i<div.length; i++) 
            div[i].style.color = "{time}";
            div = document.getElementsByClassName("submenulinktext2")
            for (i=0; i<div.length; i++) {{
            div[i].style.color = "{link}";
            if (div[i].text == "SALIR") number = i;
            }}
            div[number].parentNode.removeChild(div[number]);
            div = document.getElementsByClassName('pageheaderdiv1')
            div[0].style.marginTop = "123.75px";
            elim = document.getElementsByClassName('pagefooterdiv');
            elim[0].parentNode.removeChild(elim[0]);
            elim = document.getElementsByClassName('poweredbydiv');
            elim[0].parentNode.removeChild(elim[0]);
            div[0].style.width = "1303.6875px";
            '''.format(url=imagen, time=view["time"],link=view["link"],linkVisited=view["linkVisited"], h2=view["h2"], color=view['color']))
    
            # web.show()
    
            return finish

        botones = QWidget()
        botones.setLayout(self.botonesAccion)
        self.navegador = self.empaquetaVertical(botones,
                                                 web)
        self.setLayout(self.navegador)


    def empaquetaHorizontal(self, *argc):
        HCaja = QHBoxLayout()
        cont = 0
        for elemento in argc:
            if isinstance(elemento, QObject):
                HCaja.addWidget(elemento)
                cont += 1
        if cont > 0:
            return HCaja
        else:
            return []
                        
    def empaquetaVertical(self, *argc):
        VCaja = QVBoxLayout()
        cont = 0
        for elemento in argc:
            if isinstance(elemento, QObject):
                VCaja.addWidget(elemento)
                cont += 1

        if cont > 0:
            return VCaja
        else:
            return []

    def Config(self):
        texto, ok = QInputDialog.getText(self, "Cambio de Imagen", 
                                         "Introduce la url de una imagen")

        if ok:
            data.manejadorDatos.setImagen(str(texto), self.usuario)
            web.reload()
            
    def check(self, *argc):
        """
        Agrega los elementos de *argc a elementos, si los objetos son
        instancia de QObject.

        @param:
           *argc: Lista de elementos a ser agregados a elementos si
                  son instancia de QObject.

        @return: elementos.
        """
        elementos = []
        for value in argc:
            if isinstance(value, QObject):
                elementos.append(value)

        return elementos

def main():
    raiz = QtGui.QApplication(sys.argv)
    Central = QtGui.QMainWindow()
    ventana = Principal(Central)
    Central.setCentralWidget(ventana)
    estPropiedades(Central)
    # ventana.setLogin()
    sys.exit(raiz.exec_())


if __name__ == "__main__":
    main()
