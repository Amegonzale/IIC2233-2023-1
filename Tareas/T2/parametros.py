import os
ANCHO_GRILLA = 11
LARGO_GRILLA = 16
MIN_CARACTERES = 3
MAX_CARACTERES = 15

RUTA_FONDO = os.path.join('sprites', 'Fondos', 'fondo_inicio.png')
RUTA_LOGO = os.path.join('sprites', 'Elementos', 'logo.png')
RUTA_FIRE = os.path.join('sprites', 'Elementos', 'fire.png')
RUTA_STAR = os.path.join('sprites', 'Elementos', 'osstar.png')
RUTA_ROCK = os.path.join('sprites', 'Elementos', 'rock.png')
RUTA_WALL = os.path.join('sprites', 'Elementos', 'wall.png')
RUTA_LUIGI = os.path.join('sprites', 'Personajes', 'luigi_front.png')
RUTA_FANTASMA_VERTICAL = os.path.join('sprites', 'Personajes', 'red_ghost_vertical_1.png')
RUTA_FANTASMA_HORIZONTAL = os.path.join('sprites', 'Personajes', 'white_ghost_left_1.png')
RUTA_ELEMENTOS = os.path.join('sprites', 'Elementos')
RUTA_BORDERMAP = os.path.join('sprites', 'Elementos', 'bordermap.png')

RUTAS_LUIGI_DOWN = [os.path.join('sprites', 'Personajes', 'luigi_down_1.png'),
                    os.path.join('sprites', 'Personajes', 'luigi_down_2.png'),
                    os.path.join('sprites', 'Personajes', 'luigi_down_3.png')]

RUTAS_LUIGI_UP = [os.path.join('sprites', 'Personajes', 'luigi_up_1.png'),
                  os.path.join('sprites', 'Personajes', 'luigi_up_2.png'),
                  os.path.join('sprites', 'Personajes', 'luigi_up_3.png')]

RUTAS_LUIGI_LEFT = [os.path.join('sprites', 'Personajes', 'luigi_left_1.png'),
                    os.path.join('sprites', 'Personajes', 'luigi_left_2.png'),
                    os.path.join('sprites', 'Personajes', 'luigi_left_3.png')]

RUTAS_LUIGI_RIGHT = [os.path.join('sprites', 'Personajes', 'luigi_rigth_1.png'),
                     os.path.join('sprites', 'Personajes', 'luigi_rigth_2.png'),
                     os.path.join('sprites', 'Personajes', 'luigi_rigth_3.png')]

RUTAS_VERTICAL_GHOST = [os.path.join('sprites', 'Personajes', 'red_ghost_vertical_1.png'),
                        os.path.join('sprites', 'Personajes', 'red_ghost_vertical_2.png'),
                        os.path.join('sprites', 'Personajes', 'red_ghost_vertical_3.png')]

RUTAS_HORIZONTAL_GHOST_LEFT = [os.path.join('sprites', 'Personajes', 'white_ghost_left_1.png'),
                               os.path.join('sprites', 'Personajes', 'white_ghost_left_2.png'),
                               os.path.join('sprites', 'Personajes', 'white_ghost_left_3.png')]

RUTAS_HORIZONTAL_GHOST_RIGHT = [os.path.join('sprites', 'Personajes', 'white_ghost_rigth_1.png'),
                                os.path.join('sprites', 'Personajes', 'white_ghost_rigth_2.png'),
                                os.path.join('sprites', 'Personajes', 'white_ghost_rigth_3.png')]


CANTIDAD_STAR = 1
CANTIDAD_LUIGI = 1

MAXIMO_ROCA = 3
MAXIMO_PARED = 6
MAXIMO_FUEGO = 2
MAXIMO_FANTASMAS_VERTICAL = 2
MAXIMO_FANTASMAS_HORIZONTAL = 2

CANTIDAD_VIDAS = 3

MIN_VELOCIDAD = 5
MAX_VELOCIDAD = 20

TIEMPO_CUENTA_REGRESIVA = 40
MULTIPLICADOR_PUNTAJE = 100

AUDIO_WIN = os.path.join('sounds', 'stageClear.wav')
AUDIO_LOSS = os.path.join('sounds', 'gameOver.wav')
