import parametros as p
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QComboBox, QPushButton


class VentanaInicio(QWidget):
    senal_procesar_user = pyqtSignal(str)
    senal_info = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.init_gui()
        self.setFixedSize(600, 680)

    def init_gui(self):
        self.title = "Ventana de inicio"
        self.setWindowTitle(self.title)

        # fondo
        self.background = QLabel('', self)
        self.background.resize(600, 680)
        imagen_fondo = QPixmap(p.RUTA_FONDO)
        self.background.setPixmap(imagen_fondo)

        # logo
        self.logo = QLabel('', self)
        imagen_logo = QPixmap(p.RUTA_LOGO)
        self.logo.setPixmap(imagen_logo)
        self.logo.setGeometry(45, 30, 518, 95)

        # set username
        self.text = QLabel('Username:', self)
        self.text.setGeometry(15, 260, self.text.width(), 20)
        self.text.setStyleSheet('''
            color: white;
        ''')
        self.user = QLineEdit('', self)
        self.user.setGeometry(85, 260, 500, 20)

        # select archivo
        self.selector_archivos = QComboBox(self)
        self.selector_archivos.addItems(["Modo constructor"])
        self.selector_archivos.setGeometry(15, 300, 570, 20)

        # Iniciar
        self.boton_inicio = QPushButton('Iniciar', self)
        self.boton_inicio.resize(self.boton_inicio.sizeHint())
        self.boton_inicio.setGeometry(15, 620, 570, 25)
        self.boton_inicio.clicked.connect(self.validar_user)

        # Salir
        self.boton_salir = QPushButton('Salir', self)
        self.boton_salir.resize(self.boton_salir.sizeHint())
        self.boton_salir.setGeometry(15, 650, 570, 25)
        self.boton_salir.clicked.connect(self.close)

    # Carga los nombres de los mapas para el selector
    def actualizar_selector(self, lista_mapas):
        self.selector_archivos.addItems(lista_mapas)

    # Valida si el nombre de usuario es valido
    def validar_user(self):
        username = self.user.text()
        self.senal_procesar_user.emit(username)

    # Intenta enviar la informacion para iniciar
    # la partida ssi el username es valido
    def enviar_info(self, username_valido):
        if username_valido == 0:
            archivo = self.selector_archivos.currentText()
            username = self.user.text()
            self.senal_info.emit(archivo, username)

        elif username_valido == 1:
            self.ventana_error = VentanaUsuarioNotAlnum()
            self.ventana_error.show()

        elif username_valido == 2:
            self.ventana_error = VentanaTooShort()
            self.ventana_error.show()

        elif username_valido == 3:
            self.ventana_error = VentanaTooLong()
            self.ventana_error.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.boton_inicio.click()


class VentanaUsuarioNotAlnum(QWidget):
    def __init__(self):
        super().__init__()
        self.init_gui()
        self.setFixedSize(400, 200)

    def init_gui(self):
        self.title = "Usuario invalido"
        self.setWindowTitle(self.title)
        texto = 'Usuario invalido: nombre debe contener solo letras y numeros :('
        self.text = QLabel(texto, self)

        self.boton_salir = QPushButton('Entendido', self)
        self.boton_salir.resize(self.boton_salir.sizeHint())
        self.boton_salir.clicked.connect(self.close)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.boton_salir)

        self.setLayout(self.vbox)


class VentanaTooShort(QWidget):
    def __init__(self):
        super().__init__()
        self.init_gui()
        self.setFixedSize(400, 200)

    def init_gui(self):
        self.title = "Usuario invalido"
        self.setWindowTitle(self.title)
        texto = f'Usuario invalido: nombre debe contener almenos {p.MIN_CARACTERES} caracteres'
        self.text = QLabel(texto, self)

        self.boton_salir = QPushButton('Entendido', self)
        self.boton_salir.resize(self.boton_salir.sizeHint())
        self.boton_salir.clicked.connect(self.close)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.boton_salir)

        self.setLayout(self.vbox)


class VentanaTooLong(QWidget):
    def __init__(self):
        super().__init__()
        self.init_gui()
        self.setFixedSize(400, 200)

    def init_gui(self):
        self.title = "Usuario invalido"
        self.setWindowTitle(self.title)
        texto = f'Usuario invalido: nombre debe contener maximo {p.MAX_CARACTERES} caracteres'
        self.text = QLabel(texto, self)

        self.boton_salir = QPushButton('Entendido', self)
        self.boton_salir.resize(self.boton_salir.sizeHint())
        self.boton_salir.clicked.connect(self.close)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.boton_salir)

        self.setLayout(self.vbox)
