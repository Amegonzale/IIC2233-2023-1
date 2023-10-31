import random


def asignar_id(ids):
    ide = ids.pop(0)
    return ide


def asignar_nombre(names):
    nombre = names.pop(0)
    return nombre


def info_ini_partida(sockets_ids, sockets, vidas_iniciales, ids, max_players, names):
    players_info = []
    for ide in sockets_ids.keys():
        dado1, dado2 = random_dados()
        name = sockets[sockets_ids[ide]]['username']
        players_info.append({'id': ide, 'vidas': vidas_iniciales, 'name': name,
                             'dado1': dado1, 'dado2': dado2, 'bot': False})

    for ide, name in zip(ids, names):
        if len(players_info) < max_players:
            dado1, dado2 = random_dados()
            players_info.append({'id': ide, 'vidas': vidas_iniciales, 'name': name,
                                'dado1': dado1, 'dado2': dado2, 'bot': True})

    info_interface = []
    for player in players_info:
        info_interface.append([player['id'], player['vidas'], player['name']])
    info_interface.sort()
    players_info = sorted(players_info, key=lambda x: x['id'])

    return (players_info, info_interface)


def get_names(skts_conectados, sockets):
    names = []
    clientes = skts_conectados.values()
    for client in clientes:
        names.append(sockets[client]['username'])
    return names


def get_id(skt, sockets):
    return sockets[skt]['id']


def get_player_info(ide, players_info):
    for player in players_info:
        if player['id'] == ide:
            return player


def get_player_info_skt(skt, sockets, players_info):
    ide = get_id(skt, sockets)
    return get_player_info(ide, players_info)


def get_player_info_name(name, players_info):
    for player in players_info:
        if player['name'] == name:
            return player


def players_not_ingame(skts_conectados, sockets):
    skts_en_cola = []
    for skt in sockets.keys():
        if skt not in skts_conectados.values():
            skts_en_cola.append(skt)
    return skts_en_cola


def validar_dados(valor, maximo_anunciado):
    valido = True
    error = ''
    if not valor.isdigit():
        error = ['error', ['Valor debe ser numero']]
        valido = False
    elif valor.isdigit() and int(valor) not in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        error = ['error', ['Valor invalido']]
        valido = False
    elif valor.isdigit() and int(valor) in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        valor = int(valor)
        if valor <= maximo_anunciado:
            error = ['error', ['Valor debe ser mayor al anterior']]
            valido = False
    return (valido, error)


def miente(valor, ide, players_info):
    player = get_player_info(ide, players_info)
    suma_dados = player['dado1'] + player['dado2']
    return suma_dados != valor


def random_dados():
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    return (dado1, dado2)


def reroll_dados_players(players_info):
    for player in players_info:
        player['dado1'], player['dado2'] = random_dados()


def new_info(players_info):
    info_interface = []
    for player in players_info:
        info_interface.append([player['id'], player['vidas'], player['name']])
    return info_interface


def num_players_vivos(players_info):
    vivos = 0
    for player in players_info:
        if player['vidas'] > 0:
            vivos += 1
    return vivos


def get_dados(players_info):
    dados = []
    for player in players_info:
        if player['vidas'] <= 0:
            dados.append((0, 0))
        else:
            dados.append((player['dado1'], player['dado2']))
    return dados


def get_dados_poder(plr, players_info):
    dados = []
    for player in players_info:
        if player == plr:
            dados.append((player['dado1'], player['dado2']))
        else:
            dados.append((0, 0))
    return dados


def log_player_conectado(username):
    print(f'Se ha conectado: {username}')
    print('----------------------------')


def log_player_desconectado(username):
    print(f'Se ha desconectado: {username}')
    print('----------------------------')


def log_inicio_partida(max_players, players_info):
    names = [player['name'] for player in players_info if not player['bot']]
    print('☆ Comienza una partida con:')
    print(*names)
    print(f'... mas {max_players - len(names)} bots ☆')
    print('----------------------------')


def log_turno(player):
    print(f'Comienza el turno de: {player["name"]}')
    print('☆--------------------------☆')


def log_anunciar_valor(skt, sockets, players_info, valor, player=None):
    if player is None:
        player = get_player_info_skt(skt, sockets, players_info)
    print(f'{player["name"]} decidio anunciar valor {valor}')
    print('----------------------------')


def log_pasar_turno(skt, sockets, players_info, player=None):
    if player is None:
        player = get_player_info_skt(skt, sockets, players_info)
    suma = player['dado1'] + player['dado2']
    print(f'{player["name"]} decidio pasar turno con {suma}')
    print('----------------------------')


def log_cambiar_dados(player):
    print(f'{player["name"]} decidio cambiar dados')
    print('----------------------------')


def log_dudar(skt, sockets, players_info, player=None):
    if player is None:
        player = get_player_info_skt(skt, sockets, players_info)
    print(f'{player["name"]} decidio dudar')
    print('----------------------------')


def log_usar_poder(player):
    print(f'{player["name"]} decidio usar poder')
    print('----------------------------')


def log_vidas(player):
    print(f'{player["name"]} perdio una vida, ahora le quedan {player["vidas"]}')
    print('----------------------------')


def log_win(player):
    print(f'☆ {player["name"]} gano ☆')
    print('----------------------------')
