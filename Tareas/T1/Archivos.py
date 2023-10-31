import Arena
import Item
import Excavador
import os.path
import Torneo
import parametros


'''
Aqui se encuentra todo lo necesario para el manejo de datos.
'''


'''
A continuacion se obtendran los datos de los
archivos csv para su uso en el programa
'''
# Primero extraemos todos los datos del archivo
with open(parametros.PATH_CONSUMIBLES, 'r', encoding="utf-8") as archivo:
    consumibles = [consumible.strip('\n') for consumible in archivo]

consumibles = consumibles[1::]  # Quitamos la primera linea
# Ahora separamos todos los datos para poder instanciarlos
consumibles = [consumible.split(',') for consumible in consumibles]


# Mismo proceso uwu
with open(parametros.PATH_TESOROS, 'r', encoding="utf-8") as archivo:
    tesoros = [tesoro.strip('\n') for tesoro in archivo]
tesoros = tesoros[1::]
tesoros = [tesoro.split(',') for tesoro in tesoros]


with open(parametros.PATH_ARENAS, 'r', encoding="utf-8") as archivo:
    arenas = [arena.strip('\n') for arena in archivo]
arenas = arenas[1::]
arenas = [arena.split(',') for arena in arenas]


with open(parametros.PATH_EXCAVADORES, 'r', encoding="utf-8") as archivo:
    excavadores = [excavador.strip('\n') for excavador in archivo]
excavadores = excavadores[1::]
excavadores = [excavador.split(',') for excavador in excavadores]

'''
Ahora nos encargamos de instanciar las cosas uwu
'''
'''
Consumibles y tesoros
'''


def instanciar_consumibles(consumibles):
    items_consumibles = []
    for consumible in consumibles:
        item_consumible = Item.Consumibles(consumible[0], 'Consumible', *consumible[1::])
        items_consumibles.append(item_consumible)
    return items_consumibles


def instanciar_tesoros(tesoros):
    items_tesoros = []
    for tesoro in tesoros:
        item_tesoro = Item.Tesoros(tesoro[0], 'Tesoro', *tesoro[1::])
        items_tesoros.append(item_tesoro)
    return items_tesoros


items_consumibles = instanciar_consumibles(consumibles)
items_tesoros = instanciar_tesoros(tesoros)

todos_los_items = items_consumibles + items_tesoros

'''
Ahora instanciamos las arenas :3
'''


def instanciar_arenas(arenas, items_arena):
    # Creamos una lista para cada tipo de arena :D
    arena_normal = []
    arena_mojada = []
    arena_rocosa = []
    arena_magnetica = []

    # Instanciamos las arenas :3
    for arena in arenas:
        tipo_de_arena = arena[1]
        arena.append(items_arena)
        # Todas las arenas tendran los mismos items :D
        # Ahora instanciamos por tipo
        if tipo_de_arena == 'normal':
            arena_instanciada = Arena.ArenaNormal(*arena)
            arena_normal.append(arena_instanciada)

        elif tipo_de_arena == 'mojada':
            arena_instanciada = Arena.ArenaMojada(*arena)
            arena_mojada.append(arena_instanciada)

        elif tipo_de_arena == 'rocosa':
            arena_instanciada = Arena.ArenaRocosa(*arena)
            arena_rocosa.append(arena_instanciada)

        elif tipo_de_arena == 'magnetica':
            arena_instanciada = Arena.ArenaMagnetica(*arena)
            arena_magnetica.append(arena_instanciada)

    todas_las_arenas = arena_normal + arena_mojada + arena_rocosa + arena_magnetica

    return todas_las_arenas


todas_las_arenas = instanciar_arenas(arenas, todos_los_items[:])

'''
Por ultimo instanciamos los excavadores
'''


def instanciar_excavadores(excavadores):
    excavador_docencio = []
    excavador_tareo = []
    excavador_hibrido = []

    # Instanciamos los excavadores :3

    for excavador in excavadores:
        tipo_excavador = excavador[1]
        # Vemos a que tipo de excavador corresponde y lo instanciamos por tipo
        if tipo_excavador == 'docencio':
            excavador_instanciado = Excavador.ExcavadorDocencio(*excavador)
            excavador_docencio.append(excavador_instanciado)

        elif tipo_excavador == 'tareo':
            excavador_instanciado = Excavador.ExcavadorTareo(*excavador)
            excavador_tareo.append(excavador_instanciado)

        elif tipo_excavador == 'hibrido':
            excavador_instanciado = Excavador.ExcavadorHíbrido(*excavador)
            excavador_hibrido.append(excavador_instanciado)

    todos_los_excavadores = excavador_docencio + excavador_hibrido + excavador_tareo
    return todos_los_excavadores


todos_los_excavadores = instanciar_excavadores(excavadores)

'''
Los metodos nombres_item_arena y nombres_items_mochila son utiles para guardar
la partida, esto se debe a que para cargarla solo se necesitara buscar en la lista
de todos los items la instancia del item con el mismo nombre, en vez de volver a
instanciar todo. Ademas el archivo de partida guardada queda mas facil de manejar.
'''


def nombres_item_arena(arena):
    '''
    Retorna una lista con los nombres de
    los items dentro de una arena.
    '''
    nombres = []
    for item in arena.items:
        nombres.append(item.nombre)
    nombres = ','.join(nombres)+'\n'
    return nombres


def nombres_items_mochila(mochila):
    '''
    Retorna una lista con los nombres de
    los items dentro de la mochila.
    '''
    nombres = []
    for item in mochila:
        nombres.append(item.nombre)
    nombres = ','.join(nombres)+'\n'
    return nombres


def guardar(torneo):
    '''
    Primero extraemos toda la informacion que vaya variando
    durante el torneo
    '''
    arena = torneo.arena
    equipo = torneo.equipo
    mochila = torneo.mochila
    metros_cavados = torneo.metros_cavados
    dias_transcurridos = torneo.dias_transcurridos
    arenas = torneo.arenas
    excavadores_disponibles = torneo.excavadores_disponibles
    torneo_finalizado = torneo.torneo_finalizado

    '''
    Preguntamos al usuario que nombre desea ponerle, nos aseguramos
    que ponga un nombre valido :D
    '''

    nombre_archivo = input('''¿Que nombre desea ponerle?:
    (El nombre solo puede tener letras y numeros)
    (Si desea sobreescribir un archivo elija el mismo nombre)\n''')

    valid = nombre_archivo.replace(' ', '').isalnum()
    while not valid:
        nombre_archivo = input('''¿Que nombre desea ponerle?:
    (El nombre solo puede tener letras y numeros)
    (Si desea sobreescribir un archivo elija el mismo nombre)\n''')
        valid = nombre_archivo.replace(' ', '').isalnum()

    '''
    Ahora guardamos los datos en un archivo txt con el nombre que
    el usuario eligio.
    '''

    with open(os.path.join('Partidas', f'{nombre_archivo}.txt'), 'w', encoding='utf-8') as line:
        # line.write(','.join(dato)) funciona por el metodo __iter__ que retorna un iterable
        # lo tratamos como lista :D
        # asi quedan sus atributos guardados como nombre,descripcion,tipo,...
        # lo anterior funciona para arena y excavador

        # En una misma linea ponemos la arena actual (tal como la entregan en el archivo csv)
        # junto con los nombres de los items que posee
        line.write(','.join(arena))
        line.write(',' + nombres_item_arena(arena))

        # En la siguiente linea escribimos la canitdad de excavadores en el equipo y los disponibles
        # de esta forma es facil saber hasta que linea seran excavadores a la hora de cargar partida
        line.write(f'{len(equipo)},{len(excavadores_disponibles)}\n')

        # En las siguientes lineas van primero los (cantidad_excavadores_equipo) excavadores del eq.
        # y luego los (cantidad_excavadores_disponibles) excavadores disponibles
        for excavador in equipo:
            line.write(','.join(excavador)+'\n')
        for excavador in excavadores_disponibles:
            line.write(','.join(excavador)+'\n')

        # Ahora anotamos los nombres de los items dentro de la mochila
        line.write(nombres_items_mochila(mochila))

        # uno tras del otro, anotamos los metros cavados, dias transcurridos y si finalizo el torneo
        line.write(f'{metros_cavados},{dias_transcurridos},{torneo_finalizado}\n')

        # Por ultimo escribimos todas las arenas con el mismo formato de la arena actual
        for arena in arenas:
            line.write(','.join(arena))
            line.write(',' + nombres_item_arena(arena))


def buscar_items(nombres, todos_los_items):
    '''
    Esta funcion se encarga de tomar una lista de nombres de items
    y buscar en la lista de todos los items dicho item instanciado.
    Ya que estos no varian sus stats mediante avanza la partida.
    Retorna la lista de los items en nombres ya instanciados.
    '''
    items = []
    for i in range(len(todos_los_items)):
        for nombre in nombres:
            if todos_los_items[i].nombre == nombre:
                items.append(todos_los_items[i])
    return items


def cargar(nombre_archivo, todos_los_items, todas_las_arenas, todos_los_excavadores):
    # La funcion se puede ver engorrosa pero tiene sentido lo prometo.
    with open(os.path.join('Partidas', f'{nombre_archivo}.txt'), 'r', encoding='utf-8') as archivo:
        datos = [dato.strip('\n') for dato in archivo]
    '''
    Todo surge por como se guardan los datos.

    El formato es el siguiente (en lineas distintas):
    arena_actual, nombre_items_arena_actual
    cantidad_excavadores_equipo, cantidad_excavadores_disponibles
    excavadores
    .
    .
    .
    nombre_items_mochila
    metros_cavados, dias_transcurridos, torneo_finalizado
    arenas_disponibles, nombre_items_arenas_disponibles
    .
    .
    .

    Donde los puntos representan mas excavadores o arenas. El largo
    de los puntos de excavadores esta dado por cantidad_total que es
    la suma de ambas cantidades de excavadores.
    '''
    # La primera linea corresponde a la arena_actual y sus items
    # Usamos la funcion instanciar_arenas para instanciarla :p
    arena = datos[0].split(',')[0:6]
    items_arena = buscar_items(datos[0].split(',')[6:], todos_los_items)
    arena_actual = instanciar_arenas([arena], items_arena)[0]

    # La segunda linea indica la cantidad de excavadores del equipo y disponibles
    cantidad_excavadores_equipo = int(datos[1].split(',')[0])
    cantidad_excavadores_disp = int(datos[1].split(',')[1])
    cantidad_total = cantidad_excavadores_disp + cantidad_excavadores_equipo

    # Desde la tercera linea tomamos cantidad_excavadores_equipo siguientes
    # Corresponden a los excavadores del equipo...
    equipo = datos[2:cantidad_excavadores_equipo + 2]
    equipo = [exc.split(',') for exc in equipo]

    # Desde donde quedamos hasta que terminen los excavadoes seran los que hay disponibles
    excavadores_disponibles = datos[2 + cantidad_excavadores_equipo:cantidad_total + 2]
    excavadores_disponibles = [exc.split(',') for exc in excavadores_disponibles]

    # instanciamos ambos
    equipo = instanciar_excavadores(equipo)
    excavadores_disponibles = instanciar_excavadores(excavadores_disponibles)

    # La mochila va luego de que acaben los excavadores, es decir la tercera linea
    # mas la cantidad total de excavadores
    mochila = buscar_items(datos[cantidad_total + 2].split(','), todos_los_items)

    # Los tres datos a continuacion van en la linea siguiente a mochila
    # por ende le sumamos uno al indice
    # Como van seguidos de comas los extraemos con un indice luego de un split
    metros_cavados = float(datos[cantidad_total + 3].split(',')[0])
    dias_transcurridos = int(datos[cantidad_total + 3].split(',')[1])
    torneo_finalizado = (datos[cantidad_total + 3].split(',')[2])

    # Como torneo_finalizado es un True o False en modo string lo pasamos a bool
    if torneo_finalizado == 'False':
        torneo_finalizado = False
    else:
        torneo_finalizado = True

    # El resto de las arenas vienen en las lineas que siguen hasta el fin :D
    arenas = datos[cantidad_total + 4:]
    arenas_disponibles = []
    for arena in arenas:
        # separamos los datos como lo hicimos para la arena_actual y las instanciamos
        items_arena = buscar_items(arena.split(',')[6:], todos_los_items)
        arena = arena.split(',')[0:6]
        arena_instanciada = instanciar_arenas([arena], items_arena)[0]
        arenas_disponibles.append(arena_instanciada)

    # Juntamos todas las arenas y todos los excavadores disponibles (globalmente) en una lista asi,
    # e instanciamos un torneo
    objetos = [todas_las_arenas[:], todos_los_excavadores[:]]
    torneo = Torneo.Torneo(objetos)

    # Como hay parametros que parten vacios por default ahora los sobreescribimos

    torneo.arena = arena_actual
    torneo.equipo = equipo
    torneo.mochila = mochila
    torneo.metros_cavados = metros_cavados
    torneo.dias_transcurridos = dias_transcurridos
    torneo.arenas = arenas_disponibles
    torneo.excavadores_disponibles = excavadores_disponibles
    torneo.torneo_finalizado = torneo_finalizado

    return torneo
