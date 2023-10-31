from PyQt5.QtWidgets import QApplication
from Frontend_inicio import VentanaInicio
from Backend_inicio import ProcesadorInicio
from Backend_juego import Iniciar, Jugar
from Frontend_constructor import IniciarConstructor, ModoConstructor
from Frontend_jugar import ModoJugar, IniciarJugar
from Frontend_final import VentanaWin, VentanaLoss

import sys


class ShootApplication:
    def __init__(self) -> None:
        self.ventana_inicio = VentanaInicio()
        self.procesador = ProcesadorInicio()
        self.backend_iniciar = Iniciar()
        self.iniciar_construc = IniciarConstructor()
        self.backend_jugar = Jugar()
        self.frontend_constructor = ModoConstructor()
        self.frontend_jugar = ModoJugar()
        self.iniciar_juego = IniciarJugar()
        self.end_game_screen = VentanaWin()
        self.perdiste_jaja = VentanaLoss()

    def conectar(self) -> None:
        # Cargar mapas al selector
        self.procesador.senal_mapas.connect(self.ventana_inicio.actualizar_selector)
        self.procesador.lista_mapas()

        # Validar username
        self.ventana_inicio.senal_procesar_user.connect(self.procesador.username_valido)
        self.procesador.senal_valid_username.connect(self.ventana_inicio.enviar_info)

        # Pasamos info al backend del juego
        self.ventana_inicio.senal_info.connect(self.backend_iniciar.seleccionar_juego)

        # Selecciono que tipo de ventana se iniciara (cargar o crear)
        # Si se selecciona el constructor entonces abre self.constructor
        self.backend_iniciar.senal_modo_constructor.connect(self.constructor)

        # Si se selecciona algun mapa prehecho entonces carga el mapa y luego lo abre
        self.backend_iniciar.senal_modo_jugar.connect(self.backend_jugar.cargar_archivo)
        self.backend_jugar.senal_cerrar_inicio.connect(self.jugar_premade)

        # Inicializa todo
        self.frontend_constructor.lista_grid.connect(self.backend_jugar.comenzar_juego)
        self.backend_jugar.senal_instanciar.connect(self.frontend_jugar.update_mapa)
        self.backend_jugar.senal_comenzar_juego.connect(self.jugar_construido)
        self.backend_jugar.senal_comenzar_juego.connect(self.backend_jugar.start_time)

        # Mover a luigi
        self.frontend_jugar.senal_check_movement.connect(self.backend_jugar.validar_movimiento)
        self.backend_jugar.senal_move_luigi.connect(self.frontend_jugar.move_luigi)

        # Reiniciar todo cuando se hace daño
        self.backend_jugar.senal_icoords.connect(self.frontend_jugar.initial_coords)
        self.backend_jugar.senal_dano.connect(self.frontend_jugar.damage_taken)
        self.backend_jugar.senal_restart.connect(self.frontend_jugar.move_to_start)
        self.frontend_jugar.senal_update_backend.connect(self.backend_jugar.update_info)

        # Update info: coordenadas, tiempo, vidas, mapa y si esta sobre una estrella
        self.backend_jugar.senal_coords.connect(self.frontend_jugar.update_coords)
        self.backend_jugar.senal_update_time.connect(self.frontend_jugar.update_time)
        self.backend_jugar.senal_update_vidas.connect(self.frontend_jugar.update_vidas)
        self.backend_jugar.senal_update_map.connect(self.frontend_jugar.update_mapa)
        self.backend_jugar.senal_over_star.connect(self.frontend_jugar.update_over_star)

        # Pausa e inmortalidad
        self.frontend_jugar.senal_pausa.connect(self.backend_jugar.pausa)
        self.frontend_jugar.senal_inmortal.connect(self.backend_jugar.inmortalidad)

        # Perder el juego
        self.backend_jugar.senal_perdiste.connect(self.perdiste)
        self.backend_jugar.senal_perdiste.connect(self.backend_jugar.puntaje)
        self.backend_jugar.senal_puntaje.connect(self.perdiste_jaja.set_puntaje)
        self.backend_jugar.senal_causa.connect(self.perdiste_jaja.update_causa)
        self.backend_jugar.senal_stop.connect(self.frontend_jugar.pausar_juego)
        self.procesador.senal_username.connect(self.perdiste_jaja.update_user)

        # Reiniciar el juego una vez pierdes
        self.perdiste_jaja.senal_replay.connect(self.jugar_construido)
        self.perdiste_jaja.senal_replay.connect(self.backend_jugar.restart)
        self.perdiste_jaja.senal_info_replay.connect(self.frontend_jugar.replay_game)

        # Ganar el juego
        self.frontend_jugar.senal_ganaste.connect(self.end_game)
        self.frontend_jugar.senal_ganaste.connect(self.backend_jugar.puntaje)
        self.backend_jugar.senal_puntaje.connect(self.end_game_screen.set_puntaje)
        self.frontend_jugar.senal_not_star.connect(self.backend_jugar.update_star)
        self.procesador.senal_username.connect(self.end_game_screen.update_user)

        # Reiniciar el juego una vez ganas
        self.end_game_screen.senal_replay.connect(self.jugar_construido)
        self.end_game_screen.senal_replay.connect(self.backend_jugar.restart)
        self.end_game_screen.senal_info_replay.connect(self.frontend_jugar.replay_game)

    def iniciar(self) -> None:
        self.ventana_inicio.show()

    def constructor(self):
        self.ventana_inicio.close()
        self.frontend_constructor.show()

    def jugar_construido(self):
        self.frontend_constructor.close()
        self.frontend_jugar.show()

    def jugar_premade(self):
        self.ventana_inicio.close()

    def perdiste(self):
        self.perdiste_jaja.show()
        self.frontend_jugar.close()

    def end_game(self):
        self.frontend_jugar.close()
        self.end_game_screen.show()


if __name__ == '__main__':
    app = QApplication([])
    game = ShootApplication()
    game.conectar()
    game.iniciar()
    sys.exit(app.exec())
