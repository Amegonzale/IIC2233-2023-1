import socket
import threading
import json
import os
from Scripts import cripto
from PyQt5.QtCore import pyqtSignal, QObject


class Cliente(QObject):
    senal_emitir_sprites = pyqtSignal(dict)
    senal_update_inicio = pyqtSignal(int, list)
    senal_sala_llena = pyqtSignal()
    senal_cupo_disp = pyqtSignal()
    senal_not_ingame = pyqtSignal()
    senal_ingame = pyqtSignal()
    senal_interface_juego = pyqtSignal(list, dict)
    senal_close_inicio = pyqtSignal()
    senal_juego_iniciado = pyqtSignal()

    senal_next_turn = pyqtSignal(list)
    senal_error = pyqtSignal(str)
    senal_cambio_dados_efectivo = pyqtSignal(dict)
    senal_dudar_error = pyqtSignal(str)
    senal_poder_error = pyqtSignal(str)
    senal_new_round = pyqtSignal(list, dict)
    senal_game_over = pyqtSignal(str)
    senal_ganaste = pyqtSignal(str)
    senal_mostrar_dados = pyqtSignal(list)

    senal_sv_error = pyqtSignal()

    def __init__(self, port):
        super().__init__()
        self.host = self.client_info()["host"]
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.num = self.client_info()["N"]
        self.info_juego = None

        try:
            self.client_info()
            self.connect_to_server()
            self.initBackend()
            self.listen()
        except ConnectionError:
            print('Conexion terminada')
            self.socket_cliente.close()
            self.isConnected = False

    def client_info(self):
        with open(os.path.join('cliente', 'parametros.json')) as info:
            client_info = json.load(info)
        return client_info

    def initBackend(self):
        self.isConnected = True

    def connect_to_server(self):
        self.socket_cliente.connect((self.host, self.port))

    def listen(self):
        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def listen_thread(self):
        while self.isConnected:
            try:
                data = self.socket_cliente.recv(2**16)
                mensaje = cripto.recibir(data, self.num)
                self.procesar_mensaje(mensaje)
            except ConnectionResetError:
                # Aqui se maneja la desconexion del sv
                self.senal_sv_error.emit()
                self.isConnected = False
                self.socket_cliente.close()

    # Aqui se manejan los mensajes del sv
    def procesar_mensaje(self, mensaje):
        accion = mensaje[0]
        if accion == 'update inicio':
            self.senal_emitir_sprites.emit(self.client_info())
            self.senal_update_inicio.emit(*mensaje[1])

        elif accion == 'sala llena':
            self.senal_sala_llena.emit()
            self.senal_not_ingame.emit()

        elif accion == 'cupo disponible':
            self.senal_cupo_disp.emit()
            self.senal_ingame.emit()

        elif accion == 'partida en juego':
            self.senal_juego_iniciado.emit()

        elif accion == 'start game':
            self.info_juego = mensaje[1][1]
            interface = mensaje[1][0]
            self.senal_interface_juego.emit(interface, self.info_juego)
            self.senal_close_inicio.emit()

        elif accion == 'next turn':
            self.senal_next_turn.emit(mensaje[1])

        elif accion == 'error':
            self.senal_error.emit(mensaje[1][0])

        elif accion == 'show dados':
            self.senal_mostrar_dados.emit(mensaje[1])

        elif accion == 'cambiar dados':
            self.senal_cambio_dados_efectivo.emit(mensaje[1])

        elif accion == 'no duda':
            self.senal_dudar_error.emit(mensaje[1][0])

        elif accion == 'no poder':
            self.senal_poder_error.emit(mensaje[1][0])

        elif accion == 'new round':
            self.senal_new_round.emit(*mensaje[1])

        elif accion == 'game over':
            self.senal_game_over.emit(mensaje[1][0])
            self.isConnected = False

        elif accion == 'u win':
            self.senal_ganaste.emit(mensaje[1][0])
            self.isConnected = False

    # Los metodos de abajo se encargan de enviar info al sv
    def enviar_info(self, info):
        self.socket_cliente.send(cripto.enviar(info, self.num))

    def iniciar(self):
        self.enviar_info(['iniciar'])

    def salir(self):
        if self.isConnected:
            self.enviar_info(['salir'])
        self.isConnected = False

    def anunciar_valor(self, valor):
        self.enviar_info(['anunciar valor', valor])

    def pasar_turno(self):
        self.enviar_info(['pasar turno'])

    def cambiar_dados(self):
        self.enviar_info(['cambiar dados'])

    def dudar(self):
        self.enviar_info(['dudar'])

    def usar_poder(self, target_id):
        self.enviar_info(['usar poder', target_id])
