import parametros as p
from PyQt5.QtGui import QPixmap, QIcon, QDrag
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QMimeData
from PyQt5.QtWidgets import QComboBox, QPushButton, QGridLayout
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout


class IniciarConstructor(QObject):
    def iniciar(self, nombre):
        self.constructor = ModoConstructor()
        self.constructor.show()


class ModoConstructor(QWidget):
    lista_grid = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.init_gui()
        self.setFixedSize(720, 522)
        self.setAcceptDrops(True)

    def init_gui(self):
        self.title = "Constructor"
        self.setWindowTitle(self.title)
        self.iconos = CargarInfo().cargar_iconos()
        self.cantidades = CargarInfo().cargar_cantidades()
        self.generar_layout()

    def generar_layout(self):
        self.selector_categoria = QComboBox(self)
        self.selector_categoria.addItems(['Todos', 'Bloques', 'Entidades'])
        self.selector_categoria.setGeometry(50, 50, 300, 20)
        self.selector_categoria.activated.connect(self.update_botones)

        self.layout_botones = None
        self.layout_botones = self.generar_layout_botones()
        self.layout_botones.setSpacing(5)
        self.layout_botones.setAlignment(Qt.AlignCenter)

        self.boton_limpiar = QPushButton('Limpiar', self)
        self.boton_limpiar.clicked.connect(self.limpiar_mapa)

        self.boton_jugar = QPushButton('Jugar', self)
        self.boton_jugar.clicked.connect(self.jugar)

        self.hbox_botones = QHBoxLayout()
        self.hbox_botones.addWidget(self.boton_limpiar)
        self.hbox_botones.addWidget(self.boton_jugar)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.selector_categoria)
        self.vbox.addLayout(self.layout_botones)
        self.vbox.addLayout(self.hbox_botones)

        self.layout_mapa = self.generar_layout_mapa_vacio()

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox)
        self.hbox.addLayout(self.layout_mapa)

        self.setLayout(self.hbox)

    def update_botones(self):
        if self.vbox.itemAt(2) == self.hbox_botones:
            self.vbox.takeAt(2)

        self.layout_botones = self.generar_layout_botones()
        self.layout_botones.setAlignment(Qt.AlignCenter)
        self.vbox.addLayout(self.layout_botones)

        if self.vbox.itemAt(2) != self.hbox_botones:
            self.vbox.takeAt(1)
            self.vbox.addLayout(self.hbox_botones)

    def limpiar_mapa(self):
        self.cantidades = CargarInfo().cargar_cantidades()
        self.layout_mapa = self.generar_layout_mapa_vacio()
        self.update_botones()
        self.hbox.takeAt(1)
        self.hbox.addLayout(self.layout_mapa)

    def generar_layout_botones(self):
        # encontrar una forma de borrar los botones si es q hay
        if self.layout_botones is not None:
            while self.layout_botones.count():
                boton = self.layout_botones.takeAt(0)
                boton.widget().deleteLater()

        categoria = self.selector_categoria.currentText()

        # vemos que categoria se eligio y hacemos la lista de los botones
        # que debemos mostrar
        if categoria == 'Todos':
            iconos_botones = []
            for nombre, icono in self.iconos.items():
                iconos_botones.append(icono)

        elif categoria == 'Bloques':
            iconos_botones = [self.iconos['Pared'], self.iconos['Rock'],
                              self.iconos['Fire'], self.iconos['Star']]

        elif categoria == 'Entidades':
            iconos_botones = [self.iconos['Luigi'], self.iconos['Vertical ghost'],
                              self.iconos['Horizontal ghost']]

        # Ahora hacemos un grid vertical para posicionar los botones ><
        layout_botones = QVBoxLayout()

        # Añadimos los botones al grid, primero los creamos
        # luego le añadimos el icono
        for icon in iconos_botones:
            for nombre, ruta in self.iconos.items():
                if ruta == icon:
                    text = nombre
                    cantidad = f' ({str(self.cantidades[text[0]])})'
            boton = DragButton(text + cantidad, self)
            boton.setIcon(QIcon(icon))
            layout_botones.addWidget(boton)

        return layout_botones

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

    def grid_a_lista(self):
        grid = []
        for row in range(1, p.LARGO_GRILLA - 1):
            fila = []
            for col in range(p.ANCHO_GRILLA):
                info = self.layout_mapa.itemAtPosition(row, col)
                info = info.widget().text()
                if info == ' ':
                    fila.append('-')
                elif info == '':
                    continue
                else:
                    fila.append(info)
            grid.append(fila)

        return grid

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()
        texto_widget = (widget.text())[0]
        cantidad_item = self.cantidades[texto_widget]

        widget_dropeado = self.childAt(pos.x(), pos.y())
        index = self.layout_mapa.indexOf(widget_dropeado)

        newLabel = QLabel(widget.text(), self)
        icon = widget.icon()
        newLabel.setPixmap(icon.pixmap(32, 32))
        newLabel.setStyleSheet('background-color: grey;')

        if index != -1 and widget_dropeado.text() == ' ' and cantidad_item > 0:
            row = index // 11
            col = index % 11
            widget_dropeado.setText(texto_widget)
            self.layout_mapa.addWidget(newLabel, row, col)
            self.cantidades[texto_widget] -= 1
            self.update_botones()

        elif index != -1 and widget_dropeado.text() != ' ' and cantidad_item > 0:
            self.ventana_error = VentanaEspacioOcupado()
            self.ventana_error.show()

        e.accept()

    def jugar(self):
        grid = self.grid_a_lista()
        if self.cantidades['L'] == 0 and self.cantidades['S'] == 0:
            self.lista_grid.emit(grid)
            self.close()
        else:
            self.ventana_error = VentanaFaltaLuigi()
            self.ventana_error.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.boton_jugar.click()


class VentanaEspacioOcupado(QWidget):
    def __init__(self):
        super().__init__()
        self.init_gui()
        self.setFixedSize(400, 200)

    def init_gui(self):
        self.title = "Casilla invalida"
        self.setWindowTitle(self.title)
        texto = 'Casilla invalida: la casilla ya esta ocupada por otro elemento :('
        self.text = QLabel(texto, self)

        self.boton_salir = QPushButton('Entendido', self)
        self.boton_salir.resize(self.boton_salir.sizeHint())
        self.boton_salir.clicked.connect(self.close)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.boton_salir)

        self.setLayout(self.vbox)


class VentanaFaltaLuigi(QWidget):
    def __init__(self):
        super().__init__()
        self.init_gui()
        self.setFixedSize(400, 200)

    def init_gui(self):
        self.title = "Error"
        self.setWindowTitle(self.title)
        texto = '''                 No se puede inicializar el juego
                si no esta Luigi y una estrella presente'''
        self.text = QLabel(texto, self)

        self.boton_salir = QPushButton('Entendido', self)
        self.boton_salir.resize(self.boton_salir.sizeHint())
        self.boton_salir.clicked.connect(self.close)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.boton_salir)

        self.setLayout(self.vbox)


class DragButton(QPushButton):

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = self.icon().pixmap(32, 32)
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)


class CargarInfo:

    def cargar_iconos(self):
        nombres_y_rutas = {}

        nombres_y_rutas['Fire'] = p.RUTA_FIRE
        nombres_y_rutas['Rock'] = p.RUTA_ROCK
        nombres_y_rutas['Pared'] = p.RUTA_WALL
        nombres_y_rutas['Star'] = p.RUTA_STAR
        nombres_y_rutas['Luigi'] = p.RUTA_LUIGI
        nombres_y_rutas['Vertical ghost'] = p.RUTA_FANTASMA_VERTICAL
        nombres_y_rutas['Horizontal ghost'] = p.RUTA_FANTASMA_HORIZONTAL

        return nombres_y_rutas

    def cargar_cantidades(self):
        cantidades = {}

        cantidades['F'] = int(p.MAXIMO_FUEGO)
        cantidades['S'] = int(p.CANTIDAD_STAR)
        cantidades['R'] = int(p.MAXIMO_ROCA)
        cantidades['P'] = int(p.MAXIMO_PARED)
        cantidades['L'] = int(p.CANTIDAD_LUIGI)
        cantidades['V'] = int(p.MAXIMO_FANTASMAS_VERTICAL)
        cantidades['H'] = int(p.MAXIMO_FANTASMAS_HORIZONTAL)

        return cantidades
