from PySide import QtCore, QtGui
import sys
import data as datos
import red
import urllib

elementosLogin = datos.manejadorDatos.elementosLogin

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def __init__(self, padre):
        self.padre = padre
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(412, 521)
        self.gridLayoutWidget = QtGui.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(60, 380, 290, 120))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        # self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.envio()
        self.progreso()
        self.gridLayout.addWidget(self.progreso, 2, 0, 1, 1)
        self.verticalLayoutWidget = QtGui.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 150, 261, 91))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        # self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.matricula()
        self.verticalLayoutWidget_2 = QtGui.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(70, 280, 261, 91))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        # self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.passwordEtiqueta = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.password()
        self.logo(Form)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def matricula(self, longitud=9, accion=None, **argv):
        """
        Genera un objeto para recivir la matricula.
        """
        self.matriculaEtiqueta = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.matriculaEtiqueta.setFont(font)
        self.matriculaEtiqueta.setAlignment(QtCore.Qt.AlignCenter)
        self.matriculaEtiqueta.setObjectName(_fromUtf8("matriculaEtiqueta"))
        self.verticalLayout.addWidget(self.matriculaEtiqueta)
        self.matriculaTexto = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.matriculaTexto.setObjectName(_fromUtf8("matriculaTexto"))
        self.verticalLayout.addWidget(self.matriculaTexto)


        self.matriculaTexto.setMaxLength(longitud)
        self.matriculaTexto.setInputMask("9"*longitud)
        self.matriculaTexto.setTextMargins(5,5,5,5)


    def envio(self):
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(90)


        self.status = QtGui.QLabel()
        self.status.setFont(font)
        self.status.setAlignment(QtCore.Qt.AlignCenter)

        self.status.setText("Estado: Desconectado")
        self.status.setObjectName(_fromUtf8("status"))
        self.gridLayout.addWidget(self.status, 0, 0, 1, 1)
        self.envio = QtGui.QPushButton(self.gridLayoutWidget)
        self.envio.clicked.connect(self.antesLogin)
        self.envio.setObjectName(_fromUtf8("envio"))
        self.gridLayout.addWidget(self.envio, 1, 0, 1, 1)

    def password(self, echo=elementosLogin["passwordEcho"], 
                 longitud=elementosLogin["passwordLongitud"],
                 accion=None,
                 **argv):
        """
        Genera un objeto para recivir la contraseña.
        """
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        self.passwordEtiqueta.setFont(font)
        self.passwordEtiqueta.setAlignment(QtCore.Qt.AlignCenter)
        self.passwordEtiqueta.setObjectName(_fromUtf8("passwordEtiqueta"))
        self.verticalLayout_2.addWidget(self.passwordEtiqueta)
        self.passwordText = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.passwordText.setObjectName(_fromUtf8("passwordText"))
        self.verticalLayout_2.addWidget(self.passwordText)

        if echo == "PasswordEchoOnEdit":
            self.passwordText.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        else:
            self.passwordText.setEchoMode(QtGui.QLineEdit.Password)

        self.passwordText.returnPressed.connect(self.antesLogin)

        self.passwordText.setMaxLength(longitud)
        
    def progreso(self):
        self.progreso = QtGui.QProgressBar(self.gridLayoutWidget)
        self.progreso.setProperty("value", 0)
        self.progreso.setObjectName(_fromUtf8("progreso"))
        

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.envio.setText(_translate("Form", "Conectar", None))
        self.matriculaEtiqueta.setText(_translate("Form", "Matricula", None))
        self.passwordEtiqueta.setText(_translate("Form", "Contraseña", None))
        # self.logo.setText(_translate("Form", "TextLabel", None))

    def logo(self, Form, imagen=datos.manejadorDatos.logo, **argv):
        """
        Genera un contenedor para el elemento logo.

        @param:
           imagen: Dirección local de una imagen.

        @return: Un objeto label que funge como contenedor.
        """
        logo = QtGui.QPixmap(imagen)

        self.logo = QtGui.QLabel(Form)
        self.logo.setPixmap(logo)
        self.logo.setGeometry(QtCore.QRect(100, 10, 200, 121))
        self.logo.setObjectName(_fromUtf8("logo"))
        


    def antesLogin(self, **argc):
        getMatricula = self.matriculaTexto.text()
        getPassword = self.passwordText.text()
        if len(getPassword) >= 15:
            getPassword = getPassword[:15]

        if datos.manejadorDatos.reMatricula.search(getMatricula):
            if getPassword != "":
                if red.checkRed(datos.manejadorDatos.urlBase, 5):
                    self.envio.setCheckable(True)
                    self.matriculaTexto.clear()
                    self.passwordText.clear()
                    print("Estado: Red Accesible")

                    peticion = red.enviaPeticion(datos.manejadorDatos.urlBase + 
                                         datos.manejadorDatos.fragmentoLogin + 
                                         "?" + 
                                         urllib.parse.urlencode({"sid": getMatricula,
                                                                 "PIN": getPassword}),
                                         datos.manejadorDatos.urlBase[7:],
                                         datos.manejadorDatos.ruta)
                    if isinstance(peticion, str):
                        
                        print(peticion)
                        self.status.setText("Estado: %s", peticion)
                        
                        # self.status.adjustSize()
                    elif peticion:
                        self.padre.LoginEstatus = True
                        print("logueado")
                        self.status.setText("Estado: Accediendo")
                        print("Estado: Accediendo")
                        #self.status.adjustSize()
                        self.padre.web(getMatricula, getPassword)
                    else:
                        self.status.setText("Estado: Usuario o contraseña invalidos")
                        #self.status.adjustSize()
                        print("Estado: Usuario o contraseña invalidos")
                else:
                    self.status.setText("Estado: Red es lenta o no disponible")
                    #self.status.adjustSize()
                    print("Estado: Red es lenta o no disponible")
            else:
                self.status.setText("Estado: No hay contraseña")
                #self.status.adjustSize()
                print("Estado: No hay contraseña")
        else:
            self.status.setText("Estado: La matricula es invalida")
            # self.status.adjustSize()
            print("Estado: La matricula es invalida")


class ControlMainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui =  Ui_Form(parent)
        self.ui.setupUi(self)

# class ControlWeb(QtGui.QWidget):
#     def __init__(self, parent, usuario, password):
#         super(ControlWeb, self).__init__(parent)
#         import buapman
#         self.web = 



class Principal(QtGui.QWidget):
    def  __init__(self, principal, padre=None):
        super().__init__()
        self.stack = QtGui.QStackedLayout(self)
        self.loginVentana = ControlMainWindow(self)
        self.stack.insertWidget(0, self.loginVentana)
        self.setLayout(self.stack)
        # self._estPropiedades()
        self.padre = padre
        self.principal = principal
        self.LoginEstatus = True
        # self._estPropiedades()

                
    def web(self, usuario, password):
        import buapman
        self.principal.resize(800,600)
        self.Web = buapman.Buapman(self, usuario, password) #ControlWeb(self, usuario, password)
        self.stack.insertWidget(1, self.Web)
        
        # self.stack.setCurrentWidget(self.web)

    def login(self):
        self.loginVentana.ui.status.setText("Estado: No Conectado")
        self.principal.resize(400,550)
        del self.Web
        self.loginVentana.ui.progreso.setValue(0)
        self.stack.setCurrentWidget(self.loginVentana)

def estPropiedades(obj):
        """Inicializa el tamaño, la posicion y los elementos de la 
           ventana.
        """
        # self.setGeometry(300, 300, 500, 600)

        obj.setWindowTitle(datos.manejadorDatos.nombre)
        obj.setWindowIcon(QtGui.QIcon(datos.manejadorDatos.logo))
        obj.resize(400,550)
        obj.show()

