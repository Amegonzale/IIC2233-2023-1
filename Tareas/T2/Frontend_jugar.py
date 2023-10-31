import sys
import parametros as p
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton, QGridLayout
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QTimer
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout


class IniciarJugar(QObject):
    def iniciar(self, nombre):
        self.jugar = ModoJugar()
        self.jugar.show()


class ModoJugar(QWidget):
    senal_check_movement = pyqtSignal(tuple, tuple, str)
    senal_update_backend = pyqtSignal(dict)
    senal_ganaste = pyqtSignal()
    senal_not_star = pyqtSignal()
    senal_pausa = pyqtSignal()
    senal_inmortal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_gui()
        self.setFixedSize(720, 532)

    def init_gui(self):
        self.luigi = MovableLuigi('L', (0, 0))
        self.luigi.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.luigi_initial_pos = (0, 0)
        self.coord_elem = {}
        self.initial_coord = {}
        self.over_star = False
        self.juego_pausado = False
        self.teclas_apretadas = set()

        self.timer_key_event = QTimer()
        self.timer_key_event.setInterval(100)
        self.timer_key_event.setSingleShot(True)

        self.iconos_elementos = CargarInfo().cargar_iconos()
        self.sprites_fantasmas = CargarInfo().cargar_iconos_fantasmas()
        self.anim_index = 0

        self.tiempo_txt = QLabel('Tiempo:', self)
        self.tiempo = QLabel('', self)

        self.layout_tiempo = QHBoxLayout()
        self.layout_tiempo.addWidget(self.tiempo_txt)
        self.layout_tiempo.addWidget(self.tiempo)

        self.vidas_txt = QLabel('Vidas:', self)
        self.vidas = QLabel('', self)

        self.layout_vidas = QHBoxLayout()
        self.layout_vidas.addWidget(self.vidas_txt)
        self.layout_vidas.addWidget(self.vidas)

        self.boton_pausa = QPushButton('Pausar', self)
        self.boton_pausa.clicked.connect(self.pausar_juego)

        self.layout_info = QVBoxLayout()
        self.layout_info.addLayout(self.layout_tiempo)
        self.layout_info.addLayout(self.layout_vidas)
        self.layout_info.addWidget(self.boton_pausa)
        self.layout_info.setAlignment(Qt.AlignTop)

        self.boton_limpiar = QPushButton('Limpiar', self)
        self.boton_limpiar.setStyleSheet("color: gray;")
        self.boton_jugar = QPushButton('Jugar', self)
        self.boton_jugar.setStyleSheet("color: gray;")

        self.hbox_botones = QHBoxLayout()
        self.hbox_botones.addWidget(self.boton_limpiar)
        self.hbox_botones.addWidget(self.boton_jugar)
        self.hbox_botones.setAlignment(Qt.AlignBottom)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.layout_info)
        self.vbox.addLayout(self.hbox_botones)

        self.mapa = self.generar_layout_mapa_vacio()

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox)
        self.hbox.addLayout(self.mapa)

        self.setLayout(self.hbox)

    def replay_game(self):
        self.damage_taken()
        self.pausar_juego()

    def pausar_juego(self):
        self.senal_pausa.emit()
        self.juego_pausado = not self.juego_pausado

    def initial_coords(self, coords):
        self.initial_coord = dict(coords)

    def update_time(self, txt):
        self.tiempo.setText(txt)

    def update_vidas(self, vidas):
        self.vidas.setText(vidas)

    def update_layout(self):
        layout = self.hbox.takeAt(1)
        layout.deleteLater()
        self.hbox.addLayout(self.mapa)
        QApplication.processEvents()

    def update_coords(self, coords):
        self.coord_elem = coords

    def update_over_star(self, esta_sobre):
        self.over_star = esta_sobre

    def update_mapa(self):
        indice = 0
        while self.mapa.count() > 0:
            widget = self.mapa.takeAt(indice)
            if not isinstance(widget.widget(), MovableLuigi):
                widget.widget().deleteLater()

        new_mapa = self.generar_layout_mapa_vacio()

        for obj, coord in self.coord_elem.items():
            if obj is not None:
                if obj.tipo in self.iconos_elementos.keys():
                    elem = QLabel(obj.tipo, self)
                    elem.resize(32, 32)
                    elem.setPixmap(QIcon(self.iconos_elementos[obj.tipo]).pixmap(32, 32))
                    elem.setStyleSheet('background-color: grey;')
                    new_mapa.addWidget(elem, coord[0] + 1, coord[1] + 1)

                if obj.tipo in self.sprites_fantasmas.keys():
                    if obj.tipo == 'V':
                        fantasma = QLabel(obj.tipo, self)
                        fantasma.resize(32, 32)
                        ruta = self.sprites_fantasmas['V'][self.anim_index]
                        icon = QIcon(ruta).pixmap(32, 32)
                        self.anim_index = (self.anim_index + 1) % 3
                        fantasma.setPixmap(icon)
                        fantasma.setStyleSheet('background-color: grey;')
                        new_mapa.addWidget(fantasma, coord[0] + 1, coord[1] + 1)

                    if obj.tipo == 'H':
                        if obj.sentido:
                            sentido = 'R'
                        else:
                            sentido = 'L'
                        fantasma = QLabel(obj.tipo, self)
                        fantasma.resize(32, 32)
                        ruta = self.sprites_fantasmas['H'][sentido][self.anim_index]
                        icon = QIcon(ruta).pixmap(32, 32)
                        self.anim_index = (self.anim_index + 1) % 3
                        fantasma.setPixmap(icon)
                        fantasma.setStyleSheet('background-color: grey;')
                        new_mapa.addWidget(fantasma, coord[0] + 1, coord[1] + 1)

                if obj.tipo == 'L':
                    self.luigi.pos = (coord[0] + 1, coord[1] + 1)
                    self.luigi.setStyleSheet('background-color: grey;')
                    new_mapa.addWidget(self.luigi, coord[0] + 1, coord[1] + 1)

        self.luigi.raise_()
        self.mapa = new_mapa
        self.update_layout()

    def move_luigi(self, row, col):
        self.luigi.pos = (row + 1, col + 1)
        self.mapa.addWidget(self.luigi, row + 1, col + 1)

    def move_to_start(self):
        self.move_luigi(self.luigi_initial_pos[0], self.luigi_initial_pos[1])

    def damage_taken(self):
        self.coord_elem = dict(self.initial_coord)
        self.senal_update_backend.emit(self.coord_elem)
        self.update_mapa()
        self.luigi.raise_()

    def keyPressEvent(self, e):
        self.teclas_apretadas.add(e.key())
        key = e.key()
        row = self.luigi.pos[0]
        col = self.luigi.pos[1]
        check_position = False

        if key == Qt.Key_W:
            if not self.timer_key_event.isActive() and not self.juego_pausado:
                self.luigi.sprites_actuales = self.luigi.sprites['W']
                direccion = 'W'
                row -= 1
                check_position = True
                self.timer_key_event.start()
        elif key == Qt.Key_S:
            if not self.timer_key_event.isActive() and not self.juego_pausado:
                self.luigi.sprites_actuales = self.luigi.sprites['S']
                direccion = 'S'
                row += 1
                check_position = True
                self.timer_key_event.start()
        elif key == Qt.Key_A:
            if not self.timer_key_event.isActive() and not self.juego_pausado:
                self.luigi.sprites_actuales = self.luigi.sprites['A']
                direccion = 'A'
                col -= 1
                check_position = True
                self.timer_key_event.start()
        elif key == Qt.Key_D:
            if not self.timer_key_event.isActive() and not self.juego_pausado:
                self.luigi.sprites_actuales = self.luigi.sprites['D']
                direccion = 'D'
                col += 1
                check_position = True
                self.timer_key_event.start()

        elif key == Qt.Key_G:
            if self.over_star and not self.juego_pausado:
                self.senal_ganaste.emit()
                self.senal_not_star.emit()
                self.pausar_juego()

        elif key == Qt.Key_P:
            self.pausar_juego()

        if check_position:
            new_pos = (row - 1, col - 1)
            old_pos = (self.luigi.pos[0] - 1, self.luigi.pos[1] - 1)
            self.senal_check_movement.emit(old_pos, new_pos, direccion)

        if {Qt.Key_K, Qt.Key_I, Qt.Key_L}.issubset(self.teclas_apretadas):
            coordenadas = dict(self.coord_elem)
            for obj in coordenadas.keys():
                if obj is not None and obj.tipo in ['H', 'V']:
                    del self.coord_elem[obj]
            self.senal_update_backend.emit(self.coord_elem)

        if {Qt.Key_I, Qt.Key_N, Qt.Key_F}.issubset(self.teclas_apretadas):
            self.senal_inmortal.emit()

        e.accept()

    def keyReleaseEvent(self, e):
        self.luigi.sprites_actuales = self.luigi.sprites['Quieto']
        self.teclas_apretadas = set()
        e.accept()

    def generar_layout_mapa_vacio(self):
        layout_mapa = QGridLayout()
        layout_mapa.setSpacing(1)

        for row in range(p.LARGO_GRILLA):
            for col in range(p.ANCHO_GRILLA):
                if row in [0, p.LARGO_GRILLA - 1] or col in [0, p.ANCHO_GRILLA - 1]:
                    bordermap = QLabel('B', self)
                    bordermap.setPixmap(QPixmap(p.RUTA_BORDERMAP))
                    bordermap.resize(32, 32)
                    bordermap.setStyleSheet('background-color: grey;')
                    layout_mapa.addWidget(bordermap, row, col)
                else:
                    widget = QLabel(' ', self)
                    widget.resize(32, 32)
                    widget.setStyleSheet('background-color: grey;')
                    layout_mapa.addWidget(widget, row, col)

        return layout_mapa


class MovableLuigi(QWidget):
    def __init__(self, tipo, pos):
        super().__init__()
        self.tipo = tipo
        self.pos = pos
        self.label = QLabel(self)
        self.setFocusPolicy(Qt.StrongFocus)
        self.sprites = {'W': p.RUTAS_LUIGI_UP,
                        'A': p.RUTAS_LUIGI_LEFT,
                        'S': p.RUTAS_LUIGI_DOWN,
                        'D': p.RUTAS_LUIGI_RIGHT,
                        'Quieto': [p.RUTA_LUIGI, p.RUTA_LUIGI, p.RUTA_LUIGI]}
        self.sprites_actuales = self.sprites['Quieto']
        self.index = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.animar)
        self.timer.start(100)

    def animar(self):
        icon = QPixmap(self.sprites_actuales[self.index])
        self.label.setPixmap(icon)
        self.index = (self.index + 1) % len(self.sprites_actuales)


class CargarInfo:
    def cargar_iconos(self):
        nombres_y_rutas = {}

        nombres_y_rutas['F'] = p.RUTA_FIRE
        nombres_y_rutas['R'] = p.RUTA_ROCK
        nombres_y_rutas['P'] = p.RUTA_WALL
        nombres_y_rutas['S'] = p.RUTA_STAR

        return nombres_y_rutas

    def cargar_iconos_fantasmas(self):
        fantasmas = {}
        fantasmas['V'] = p.RUTAS_VERTICAL_GHOST
        fantasmas['H'] = {'L': p.RUTAS_HORIZONTAL_GHOST_LEFT,
                          'R': p.RUTAS_HORIZONTAL_GHOST_RIGHT}
        return fantasmas


if __name__ == '__main__':
    app = QApplication([])
    game = ModoJugar()
    game.show()
    sys.exit(app.exec())
