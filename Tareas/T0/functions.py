import os.path


def menu() -> None:
    print('--- Menu de Aciones ---\n')
    print('[1] Mostrar tablero')
    print('[2] Validar bombas y tortugas')
    print('[3] Validar solucion')
    print('[4] Solucionar el tablero')
    print('[0] Salir del programa\n')


def verificar_archivo(nombre_archivo: str) -> bool:
    return os.path.exists(os.path.join('Archivos', f'{nombre_archivo}'))


def cargar_tablero(nombre_archivo: str) -> list:
    with open(os.path.join('Archivos', f'{nombre_archivo}')) as archivo:
        archivo = archivo.readline()
    dimension_tablero = int(archivo[0])
    archivo = (archivo.split(','))[1::]
    tablero = []
    for i in range(dimension_tablero):
        tablero.append(archivo[dimension_tablero * i: dimension_tablero * (i + 1)])
    return tablero


def guardar_tablero(nombre_archivo: str, tablero: list) -> None:
    solucion = f'{len(tablero)},'
    for linea in tablero:
        solucion += ','.join(linea)+','
    solucion = solucion[:len(solucion) - 1]
    with open(os.path.join('Archivos', f'{nombre_archivo}'), 'w') as archivo_nuevo:
        archivo_nuevo.write(solucion)


def verificar_valor_bombas(tablero: list) -> int:
    tablero_unido = []
    invalidos = 0
    for row in tablero:
        tablero_unido += row
    for elemento in tablero_unido:
        if ('-' not in elemento) and ('T' not in elemento):
            if int(elemento) < 2 or int(elemento) > (2 * len(tablero) - 1):
                invalidos += 1
    return invalidos


'''
Las siguientes 4 funciones son para verificar
el alcance que tienen las bombas, tanto
horizontalmente como verticalmente (up, down, left, right)
'''


def alcance_up(tablero: list, i: int, j: int) -> int:
    aux = 1
    contador = 0
    while i - aux >= 0 and tablero[i - aux][j] != 'T':
        contador += 1
        aux += 1
    return contador


def alcance_down(tablero: list, i: int, j: int) -> int:
    aux = 1
    contador = 0
    while i + aux < len(tablero) and tablero[i + aux][j] != 'T':
        contador += 1
        aux += 1
    return contador


def alcance_left(tablero: list, i: int, j: int) -> int:
    aux = 1
    contador = 0
    while j - aux >= 0 and tablero[i][j - aux] != 'T':
        contador += 1
        aux += 1
    return contador


def alcance_right(tablero: list, i: int, j: int) -> int:
    aux = 1
    contador = 0
    while j + aux < len(tablero) and tablero[i][j + aux] != 'T':
        contador += 1
        aux += 1
    return contador


def verificar_alcance_bomba(tablero: list, coordenada: tuple) -> int:
    '''
    Para verificar el alcance total
    de las bombas sumamos el alcance horizontal
    y vertical y le sumamos uno (dado que en el
    espacio en el que esta la bomba tambien cuenta)
    '''
    i = coordenada[0]
    j = coordenada[1]
    if tablero[i][j] != 'T' and tablero[i][j] != '-':
        suma_horizontal = alcance_left(tablero, i, j) + alcance_right(tablero, i, j)
        suma_vertical = alcance_up(tablero, i, j) + alcance_down(tablero, i, j)
        return 1 + suma_horizontal + suma_vertical
    else:
        return 0


'''
las siguientes 4 funciones son para verificar
la existencia de una tortuga sobre, bajo o a
los lados de otra tortuga. Retorna True si es
asi.
'''


def verificar_up(tablero: list, i: int, j: int) -> bool:
    if i == 0:
        return False
    else:
        if tablero[i - 1][j] == 'T':
            return True
        else:
            return False


def verificar_down(tablero: list, i: int, j: int) -> bool:
    if i == (len(tablero) - 1):
        return False
    else:
        if tablero[i + 1][j] == 'T':
            return True
        else:
            return False


def verificar_left(tablero: list, i: int, j: int) -> bool:
    if j == 0:
        return False
    else:
        if tablero[i][j - 1] == 'T':
            return True
        else:
            return False


def verificar_right(tablero: list, i: int, j: int) -> bool:
    if j == (len(tablero[0]) - 1):
        return False
    else:
        if tablero[i][j + 1] == 'T':
            return True
        else:
            return False


'''
Utilizamos dichas funciones para chequear la
cantidad de tortugas que no cumplen con la condicion
'''


def verificar_tortugas(tablero: list) -> int:
    tortugas_invalidas = 0
    for i in range(len(tablero)):
        for j in range(len(tablero)):
            if tablero[i][j] == 'T':
                if verificar_up(tablero, i, j) or verificar_down(tablero, i, j):
                    tortugas_invalidas += 1
                elif verificar_left(tablero, i, j) or verificar_right(tablero, i, j):
                    tortugas_invalidas += 1
    return tortugas_invalidas


def tortuga_invalida(tablero: list, i: int, j: int) -> bool:
    '''
    Revisa si hay una tortuga a los lados
    o arriba o abajo, retorna true si la
    tortuga es invalida. (esta funcion se
    utilizara para solucionar el tablero)
    '''
    if verificar_up(tablero, i, j) or verificar_down(tablero, i, j):
        return True
    elif verificar_left(tablero, i, j) or verificar_right(tablero, i, j):
        return True
    return False


def get_coordinates(tablero: list) -> list:
    '''
    La siguiente funcion tiene las coordenadas
    de todas las bombas que hay en el tablero,
    es una lista de tuplas
    '''
    coordenadas_bombas = []
    for i in range(len(tablero)):
        for j in range(len(tablero)):
            if tablero[i][j] != 'T' and tablero[i][j] != '-':
                coordenadas_bombas.append((i, j))
    return coordenadas_bombas


def verificar_celdas_tapadas(tablero: list) -> bool:
    '''
    La funcion chequea si hay un elemento T
    en la celda y ve si existe otro elemento
    mas en la misma celda (bomba)
    '''
    coordenadas = get_coordinates(tablero)
    tapado = False
    for coordenada in coordenadas:
        i = coordenada[0]
        j = coordenada[1]
        if 'T' in tablero[i][j] and '-' not in tablero[i][j] and len(tablero[i][j]) == 2:
            tapado = True
    return tapado


def coinciden(tablero: list, coordenada: tuple) -> bool:
    '''
    El objetivo de esta funcion es verificar
    si el numero del alcance de la bomba
    coincide con su alcance real
    '''
    alcance_real = verificar_alcance_bomba(tablero, coordenada)
    if alcance_real == int(tablero[coordenada[0]][coordenada[1]]):
        return True
    else:
        return False


def coinciden_todas(tablero: list) -> bool:
    '''
    Esta funcion verifica si el alcance
    se cumple para todas las bombas
    '''
    coordenadas = get_coordinates(tablero)
    for coordenada in coordenadas:
        if not (coinciden(tablero, coordenada)):
            return False
    return True


def tablero_valido(tablero: list) -> bool:
    '''
    Esta funcion verifica si se cumplen
    las reglas 1, 2, 3 y 4
    '''
    bombas_invalidas = verificar_valor_bombas(tablero)
    tortugas_invalidas = verificar_tortugas(tablero)
    tapado = verificar_celdas_tapadas(tablero)
    coinciden_alcance = coinciden_todas(tablero)
    valido = True
    if bombas_invalidas != 0 or tortugas_invalidas != 0 or tapado or not coinciden_alcance:
        valido = False
    return valido

import functions as f

'''
Aqui estaran todas las funciones que se
utilizaran exclusivamente para encontrar
una solucion valida para el tablero
'''


def celda_valida(tablero: list, i: int, j: int) -> bool:
    '''
    Tiene como objetivo determinar si la celda
    (i, j) ya tiene una tortuga o una bomba
    en esa posicion. Retorna True si no tiene
    ninguna de las dos indicando que es valida.
    '''
    valido = True
    if tablero[i][j] != '-' or f.tortuga_invalida(tablero, i, j):
        valido = False
    return valido


def bombas_afectadas(tablero: list, i: int, j: int, coordenadas: list) -> list:
    '''
    La funcion tiene como objetivo identificar
    si cuales son las bombas afectadas en el
    caso de poner una tortuga en la posicion
    (i, j). De esta forma, si no altera ninguna
    no considera esa celda como opcion.
    '''
    afectadas = []
    for coordenada in coordenadas:
        if coordenada[0] == i or coordenada[1] == j:
            afectadas.append(coordenada)
    return afectadas


def validez_nuevo_alcance(tablero: list, i: int, j: int, bomba: tuple) -> bool:
    '''
    Esta funcion se pone en el caso
    hipotetico de posicionar una tortuga
    en las coordenadas (i, j) y revisa
    el nuevo alcance de una cierta bomba.
    Si su valor es menor al que deberia
    tener retorna False. Evita hacer mas
    permutaciones.
    '''
    nuevo_tablero = [[elemento for elemento in tablero[x]] for x in range(len(tablero))]
    nuevo_tablero[i][j] = 'T'
    nuevo_alcance = f.verificar_alcance_bomba(nuevo_tablero, bomba)
    if nuevo_alcance < int(tablero[bomba[0]][bomba[1]]):
        return False
    else:
        return True


def validez_nueva_tortuga(tablero: list, i: int, j: int, coordenadas: list) -> bool:
    '''
    Verifica la validez de todas las
    bombas afectadas por situar una tortuga
    en las coordenadas (i, j)
    '''
    bombas = bombas_afectadas(tablero, i, j, coordenadas)
    for bomba in bombas:
        if not validez_nuevo_alcance(tablero, i, j, bomba):
            return False
    return True


def posicion_valida(tablero: list, posicion: tuple):
    '''
    verifica si la posicion es valida y
    si posicionarla afecta negativamente
    el alcance de una de las bombas
    (condensa dos funciones en una)
    Ademas verifica si hay bombas afectadas,
    para que tenga sentido poner la tortuga
    '''
    coordenadas = f.get_coordinates(tablero)
    i = posicion[0]
    j = posicion[1]
    if len(bombas_afectadas(tablero, i, j, coordenadas)) != 0:
        if validez_nueva_tortuga(tablero, i, j, coordenadas) and celda_valida(tablero, i, j):
            return True
    return False


def solucionar_tablero(tablero: list) -> list:
    # caso de salida
    if f.tablero_valido(tablero):
        return tablero
    # recursion (amo la recursion)
    for i in range(len(tablero)):
        for j in range(len(tablero)):
            if posicion_valida(tablero, (i, j)):
                tablero[i][j] = 'T'
                amongas = solucionar_tablero(tablero)
                '''
                En el laberinto hacen esto y funciona xD
                es medio sus, asi que le puse amongas a la variable
                '''
                if amongas is not None:
                    return amongas
                tablero[i][j] = '-'
