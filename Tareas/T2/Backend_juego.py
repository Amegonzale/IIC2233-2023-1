import os
import parametros as p
from random import uniform
from PyQt5.QtCore import QObject, pyqtSignal, QTimer


class Luigi:
    def __init__(self):
        self.tipo = 'L'
        self.vidas = p.CANTIDAD_VIDAS


class Bloque:
    def __init__(self, tipo, inamovible, inpenetrable, dano, pos):
        self.tipo = tipo
        self.inamovible = inamovible
        self.inpenetrable = inpenetrable
        self.dano = dano
        self.pos = pos
        self.sentido_positivo = True  # sentido respecto los indices del mapa


class Fantasma:
    def __init__(self, tipo, pos):
        super().__init__()
        self.tiempo_movimiento_fantasmas = 1/(uniform(p.MIN_VELOCIDAD, p.MAX_VELOCIDAD))
        self.tipo = tipo
        self.pos = pos
        self.dano = True
        self.sentido = True

        self.timer = QTimer()
        self.timer.setInterval(int(self.tiempo_movimiento_fantasmas*1000))
        self.timer.setSingleShot(True)


class Iniciar(QObject):
    senal_modo_constructor = pyqtSignal()
    senal_modo_jugar = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def seleccionar_juego(self, archivo, nombre):
        if archivo == 'Modo constructor':
            self.senal_modo_constructor.emit()
        else:
            self.senal_modo_jugar.emit(archivo)


class Jugar(QObject):
    senal_comenzar_juego = pyqtSignal()
    senal_instanciar = pyqtSignal()
    senal_cerrar_inicio = pyqtSignal()
    senal_dano = pyqtSignal()
    senal_coords = pyqtSignal(dict)
    senal_icoords = pyqtSignal(dict)
    senal_move_luigi = pyqtSignal(int, int)
    senal_restart = pyqtSignal()
    senal_over_star = pyqtSignal(bool)
    senal_update_vidas = pyqtSignal(str)
    senal_update_time = pyqtSignal(str)
    senal_update_map = pyqtSignal()
    senal_perdiste = pyqtSignal()
    senal_causa = pyqtSignal(str)
    senal_stop = pyqtSignal()
    senal_puntaje = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.grid = []
        self.coords = {}
        self.username = ''
        self.cantidad_vidas = p.CANTIDAD_VIDAS
        self.star = None
        self.star_coords = (0, 0)
        self.over_star = False
        self.over_star_fantama = False
        self.siguente_turno = False
        self.inmortal = False

        self.actual_time = p.TIEMPO_CUENTA_REGRESIVA
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time)
        self.timer.timeout.connect(self.check_timer)

        self.timer_fantasma = QTimer()
        self.timer_fantasma.setInterval(100)
        self.timer_fantasma.timeout.connect(self.update_fantasmas)

    def puntaje(self):
        tiempo = self.actual_time
        multiplicador = p.MULTIPLICADOR_PUNTAJE
        vidas = self.cantidad_vidas
        vidas_inicio = p.CANTIDAD_VIDAS
        puntaje = (tiempo*multiplicador)/(vidas_inicio - vidas + 1)
        self.senal_puntaje.emit(int(puntaje))

    def inmortalidad(self):
        self.inmortal = True

    def start_time(self):
        self.timer.start()
        self.timer_fantasma.start()

    def restart(self):
        self.actual_time = p.TIEMPO_CUENTA_REGRESIVA
        self.cantidad_vidas = p.CANTIDAD_VIDAS
        self.senal_update_vidas.emit(str(self.cantidad_vidas))
        self.inmortal = False
        self.update_time()

    def cargar_archivo(self, nombre_archivo):
        path = os.path.join('mapas', f'{nombre_archivo}.txt')
        with open(path, 'r', encoding='utf-8') as mapa:
            grid = [list(row.strip()) for row in mapa]

        self.comenzar_juego(grid)
        self.senal_cerrar_inicio.emit()

    def comenzar_juego(self, grid):
        for row in range(p.LARGO_GRILLA - 2):
            for col in range(p.ANCHO_GRILLA - 2):
                element = grid[row][col]
                pos = (row, col)
                if element == 'L':
                    self.coords[Luigi()] = pos

        for row in range(p.LARGO_GRILLA - 2):
            for col in range(p.ANCHO_GRILLA - 2):
                element = grid[row][col]
                pos = (row, col)

                if element == 'V':
                    self.coords[Fantasma('V', pos)] = pos

                elif element == 'H':
                    self.coords[Fantasma('H', pos)] = pos

                elif element == 'P':
                    self.coords[Bloque('P', True, True, False, pos)] = pos

                elif element == 'R':
                    self.coords[Bloque('R', False, True, False, pos)] = pos

                elif element == 'F':
                    self.coords[Bloque('F', True, False, True, pos)] = pos

                elif element == 'S':
                    star = Bloque('S', False, False, False, pos)
                    self.coords[star] = pos
                    self.star = star
                    self.star_coords = pos

        self.senal_comenzar_juego.emit()
        self.senal_update_vidas.emit(str(self.cantidad_vidas))
        self.senal_coords.emit(self.coords)
        self.senal_instanciar.emit()
        self.senal_icoords.emit(self.coords)

    def check_timer(self):
        if self.actual_time <= 0:
            self.senal_perdiste.emit()
            self.senal_causa.emit('Te quedaste sin tiempo :(')
            self.senal_stop.emit()

    def moriste(self):
        if not self.inmortal:
            self.cantidad_vidas -= 1
        self.senal_update_vidas.emit(str(self.cantidad_vidas))
        self.senal_dano.emit()
        self.senal_restart.emit()
        if self.cantidad_vidas < 0:
            self.senal_perdiste.emit()
            self.senal_causa.emit('Te quedaste sin vidas, RIP :(')
            self.senal_stop.emit()

    def pausa(self):
        if self.timer.isActive():
            self.timer.stop()
            self.timer_fantasma.stop()
        else:
            self.timer.start()
            self.timer_fantasma.start()

    def update_info(self, coords):
        self.coords = dict(coords)

    def update_star(self):
        self.over_star = False

    def update_time(self):
        mins = (self.actual_time) // 60
        sec = (self.actual_time) % 60
        if sec < 10:
            sec = '0' + str(sec)
        time = str(mins) + ':' + str(sec)
        self.senal_update_time.emit(time)
        if not self.inmortal:
            self.actual_time -= 1

    def update_fantasmas(self):
        coordenadas = dict(self.coords)
        for obj, coords in coordenadas.items():
            if obj is not None and obj.tipo in ['H', 'V']:
                if not obj.timer.isActive():
                    self.validar_mov_fantasma(coords, obj.tipo, obj)
                    obj.timer.start()

        self.senal_coords.emit(self.coords)
        self.senal_update_map.emit()

    def validar_movimiento(self, old_pos, new_pos, direccion):
        new_row = new_pos[0]
        new_col = new_pos[1]
        old_row = old_pos[0]
        old_col = old_pos[1]
        largo_grid = p.LARGO_GRILLA
        ancho_grid = p.ANCHO_GRILLA
        move = True
        star = False

        obj = self.obj_in_pos((new_row, new_col))
        posiciones = self.coords.values()

        if self.over_star:
            star = True

        if not (new_row >= 0 and new_row < largo_grid - 2
                and new_col >= 0 and new_col < ancho_grid - 2):
            move = False

        elif (new_row, new_col) in posiciones and obj.dano:
            move = False
            self.moriste()

        elif (new_row, new_col) in posiciones and obj.inamovible:
            move = False

        elif (new_row, new_col) in posiciones and not obj.inamovible and obj.tipo != 'S':
            if direccion == 'W':
                new_rock_position = (new_row - 1, new_col)

            elif direccion == 'A':
                new_rock_position = (new_row, new_col - 1)

            elif direccion == 'S':
                new_rock_position = (new_row + 1, new_col)

            elif direccion == 'D':
                new_rock_position = (new_row, new_col + 1)

            valid = self.validar_mov_roca(new_rock_position)

            if valid:
                new_row_rock = new_rock_position[0]
                new_col_rock = new_rock_position[1]

                if (new_row, new_col) in posiciones:
                    roca = self.obj_in_pos((new_row, new_col))
                    self.coords[roca] = (new_row_rock, new_col_rock)

                self.senal_update_map.emit()

            else:
                move = False

        elif (new_row, new_col) in posiciones and obj.tipo == 'S':
            self.over_star = True
            print('SOBRE ESTRELLA')

        if move:
            if (old_row, old_col) in posiciones:
                luigi = self.obj_in_pos((old_row, old_col))
                self.coords[luigi] = (new_row, new_col)

            if star:
                self.over_star = False

            self.senal_over_star.emit(self.over_star)
            self.senal_coords.emit(self.coords)
            self.senal_move_luigi.emit(new_row, new_col)

    def validar_mov_roca(self, pos):
        row = pos[0]
        col = pos[1]
        largo_grid = p.LARGO_GRILLA
        ancho_grid = p.ANCHO_GRILLA
        move = True

        if not (row >= 0 and row < largo_grid - 2
                and col >= 0 and col < ancho_grid - 2):
            move = False

        elif (row, col) in self.coords.values():
            move = False

        return move

    def validar_mov_fantasma(self, pos, tipo, fantasma):
        largo_grid = p.LARGO_GRILLA
        ancho_grid = p.ANCHO_GRILLA

        row = pos[0]
        col = pos[1]
        new_row = row
        new_col = col
        posiciones = self.coords.values()

        turn = False
        move = True

        if (row, col) in posiciones:
            sentido = fantasma.sentido

            if tipo == 'V':
                if sentido:
                    new_row = row + 1
                else:
                    new_row = row - 1
            if tipo == 'H':
                if sentido:
                    new_col = col + 1
                else:
                    new_col = col - 1
        else:
            move = False

        obj_frente = self.obj_in_pos((new_row, new_col))

        if (new_row, new_col) in posiciones and obj_frente.tipo == 'L':
            self.moriste()
            move = False
            turn = False

        if not (new_row >= 0 and new_row < largo_grid - 2
                and new_col >= 0 and new_col < ancho_grid - 2):
            move = False
            turn = True

        if move:
            if (new_row, new_col) in posiciones and obj_frente.tipo not in ['L', 'V', 'H']:
                if obj_frente.inpenetrable:
                    turn = True
                    move = False
                elif obj_frente.tipo == 'F':
                    del self.coords[fantasma]
                    move = False

        if move:
            self.coords[fantasma] = (new_row, new_col)

        if turn:
            fantasma.sentido = not fantasma.sentido

    def obj_in_pos(self, pos):
        for obj, coord in self.coords.items():
            if pos == coord:
                return obj
        return None
