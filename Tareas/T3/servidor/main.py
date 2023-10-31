import socket
import json
import os
import sys
import threading
from Scripts import cripto
from bot import Bot
import metodos_auxiliares as m
from time import sleep
import random


class Servidor:

    def __init__(self, port):
        self.lok = threading.Lock()
        self.max_recv = 2**16
        self.host = self.server_info()["host"]
        self.port = port
        self.num = self.server_info()["N"]
        self.ids = ['id_1', 'id_2', 'id_3', 'id_4']
        self.nombres = [
            self.server_info()["id_1"], self.server_info()["id_2"],
            self.server_info()["id_3"], self.server_info()["id_4"],
            self.server_info()["id_5"], self.server_info()["id_6"],
            self.server_info()["id_7"], self.server_info()["id_8"]
                        ]
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets = {}   # Incluye todos los clientes que se quieren conectar
        self.skts_conectados = {}  # Incluye solo a los conectados
        self.players_info = {}  # Incluye info jugadores de la partida iniciada (bots tmb)
        self.en_juego = False  # Indica si esta iniciado el juego o no
        self.max_players = self.server_info()["NUMERO_JUGADORES"]
        self.num_ronda = 1
        self.prob = (self.server_info()['PROB_DUDAR'], self.server_info()['PROB_ANUNCIAR'])
        self.bot = Bot(*self.prob)  # Se instancia el bot que se usara
        self.valor_anunciado = {'valor': 0, 'id': None, 'mintiendo': True}
        self.maximo_anunciado = 0
        self.turno_actual = -1
        self.numero_turno = 0
        self.turno_players = {'turno anterior': '', 'turno actual': ''}
        self.vidas_ini = self.server_info()['NUMERO_VIDAS']
        self.valor_paso = self.server_info()['VALOR_PASO']
        self.win = False
        self.bind_listen()
        self.accept_connections()
        self.is_online = True
        self.online()

    def server_info(self):
        with open(os.path.join('servidor', 'parametros.json')) as info:
            server_info = json.load(info)
        return server_info

    def enviar_info(self, msg, skt):
        with self.lok:
            skt.send(cripto.enviar(msg, self.num))

    def online(self):
        while self.is_online:
            pass

    def bind_listen(self):
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()

    def accept_connections(self):
        print('----------------------------')
        thread = threading.Thread(target=self.accept_connections_thread, daemon=True)
        thread.start()

    def accept_connections_thread(self):
        server_conectado = True
        while server_conectado:
            try:
                # Recibo la info y le busco un id y usuario
                client_socket, address = self.socket_server.accept()
                connected = True
                if self.en_juego:
                    connected = False
                    self.partida_en_juego(client_socket)
                elif len(self.sockets) >= self.max_players:
                    connected = False
                    self.sala_llena(client_socket)

                username = m.asignar_nombre(self.nombres)
                self.sockets[client_socket] = {'username': username}
                m.log_player_conectado(username)

                # Si no esta lleno ni en partida lo conectamos
                if connected:
                    self.connect_player(client_socket)
                else:
                    self.sockets[client_socket]['connected'] = connected
                # thread
                listening_client_thread = threading.Thread(
                    target=self.listen_client_thread,
                    args=(client_socket, ), daemon=True)

                # inicio el thread y actualizo la interface de todos.
                listening_client_thread.start()
                if not self.en_juego:
                    self.update_interface_inicio()
            except (OSError, KeyboardInterrupt):
                print('☆ Se cerro el servidor uwu ☆')
                server_conectado = False
                self.is_online = False

    def connect_player(self, client_socket):
        identificacion = m.asignar_id(self.ids)
        # lo añado a los diccionarios
        self.sockets[client_socket]['id'] = identificacion
        self.sockets[client_socket]['connected'] = True
        self.skts_conectados[identificacion] = client_socket

    def listen_client_thread(self, client_socket):
        client_is_connected = True
        # este aproach sirve pues solo funciona si es que client skt existe
        # si no existe es pq se salio entonces seteamos que esta desconectado
        while client_is_connected:
            try:
                # vemos cuantos bytes hay en el mensaje
                largo_msg = client_socket.recv(4)
                largo = cripto.desencriptar_largo(largo_msg)
                chunk = 128
                numero_chunks = (largo // chunk) + 1
                cantidad_bytes = (numero_chunks) * chunk + 4 * numero_chunks

                # si el mensaje pasa de 2^16 bytes lo cortamos xd
                if cantidad_bytes > self.max_recv:
                    cantidad_bytes = self.max_recv

                # Recibimos de a chunks de 4096 o menos :P
                m_encriptado = bytearray()
                while len(m_encriptado) < cantidad_bytes:
                    bytes_leer = min(4096, cantidad_bytes - len(m_encriptado))
                    respuesta = client_socket.recv(bytes_leer)
                    m_encriptado.extend(respuesta)

                # Aqui decodificamos y desencriptamos el mensaje
                mensaje = cripto.recibir(largo_msg + m_encriptado, self.num)
                self.procesar_info(mensaje, client_socket)

            # Lo atrapamos cuando se desconecta y lo sacamos del while
            except (ConnectionResetError, OSError):
                client_is_connected = False

    def procesar_info(self, msg, skt):
        accion = msg[0]

        if accion == 'salir':
            self.update_connected_players(skt)
        elif accion == 'iniciar':
            self.en_juego = True
            self.iniciar_partida()
        elif accion == 'anunciar valor':
            self.validar_valor(msg[1], skt)
        elif accion == 'pasar turno':
            self.pasar_turno(skt)
        elif accion == 'cambiar dados':
            self.cambiar_dados(skt)
        elif accion == 'dudar':
            self.dudar(skt)
        elif accion == 'usar poder':
            self.usar_poder(skt, msg[1])

    def update_connected_players(self, skt):
        hay_cola = False
        connected = self.sockets[skt]['connected']
        turno = False
        m.log_player_desconectado(self.sockets[skt]['username'])
        if len(self.sockets) > self.max_players:
            hay_cola = True

        if self.en_juego and skt in self.skts_conectados.values():
            player = m.get_player_info_skt(skt, self.sockets, self.players_info)
            player['vidas'] = 0
            if self.players_info[self.turno_actual] == player:
                turno = True

        # Devolvemos el id y el nombre al poll y borramos al cliente
        if skt in self.skts_conectados.values():
            ide = self.sockets[skt]['id']
            self.ids.append(ide)
            self.nombres.append(self.sockets[skt]['username'])
            self.skts_conectados.pop(ide)

        self.sockets.pop(skt)
        skt.close()

        # Vemos si hay algun cliente en cola para conectarse
        if hay_cola and not self.en_juego and connected:
            self.check_cola()
        if not self.en_juego:
            self.update_interface_inicio()

        if self.win or len(self.skts_conectados) == 0:
            self.socket_server.close()
        elif self.en_juego and not self.win and (len(self.skts_conectados) != 0):
            self.check_win()
            if turno:
                self.next_turn()

    def update_interface_inicio(self):
        names = m.get_names(self.skts_conectados, self.sockets)
        skts = self.sockets.keys()
        for skt in skts:
            self.enviar_info(['update inicio', [len(self.skts_conectados.keys()), names]], skt)

    def sala_llena(self, client_skt):
        # Informamos al cliente que la sala esta llena
        self.update_interface_inicio()
        self.enviar_info(['sala llena'], client_skt)

    def check_cola(self):
        buscando = True
        for client_skt in self.sockets.keys():
            if not self.sockets[client_skt]['connected'] and buscando:
                # Avisamos al primero que este en la cola que hay cupo disponible
                self.enviar_info(['cupo disponible'], client_skt)
                self.connect_player(client_skt)
                buscando = False

    def partida_en_juego(self, client_skt):
        # Informamos al cliente que hay una partida en juego
        sleep(0.1)
        client_skt.send(cripto.enviar(['partida en juego'], self.num))
        names = m.get_names(self.skts_conectados, self.sockets)
        print('')
        self.enviar_info(['update inicio', [len(self.skts_conectados.keys()), names]], client_skt)

    def iniciar_partida(self):
        self.en_juego = True
        skts_info = (self.skts_conectados, self.sockets)
        info = (*skts_info, self.vidas_ini, self.ids, self.max_players, self.nombres)
        info_ini = m.info_ini_partida(*info)
        self.players_info, info_interface = info_ini
        m.log_inicio_partida(self.max_players, self.players_info)
        for player in self.players_info:
            if not player['bot']:
                skt = self.skts_conectados[player['id']]
                self.enviar_info(['start game', [info_interface, player]], skt)
        for skt in m.players_not_ingame(self.skts_conectados, self.sockets):
            skt.send(cripto.enviar(['partida en juego'], self.num))
        self.turno_actual = (random.randint(1, self.max_players)) % self.max_players
        self.next_turn()

    def next_turn(self):
        self.turno_actual = (self.turno_actual + 1) % self.max_players
        player = self.players_info[self.turno_actual]

        if player['vidas'] > 0:
            m.log_turno(player)
            self.numero_turno += 1
            msg = [(player)['name'], self.numero_turno, self.maximo_anunciado]
            self.send_info_to_players(['next turn', msg])
            if player['bot'] and self.is_online:
                self.bot_turn(player, (self.numero_turno == 1))

        else:
            self.next_turn()

    def validar_valor(self, valor, skt):
        valid, error = m.validar_dados(valor, self.maximo_anunciado)
        if valid:
            valor = int(valor)
            ide = m.get_id(skt, self.sockets)
            self.valor_anunciado['valor'] = valor
            self.valor_anunciado['id'] = ide
            self.valor_anunciado['mintiendo'] = m.miente(valor, ide, self.players_info)
            self.maximo_anunciado = valor
            m.log_anunciar_valor(skt, self.sockets, self.players_info, valor)
            self.next_turn()
        else:
            self.enviar_info(error, skt)

    def pasar_turno(self, skt):
        ide = m.get_id(skt, self.sockets)
        self.valor_anunciado['valor'] = self.valor_paso
        self.valor_anunciado['id'] = ide
        self.valor_anunciado['mintiendo'] = m.miente(self.valor_paso, ide, self.players_info)
        m.log_pasar_turno(skt, self.sockets, self.players_info)
        self.next_turn()

    def cambiar_dados(self, skt):
        dado1, dado2 = m.random_dados()
        player = m.get_player_info_skt(skt, self.sockets, self.players_info)
        player['dado1'] = dado1
        player['dado2'] = dado2
        m.log_cambiar_dados(player)
        self.enviar_info(['cambiar dados', player], skt)

    def dudar(self, skt):
        if self.valor_anunciado['id'] is not None:
            m.log_dudar(skt, self.sockets, self.players_info)
            self.send_info_to_players(['show dados', m.get_dados(self.players_info)])
            sleep(3)  # El sleep de aca esta para darle tiempo para mostrar los dados uwu
            if self.valor_anunciado['mintiendo']:
                mentiroso = m.get_player_info(self.valor_anunciado['id'], self.players_info)
                mentiroso['vidas'] -= 1
                self.check_gameover(mentiroso)
            else:
                player = m.get_player_info_skt(skt, self.sockets, self.players_info)
                player['vidas'] -= 1
                self.check_gameover(player)
        else:
            self.enviar_info(['no duda', ['No hay valor para dudar']], skt)

    def usar_poder(self, skt, target_name):
        player = m.get_player_info_skt(skt, self.sockets, self.players_info)
        target = m.get_player_info_name(target_name, self.players_info)
        new_round = False
        if set([player['dado1'], player['dado2']]) == {1, 2}:
            target['vidas'] -= 1
            new_round = True
            print('Ataque!')
        elif set([player['dado1'], player['dado2']]) == {1, 3}:
            target['vidas'] = random.randint(1, self.vidas_ini)
            new_round = True
            print('Terremoto!')
        if new_round:
            m.log_usar_poder(player)
            msg = ['show dados', m.get_dados_poder(player, self.players_info)]
            self.send_info_to_players(msg)
            sleep(3)
            self.check_gameover(target)
        else:
            self.enviar_info(['no poder', ['No tiene los dados correctos']], skt)

    def bot_turn(self, player, parte):
        sleep(2)  # Este tambien esta para darle un poco mas de realidad
        ans = self.bot.play(self.valor_anunciado, parte, player,
                            self.players_info, self.valor_paso, self.maximo_anunciado)
        if ans[0] == 'dudar':
            self.send_info_to_players(['show dados', m.get_dados(self.players_info)])
            sleep(3)
            if ans[1][1] == 'mintiendo':
                mentiroso = ans[1][0]
                mentiroso['vidas'] -= 1
            else:
                player['vidas'] -= 1
            self.check_gameover(ans[1][0])
        elif ans[0] == 'anunciar valor':
            self.maximo_anunciado = ans[1][0]
            self.next_turn()
        elif ans[0] == 'pasar':
            self.next_turn()

    def check_gameover(self, player):
        if player['vidas'] >= 0:
            m.log_vidas(player)
        if player['vidas'] == 0 and player['id'] in self.skts_conectados.keys():
            skt_player = self.skts_conectados[player['id']]
            msg = ['Te quedaste sin vidas\nDebe cerrar el programa unu']
            self.enviar_info(['game over', msg], skt_player)
            self.update_connected_players(skt_player)
        self.turno_actual = (self.players_info.index(player) - 1)
        if not self.win:
            self.check_win()
            self.new_round()

    def check_win(self):
        if m.num_players_vivos(self.players_info) == 1 and len(self.skts_conectados) == 1:
            skt = list(self.skts_conectados.values())[0]
            player = m.get_player_info_skt(skt, self.sockets, self.players_info)
            m.log_win(player)
            msg = [f'☆ FELICIDADES {player["name"]} GANASTE ☆\n    Debe cerrar el programa n.n']
            self.enviar_info(['u win', msg], skt)
            self.win = True
            self.socket_server.close()

    def new_round(self):
        self.numero_turno = 0
        for player in self.players_info:
            dado1, dado2 = m.random_dados()
            player['dado1'] = dado1
            player['dado2'] = dado2
        self.valor_anunciado = {'valor': 0, 'id': None, 'mintiendo': True}
        self.maximo_anunciado = 0
        for player in self.players_info:
            if player['id'] in self.skts_conectados.keys():
                skt = self.skts_conectados[player['id']]
                self.enviar_info(['new round', [m.new_info(self.players_info), player]], skt)
        self.next_turn()

    def send_info_to_players(self, msg):
        for player in self.players_info:
            if player['id'] in self.skts_conectados.keys():
                skt = self.skts_conectados[player['id']]
                self.enviar_info(msg, skt)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        port = int(sys.argv[1])
    else:
        port = 69
    server = Servidor(port)
