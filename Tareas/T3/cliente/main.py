from PyQt5.QtWidgets import QApplication
import sys
from frontend.frontend_inicio import VentanaInicio
from backend.backend import Cliente
from frontend.frontend_juego import VentanaJuego


class ShootApplication:
    def __init__(self, port) -> None:
        self.ventana_inicio = VentanaInicio()
        self.back = Cliente(port)
        self.ventana_juego = VentanaJuego()

    def conectar(self) -> None:
        # Inicio
        # Botones
        self.ventana_inicio.senal_cerrar_cliente.connect(self.back.salir)
        self.ventana_inicio.senal_cerrar_cliente.connect(self.salir_inicio)
        self.back.senal_update_inicio.connect(self.ventana_inicio.update_interface)
        self.back.senal_emitir_sprites.connect(self.ventana_inicio.update_sprites)
        self.back.senal_emitir_sprites.connect(self.ventana_juego.update_sprites)

        # Sala y cola
        self.back.senal_sala_llena.connect(self.ventana_inicio.sala_llena)
        self.back.senal_cupo_disp.connect(self.ventana_inicio.cupo_disponible)

        # habilitar y deshabilitar botones
        self.back.senal_not_ingame.connect(self.ventana_inicio.disable)
        self.back.senal_ingame.connect(self.ventana_inicio.enable)

        # Si juego esta iniciado ya
        self.back.senal_juego_iniciado.connect(self.ventana_inicio.partida_en_juego)
        self.back.senal_juego_iniciado.connect(self.ventana_inicio.disable)

        # Inicio del juego
        self.ventana_inicio.senal_iniciar_partida.connect(self.back.iniciar)

        # Juego
        # Inicializar juego
        self.back.senal_close_inicio.connect(self.iniciar_partida)
        self.back.senal_interface_juego.connect(self.ventana_juego.initial_info)

        # Funciones de la partida
        self.back.senal_next_turn.connect(self.ventana_juego.next_turn)
        self.back.senal_new_round.connect(self.ventana_juego.new_round)
        self.back.senal_mostrar_dados.connect(self.ventana_juego.show_dados)

        # Acciones del jugador
        # Anunciar valor
        self.ventana_juego.senal_anunciar_valor.connect(self.back.anunciar_valor)
        self.back.senal_error.connect(self.ventana_juego.msg_error)

        # Cambio dados
        self.ventana_juego.senal_cambiar_dados.connect(self.back.cambiar_dados)
        self.back.senal_cambio_dados_efectivo.connect(self.ventana_juego.update_dados)

        # Dudar
        self.ventana_juego.senal_dudar.connect(self.back.dudar)
        self.back.senal_dudar_error.connect(self.ventana_juego.accion_error)

        # Usar poder
        self.ventana_juego.senal_usar_poder.connect(self.back.usar_poder)
        self.back.senal_poder_error.connect(self.ventana_juego.accion_error)

        # Pasar turno
        self.ventana_juego.senal_pasar_turno.connect(self.back.pasar_turno)

        # Fin del juego
        self.back.senal_game_over.connect(self.ventana_juego.game_over)
        self.back.senal_ganaste.connect(self.ventana_juego.win)
        self.ventana_juego.senal_cerrar_juego.connect(self.close_game)
        self.ventana_juego.senal_cerrar_cliente.connect(self.back.salir)

        # Desconexion del sv
        self.back.senal_sv_error.connect(self.ventana_inicio.desconexion_sv)
        self.back.senal_sv_error.connect(self.ventana_juego.desconexion_sv)

    def iniciar(self) -> None:
        self.ventana_inicio.show()

    def salir_inicio(self):
        self.ventana_inicio.close()

    def iniciar_partida(self):
        self.ventana_inicio.hide()
        self.ventana_juego.show()

    def close_game(self):
        self.ventana_juego.close()


if __name__ == '__main__':
    app = QApplication([])
    if len(sys.argv) > 2:
        port = int(sys.argv[1])
    else:
        port = 69
    game = ShootApplication(port)
    game.conectar()
    game.iniciar()
    sys.exit(app.exec())
