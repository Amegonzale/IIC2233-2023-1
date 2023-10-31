import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QPushButton, QComboBox
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QMessageBox


class VentanaJuego(QWidget):
    senal_anunciar_valor = pyqtSignal(str)
    senal_pasar_turno = pyqtSignal()
    senal_usar_poder = pyqtSignal(str)
    senal_dudar = pyqtSignal()
    senal_cambiar_dados = pyqtSignal()
    senal_cerrar_juego = pyqtSignal()
    senal_cerrar_cliente = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_gui()
        self.setFixedSize(1280, 720)

    def init_gui(self):
        self.players = None
        self.own_info = None
        self.my_turn = False  # Para estar al tanto si los botones estan habilitados
        self.turno_actual = ''
        self.turno_anterior = ''
        self.vidas_iniciales = None
        self.puede_cambiar_dados = True
        self.botones = []
        self.numero_turno = 0
        self.valor_max = 0
        self.dados = {}
        self.load_interface()

    def load_interface(self):
        # Por si no se nota, no me gusto qtdesigner
        self.title = "Ventana de Juego"
        self.setWindowTitle(self.title)

        # fondo
        self.background = QLabel('', self)
        self.background.resize(1280, 720)

        # Fonts
        font_txt = QFont()
        font_txt.setPointSize(14)
        font_txt.setBold(True)
        font_vidas = QFont()
        font_vidas.setPointSize(20)
        font_vidas.setBold(True)
        font_btn = QFont()
        font_btn.setPointSize(10)

        # Jugadores
        self.jugadores = []
        # jugador 1
        self.jugador1 = QLabel('', self)
        self.jugador1.move(590, 550)
        self.jugador_txt1 = QLabel('', self)
        self.jugador_txt1.move(580, 640)
        self.jugador_vidas1 = QLabel('♥♥♡', self)
        self.jugador_vidas1.move(700, 575)
        self.jugadores.append((self.jugador1, self.jugador_txt1, self.jugador_vidas1))

        # jugador 2
        self.jugador2 = QLabel('', self)
        self.jugador2.move(1000, 350)
        self.jugador_txt2 = QLabel('', self)
        self.jugador_txt2.move(1000, 440)
        self.jugador_vidas2 = QLabel('♥♥♡', self)
        self.jugador_vidas2.move(1120, 375)
        self.jugadores.append((self.jugador2, self.jugador_txt2, self.jugador_vidas2))

        # jugador 3
        self.jugador3 = QLabel('', self)
        self.jugador3.move(590, 130)
        self.jugador_txt3 = QLabel('', self)
        self.jugador_txt3.move(580, 220)
        self.jugador_vidas3 = QLabel('♥♥♡', self)
        self.jugador_vidas3.move(700, 155)
        self.jugadores.append((self.jugador3, self.jugador_txt3, self.jugador_vidas3))

        # jugador 4
        self.jugador4 = QLabel('', self)
        self.jugador4.move(220, 350)
        self.jugador_txt4 = QLabel('', self)
        self.jugador_txt4.move(220, 440)
        self.jugador_vidas4 = QLabel('♥♥♡', self)
        self.jugador_vidas4.move(340, 375)
        self.jugadores.append((self.jugador4, self.jugador_txt4, self.jugador_vidas4))

        for jug, txt, vidas in self.jugadores:
            txt.setFont(font_txt)
            txt.setStyleSheet("color: white;")
            vidas.setFont(font_vidas)
            vidas.setStyleSheet("color: white;")

        # Turnos
        self.turno_ac_txt = QLabel('', self)
        self.turno_ac_txt.setFont(font_txt)
        self.turno_ac_txt.setStyleSheet("color: white;")
        self.turno_ac_txt.move(520, 3)

        self.turno_an_txt = QLabel('', self)
        self.turno_an_txt.setFont(font_txt)
        self.turno_an_txt.setStyleSheet("color: white;")
        self.turno_an_txt.move(490, 38)

        self.num_mayor_txt = QLabel('', self)
        self.num_mayor_txt.setFont(font_txt)
        self.num_mayor_txt.setStyleSheet("color: white;")
        self.num_mayor_txt.move(50, 38)

        self.num_turno_txt = QLabel('', self)
        self.num_turno_txt.setFont(font_txt)
        self.num_turno_txt.setStyleSheet("color: white;")
        self.num_turno_txt.move(1000, 38)

        self.error_txt = QLabel('', self)
        self.error_txt.setStyleSheet("color: white;")
        self.error_txt.move(1075, 525)

        # dados
        self.dado11 = QLabel('', self)
        self.dado11.move(580, 490)
        self.dado12 = QLabel('', self)
        self.dado12.move(640, 490)

        self.dado21 = QLabel('', self)
        self.dado21.move(930, 350)
        self.dado22 = QLabel('', self)
        self.dado22.move(930, 410)

        self.dado31 = QLabel('', self)
        self.dado31.move(580, 250)
        self.dado32 = QLabel('', self)
        self.dado32.move(640, 250)

        self.dado41 = QLabel('', self)
        self.dado41.move(150, 350)
        self.dado42 = QLabel('', self)
        self.dado42.move(150, 410)

        self.dds = [(self.dado11, self.dado12), (self.dado21, self.dado22),
                    (self.dado31, self.dado32), (self.dado41, self.dado42)]
        for (dado1, dado2) in self.dds:
            dado1.setStyleSheet("border: 1px solid white;")
            dado2.setStyleSheet("border: 1px solid white;")
            dado1.setFixedSize(45, 45)
            dado2.setFixedSize(45, 45)

        # Botones
        self.btn_anunciar_valor = QPushButton()
        self.btn_anunciar_valor = QPushButton('Anunciar Valor', self)
        self.btn_anunciar_valor.setGeometry(950, 550, 120, 30)
        self.btn_anunciar_valor.clicked.connect(self.anunciar_valor)

        self.ingreso_valor = QLineEdit('', self)
        self.ingreso_valor.setPlaceholderText('Ingrese valor Aqui')
        self.ingreso_valor.setGeometry(1075, 550, 120, 30)

        self.btn_pasar_turno = QPushButton()
        self.btn_pasar_turno = QPushButton('Pasar turno', self)
        self.btn_pasar_turno.setGeometry(950, 585, 120, 30)
        self.btn_pasar_turno.clicked.connect(self.pasar_turno)

        self.btn_usar_poder = QPushButton()
        self.btn_usar_poder = QPushButton('Usar poder', self)
        self.btn_usar_poder.setGeometry(950, 620, 120, 30)
        self.btn_usar_poder.clicked.connect(self.elegir_target)

        self.btn_cambiar_dados = QPushButton()
        self.btn_cambiar_dados = QPushButton('Cambiar dados', self)
        self.btn_cambiar_dados.setGeometry(1075, 585, 120, 30)
        self.btn_cambiar_dados.clicked.connect(self.cambiar_dados)

        self.btn_dudar = QPushButton()
        self.btn_dudar = QPushButton('Dudar', self)
        self.btn_dudar.setGeometry(1075, 620, 120, 30)
        self.btn_dudar.clicked.connect(self.dudar)

        self.botones = [self.btn_anunciar_valor, self.btn_cambiar_dados, self.btn_dudar,
                        self.btn_pasar_turno, self.btn_usar_poder, self.ingreso_valor]
        for btn in self.botones:
            btn.setFont(font_btn)

        # creamos esto para cuando se use el poder, esta hiden
        self.select_target = QComboBox(self)
        self.select_target.setGeometry(500, 350, 300, 25)
        self.btn_ok = QPushButton()
        self.btn_ok = QPushButton('Confirm target', self)
        self.btn_ok.setGeometry(500, 380, 300, 25)
        self.btn_ok.clicked.connect(self.usar_poder)

    def update_sprites(self, info):
        self.dados = {
            1: os.path.join(*info['RUTA_DICE_1']),
            2: os.path.join(*info['RUTA_DICE_2']),
            3: os.path.join(*info['RUTA_DICE_3']),
            4: os.path.join(*info['RUTA_DICE_4']),
            5: os.path.join(*info['RUTA_DICE_5']),
            6: os.path.join(*info['RUTA_DICE_6'])
        }
        imagen_fondo = QPixmap(os.path.join(*info['RUTA_FONDO_JUEGO']))
        self.background.setPixmap(imagen_fondo)
        for jug in self.jugadores:
            imagen_user = QPixmap(os.path.join(*info['RUTA_USER']))
            imagen_user = imagen_user.scaled(80, 80)
            jug[0].setPixmap(imagen_user)

    def initial_info(self, players, info):
        # Info inicial
        self.vidas_iniciales = info['vidas']
        self.players = players
        self.own_info = info

        # Desplazamos los datos para que el primero sea el player
        pos = int((self.own_info['id'])[-1]) - 1
        self.players = self.players[pos:] + self.players[:pos]
        self.name_players()
        self.new_round(self.players, self.own_info)

    def name_players(self):
        pos = 0
        for player in self.players:
            self.jugadores[pos][1].setText(player[2])
            pos += 1

    def new_round(self, players, info):
        self.players = players
        self.own_info = info
        pos = int((self.own_info['id'])[-1]) - 1
        self.players = self.players[pos:] + self.players[:pos]
        self.new_info()

    def new_info(self):
        # we update las vidas
        corazon_lleno = '♥'
        corazon_vacio = '♡'

        # Info
        vidas_max = self.vidas_iniciales
        pos = 0
        for player in self.players:
            vidas_ac = player[1]
            vidas = corazon_lleno * vidas_ac + corazon_vacio * (vidas_max - vidas_ac)
            self.jugadores[pos][2].setText(vidas)
            self.jugadores[pos][2].resize(self.jugadores[pos][2].sizeHint())
            pos += 1

        # We update los dados del jugador
        for (dado1, dado2) in self.dds:
            dado1.clear()
            dado2.clear()

        dado1 = self.own_info['dado1']
        dado2 = self.own_info['dado2']
        dado1_imagen = QPixmap(self.dados[dado1])
        dado1_imagen = dado1_imagen.scaled(45, 45)
        dado2_imagen = QPixmap(self.dados[dado2])
        dado2_imagen = dado2_imagen.scaled(45, 45)
        self.dado11.setPixmap(dado1_imagen)
        self.dado12.setPixmap(dado2_imagen)
        self.update()

    def next_turn(self, info):
        name = info[0]
        self.numero_turno = info[1]
        self.valor_max = info[2]
        self.puede_cambiar_dados = True
        self.turno_anterior = self.turno_actual
        self.turno_actual = name
        self.error_txt.hide()
        self.select_target.hide()
        self.btn_ok.hide()

        self.turno_ac_txt.setText(f'Turno de {self.turno_actual}')
        self.turno_ac_txt.resize(self.turno_ac_txt.sizeHint())
        self.turno_an_txt.setText(f'Turno anterior fue {self.turno_anterior}')
        self.turno_an_txt.resize(self.turno_an_txt.sizeHint())
        self.num_mayor_txt.setText(f'Numero mayor anunciado: {self.valor_max}')
        self.num_mayor_txt.resize(self.num_mayor_txt.sizeHint())
        self.num_turno_txt.setText(f'Numero turno: {self.numero_turno}')
        self.num_turno_txt.resize(self.num_turno_txt.sizeHint())

        if self.turno_actual == self.own_info['name']:
            for btn in self.botones:
                btn.setEnabled(True)
        else:
            for btn in self.botones:
                btn.setEnabled(False)
            self.ingreso_valor.clear()

    def anunciar_valor(self):
        valor = self.ingreso_valor.text()
        self.senal_anunciar_valor.emit(valor)

    def pasar_turno(self):
        self.senal_pasar_turno.emit()

    def elegir_target(self):
        self.select_target.clear()
        for player in self.players:
            if player[1] > 0:
                self.select_target.addItem(player[2])
        self.select_target.show()
        self.btn_ok.show()

    def usar_poder(self):
        taget_name = self.select_target.currentText()
        self.senal_usar_poder.emit(taget_name)

    def cambiar_dados(self):
        self.senal_cambiar_dados.emit()

    def update_dados(self, info):
        self.own_info = info
        self.btn_cambiar_dados.setEnabled(False)
        self.btn_dudar.setEnabled(False)
        self.new_info()
        self.update()

    def dudar(self):
        self.senal_dudar.emit()

    def show_dados(self, info_dados):
        pos = int((self.own_info['id'])[-1]) - 1
        info_dados = info_dados[pos:] + info_dados[:pos]
        for (dado1, dado2), (info1, info2) in zip(self.dds, info_dados):
            if (info1, info2) != (0, 0):
                dado1_imagen = QPixmap(self.dados[info1])
                dado1_imagen = dado1_imagen.scaled(45, 45)
                dado2_imagen = QPixmap(self.dados[info2])
                dado2_imagen = dado2_imagen.scaled(45, 45)
                dado1.setPixmap(dado1_imagen)
                dado2.setPixmap(dado2_imagen)

    def accion_error(self, msg):
        QMessageBox.information(self, 'Invalid', msg)

    def game_over(self, msg):
        QMessageBox.information(self, 'Game Over', msg)
        for btn in self.botones:
            btn.setEnabled(False)
        self.ingreso_valor.clear()

    def win(self, msg):
        QMessageBox.information(self, 'Win', msg)
        for btn in self.botones:
            btn.setEnabled(False)
        self.ingreso_valor.clear()

    def desconexion_sv(self):
        if self.isVisible():
            QMessageBox.information(self, 'Error', 'Se ha perdido la conexion con el servidor')
        self.close()

    def closeEvent(self, e) -> None:
        self.senal_cerrar_cliente.emit()

    def msg_error(self, msg):
        self.error_txt.setText(msg)
        self.error_txt.resize(self.error_txt.sizeHint())
        self.error_txt.show()
        self.update()
