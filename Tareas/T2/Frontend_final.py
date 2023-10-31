from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal, Qt, QUrl
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtMultimedia import QSoundEffect
import parametros as p


class VentanaWin(QWidget):
    senal_replay = pyqtSignal()
    senal_info_replay = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_gui()
        self.setFixedSize(400, 200)

    def init_gui(self):
        self.title = "WIN"
        self.setWindowTitle(self.title)
        self.text = QLabel('☆ FELICIDADES GANASTE ☆', self)
        self.puntaje = QLabel('', self)

        self.boton_play_again = QPushButton('Play again', self)
        self.boton_play_again.clicked.connect(self.play_again)
        self.boton_salir = QPushButton('Salir', self)
        self.boton_salir.clicked.connect(self.close)

        self.hbox_botones = QHBoxLayout()
        self.hbox_botones.addWidget(self.boton_play_again)
        self.hbox_botones.addWidget(self.boton_salir)
        self.hbox_botones.setAlignment(Qt.AlignBottom)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.puntaje)
        self.vbox.addLayout(self.hbox_botones)
        self.vbox.setAlignment(Qt.AlignCenter)

        self.setLayout(self.vbox)

        self.audio = QSoundEffect(self)
        self.audio.setSource(QUrl.fromLocalFile(p.AUDIO_WIN))

    def showEvent(self, e):
        self.audio.play()

    def update_user(self, username):
        text = f'☆ FELICIDADES {username} GANASTE ☆'
        self.text.setText(text)

    def set_puntaje(self, puntaje):
        text = f'Tu puntaje es: {puntaje}'
        self.puntaje.setText(text)

    def play_again(self):
        self.senal_replay.emit()
        self.senal_info_replay.emit()
        self.close()


class VentanaLoss(QWidget):
    senal_replay = pyqtSignal()
    senal_info_replay = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_gui()
        self.setFixedSize(400, 200)

    def init_gui(self):
        self.title = "PERDISTE"
        self.setWindowTitle(self.title)
        self.text = QLabel('☆ FELICIDADES PERDISTE ☆', self)
        self.causa = QLabel('', self)
        self.puntaje = QLabel('', self)

        self.boton_play_again = QPushButton('Play again', self)
        self.boton_play_again.clicked.connect(self.play_again)
        self.boton_salir = QPushButton('Salir', self)
        self.boton_salir.clicked.connect(self.close)

        self.hbox_botones = QHBoxLayout()
        self.hbox_botones.addWidget(self.boton_play_again)
        self.hbox_botones.addWidget(self.boton_salir)
        self.hbox_botones.setAlignment(Qt.AlignBottom)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.causa)
        self.vbox.addWidget(self.puntaje)
        self.vbox.addLayout(self.hbox_botones)
        self.vbox.setAlignment(Qt.AlignCenter)

        self.setLayout(self.vbox)

        self.audio = QSoundEffect(self)
        self.audio.setSource(QUrl.fromLocalFile(p.AUDIO_LOSS))

    def showEvent(self, e):
        self.audio.play()

    def update_causa(self, causa):
        self.causa.setText(causa)

    def update_user(self, username):
        text = f'☆ FELICIDADES {username} PERDISTE ☆'
        self.text.setText(text)

    def set_puntaje(self, puntaje):
        text = f'Tu puntaje es: {puntaje}'
        self.puntaje.setText(text)

    def play_again(self):
        self.senal_replay.emit()
        self.senal_info_replay.emit()
        self.close()
