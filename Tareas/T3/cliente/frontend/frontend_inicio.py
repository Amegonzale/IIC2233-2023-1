import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QPushButton, QMessageBox
from PyQt5.QtWidgets import QWidget, QLabel


class VentanaInicio(QWidget):
    senal_cerrar_cliente = pyqtSignal()
    senal_iniciar_partida = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_gui()
        self.setFixedSize(1080, 1080)

    def init_gui(self):
        self.players = []
        self.sprites = {}

        self.title = "Ventana de inicio"
        self.setWindowTitle(self.title)

        # fondo
        self.background = QLabel('', self)
        self.background.resize(1080, 1080)

        self.titulo = QLabel('SALA DE ESPERA', self)
        font_titulo = QFont()
        font_titulo.setPointSize(24)
        font_titulo.setBold(True)
        self.titulo.setFont(font_titulo)
        self.titulo.move(370, 200)

        # Iniciar
        self.boton_inicio = QPushButton('Iniciar', self)
        self.boton_inicio.resize(self.boton_inicio.sizeHint())
        self.boton_inicio.setGeometry(500, 820, 80, 25)
        self.boton_inicio.clicked.connect(self.iniciar)

        # Salir
        self.boton_salir = QPushButton('Salir', self)
        self.boton_salir.resize(self.boton_salir.sizeHint())
        self.boton_salir.setGeometry(500, 880, 80, 25)
        self.boton_salir.clicked.connect(self.cerrar)

    def update_sprites(self, info):
        self.sprites['RUTA_USER'] = os.path.join(*info['RUTA_USER'])
        imagen_fondo = QPixmap(os.path.join(*info['RUTA_FONDO_INICIO']))
        self.background.setPixmap(imagen_fondo)

    def cerrar(self):
        self.senal_cerrar_cliente.emit()

    def iniciar(self):
        self.senal_iniciar_partida.emit()

    def disable(self):
        self.boton_inicio.setEnabled(False)

    def enable(self):
        self.boton_inicio.setEnabled(True)

    def update_interface(self, num_players, names):
        '''
        Este metodo actualiza la interface, crea los labels de
        los iconos y nombres de los clientes que estan conectados.
        '''

        imagen_user = QPixmap(self.sprites['RUTA_USER'])
        imagen_user = imagen_user.scaled(150, 150)
        font_players = QFont()
        font_players.setPointSize(18)
        pos_x = 100

        for player in self.players:
            player[0].hide()
            player[1].hide()

        for num in range(num_players):
            jugador = QLabel('', self)
            jugador.setPixmap(imagen_user)
            jugador.move(pos_x, 470)

            jugador_txt = QLabel(names[num], self)
            jugador_txt.setFont(font_players)
            jugador_txt.move(pos_x, 650)

            jugador.show()
            jugador_txt.show()

            self.players.append([jugador, jugador_txt])

            pos_x += 250

        self.update()

    def sala_llena(self):
        QMessageBox.information(self, 'Sala Llena', 'SALA LLENA - Espere un cupo')

    def cupo_disponible(self):
        QMessageBox.information(self, 'Cupo Disponible', 'CUPO ENCONTRADO')

    def partida_en_juego(self):
        QMessageBox.information(self, 'Partida En Juego', 'PARTIDA EN JUEGO - intentelo mas tarde')

    def desconexion_sv(self):
        if self.isVisible():
            QMessageBox.information(self, 'Error', 'Se ha perdido la conexion con el servidor')
        self.close()

    def closeEvent(self, e) -> None:
        self.senal_cerrar_cliente.emit()
