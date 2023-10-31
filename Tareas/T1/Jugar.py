import os.path
import Archivos
import Torneo
import parametros

'''
Todo lo que es menus como tal se encuentra aca
El manejo de los archivos como, guardar y cargar
se encuentra en el modulo Archivos :D
'''

VOLVER = "volver"
SALIR = "salir"


def menu_manager():
    historial = ["ir_menu_inicio"]
    respuesta = ""
    while respuesta != SALIR:
        estado_actual = historial[-1]

        if estado_actual == "ir_menu_inicio":
            # en el menu de inicio hay dos opciones, una es nueva partida
            # entonces instanciamos torneo nuevo y la otra es cargar partida
            # donde se instancia otra partida ya guardada

            respuesta = menu_inicio()

            # vemos si se instancio una nueva
            if type(respuesta) == Torneo.Torneo:
                torneo = respuesta
                respuesta = 'ir_menu_principal'

            # de no ser asi respuesta sera 'ir_cargar_partida'

        elif estado_actual == "ir_menu_principal":
            respuesta = menu_principal(torneo)

        elif estado_actual == "ir_ver_mochila":
            respuesta = ver_mochila(torneo)

        elif estado_actual == 'ir_cargar_partida':
            cargar = cargar_partida()
            # cargar_partida puede retornar una instancia de torneo
            # SALIR o VOLVER, los ifs se encargan de manejar lo que retorna
            if cargar == SALIR:
                respuesta = SALIR
            elif cargar == VOLVER:
                respuesta = 'ir_menu_inicio'
            else:
                torneo = cargar
                respuesta = 'ir_menu_principal'

        if respuesta == VOLVER:
            historial.pop()

        elif respuesta.startswith("ir"):
            historial.append(respuesta)


def menu_inicio():
    while True:
        # Primero mostramos el texto uwu
        print(f'''\n {'        *** Menú de Inicio ***'}
        {'-' * 22}
        {'[1] Nueva partida'}
        {'[2] Cargar partida'}
        {'[X] Salir'}''')

        # Solicitamos respuesta del usuario
        respuesta = input('\nIndique su opción (1, 2 o X): \n')

        # Si es nueva partida se instancia una nueva partida uwu
        if respuesta == '1':
            objetos = [Archivos.todas_las_arenas[:], Archivos.todos_los_excavadores[:]]
            torneo = Torneo.Torneo(objetos)
            return torneo

        # Si es cargar partida la opcion mandara al usario al metodo de cargar partida
        elif respuesta == '2':
            return 'ir_cargar_partida'

        elif respuesta == 'X':
            return SALIR

        else:
            print('Opcion invalida, intentelo otra vez. ^^\n')


def menu_principal(torneo):
    while True:
        print(f'''{'         *** Menú Principal ***  '}
        {'-' * 27}
        {f'Dia torneo DCCavaCava: {torneo.dias_transcurridos}/{torneo._dias_totales}'}
        {f'Tipo de arena: {torneo.arena.tipo}'}
        {'[1] Simular día torneo'}
        {'[2] Ver estado torneo'}
        {'[3] Ver ítems'}
        {'[4] Guardar partida'}
        {'[R] Volver'}
        {'[X] Salir del programa'}''')

        respuesta = input('\nIndique su opción (1, 2, 3, 4, R o X): \n')
        if respuesta == "1":
            torneo.simular_dia()

        elif respuesta == "2":
            torneo.mostrar_estado_torneo()

        elif respuesta == "3":
            return 'ir_ver_mochila'

        elif respuesta == '4':
            guardar_partida(torneo)

        elif respuesta == 'R':
            return VOLVER

        elif respuesta == 'X':
            print('CHAO PESCAO')
            return SALIR

        else:
            print('Opcion invalida, intentelo otra vez. ^^\n')

        if torneo.torneo_finalizado is True:
            return 'ir_menu_inicio'


def ver_mochila(torneo):
    while True:
        # Texto :S
        print(f'''{'*** Menu Items ***'.center(85, ' ')}
        {'-' * 85}
        {'    Nombre                |    Tipo    |                    Descripcion'}
        {'-' * 85}''')
        for i in range(len(torneo.mochila)):
            nombre = f'[{i+1}] {torneo.mochila[i].nombre}'.ljust(34, ' ')
            tipo = f'{torneo.mochila[i].tipo}'.center(12, ' ')
            descripcion = f' {torneo.mochila[i].descripcion}'
            texto = '|'.join([nombre, tipo, descripcion])
            print(texto)
        print('-' * 85)
        print('[R] Volver')
        print('[X] Salir del programa')

        # Imput del usuario
        seleccion = input()

        # Revisamos si es un numero y si es valido (dentro del rango)
        if seleccion.isnumeric():
            seleccion = int(seleccion)
            seleccion -= 1
            if len(torneo.mochila) > seleccion and seleccion >= 0:
                torneo.ver_mochila(seleccion)
            else:
                print('Item invalido :c')

        elif seleccion == 'R':
            return VOLVER

        elif seleccion == 'X':
            return SALIR

        else:
            print('Item invalido :c')


def guardar_partida(torneo):
    Archivos.guardar(torneo)
    print('¡¡Su partida fue guardada con exito!! :DD')


def cargar_partida():
    while True:
        # primero hacemos una lista con los nombres de los archivos en Partidas
        partidas = os.listdir(parametros.PATH_PARTIDAS)
        partidas = [partida.split('.')[0] for partida in partidas]

        # Mostramos dicha lista en el formato pedido uwu
        print(f'''{'         *** Menu de carga ***'}
        {'-' * 22}''')
        for i in range(len(partidas)):
            print(f'[{i+1}] {partidas[i]}')
        print('[R] Volver')
        print('[X] Salir')

        # Pedimos al usuario elegir una de las opciones
        seleccion = input()

        # Si es un numero chequeamos que sea valido (que este dentro del rango)
        if seleccion.isnumeric():
            seleccion = int(seleccion)
            seleccion -= 1
            if len(partidas) > seleccion and seleccion >= 0:
                items = Archivos.todos_los_items
                arenas = Archivos.todas_las_arenas
                excavadores = Archivos.todos_los_excavadores
                torneo = Archivos.cargar(partidas[seleccion], items, arenas, excavadores)
                return torneo
            else:
                print('Archivo invalido :c')

        # Si es una X volvemos al menu anterior
        elif seleccion == 'R':
            return VOLVER

        # Si es una X salimos del programa
        elif seleccion == 'X':
            return SALIR

        # Si no es ninguna entonces decimos que el input es invalido :p
        else:
            print('Archivo invalido :c')

# Ahora lo unico que debemos hacer para que corra el programa es llamar a la funcion menu_manager ^^


menu_manager()
