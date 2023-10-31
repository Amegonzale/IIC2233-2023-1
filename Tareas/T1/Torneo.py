import parametros as param
import random


class Torneo:

    def __init__(self, objetos):
        self._arena = None
        self.eventos = ['Lluvia', 'Terremoto', 'Derrumbe']
        self.probabilidad_eventos = [param.PROB_LLUVIA, param.PROB_TERREMOTO, param.PROB_DERRUMBE]
        self.equipo = []
        self.mochila = []
        self._metros_cavados = 0
        self.dias_transcurridos = 0
        self._meta = float(param.METROS_META)
        self._dias_totales = int(param.DIAS_TOTALES_TORNEO)
        self.arenas = objetos[0]
        self.excavadores_disponibles = objetos[1]
        self.torneo_finalizado = False

        '''
        Elegimos los excavadores del equipo a partir
        de los disponibles solo si estamos eligiendolos
        iniciales. Esto es para evitar problemas al
        cargar partida.
        '''
        if self.equipo == []:
            cantidad_excavadores = param.CANTIDAD_EXCAVADORES_INICIALES
            for _ in range(cantidad_excavadores):
                excavador_elegido = random.choice(self.excavadores_disponibles)
                self.equipo.append(excavador_elegido)
                self.excavadores_disponibles.remove(excavador_elegido)

        '''
        Ahora elegimos la arena, el tipo de la arena
        sera la establecida en parametros, elegimos
        al azar una arena de esa clase. Lo mismo de antes,
        esto solo ocurre si la arena inicial es None para
        evitar problemas con cargar partida uwu.
        '''
        if self.arena is None:
            tipo_arena = param.ARENA_INICIAL
            self.arena = random.choice(self.arenas_tipo(tipo_arena))

    def arenas_tipo(self, tipo_arena):
        '''
        La siguiente funcion se encarga de recorrer
        toda la lista de arenas disponibles y retorna una
        lista de un tipo de arena en especifico, dado
        por tipo_arena
        '''
        lista_arenas = [arena for arena in self.arenas if arena.tipo == tipo_arena]
        return lista_arenas

    def excavadores_tipo(self, tipo_excavador):
        '''
        La siguiente funcion se encarga de recorrer
        todos los excavadores_disponible y retorna una
        lista de un tipo de excavador dado por
        tipo_excavador
        '''
        lista_exc = [exc for exc in self.excavadores_disponibles if exc.tipo == tipo_excavador]
        return lista_exc

    @property
    def arena(self):
        return self._arena

    @arena.setter
    def arena(self, nueva_arena):
        '''
        Este setter se encarga de devolver la arena
        a las arenas disponibles, asignar la arena
        a la nueva_arena y remover esa del poll disponible
        (asi me ahorro lineas de codigo mas adelante tambien juju)
        '''
        if self._arena is not None:  # Como el parametro inicial comienza en None esto evita bugs
            self.arenas.append(self._arena)
        self._arena = nueva_arena
        if nueva_arena in self.arenas:
            self.arenas.remove(nueva_arena)

    @property
    def meta(self):
        return self._meta

    @property
    def dias_totales(self):
        return self._dias_totales

    @property
    def metros_cavados(self):
        return self._metros_cavados

    @metros_cavados.setter
    def metros_cavados(self, nuevo_hondo):
        '''
        Este setter evita que hayan metros
        cavados negativos cuando ocurren derrumbes
        y se reste al total
        '''
        if nuevo_hondo >= 0:
            self._metros_cavados = nuevo_hondo
        else:
            self._metros_cavados = 0

    def simular_dia(self):
        if not self.torneo_finalizado:
            '''
            Revisamos que el torneo aun no haya
            finalizado. Le sumamos uno al dia y
            mostramos en consola el header con el dia.
            '''
            self.dias_transcurridos += 1

            # Lo de abajo es solo para el display del menu
            print(f'\n              Dia {self.dias_transcurridos}'.center(53))
            print('-' * 53)

            # Por como esta armada la arena magnetica, debe cambiar sus
            # stats por unos random cada vez que cambia el dia
            if self.arena.tipo == 'magnetica':
                self.arena.nuevo_dia()

            '''
            Primero se trabaja la primera parte, la de cavar :D
            Para cada excavador en el equipo que no este descansando
            hacemos que cave y sumamos eso a metros cavados por el
            equipo. Si esta descansando se muestra que esta mimiendo.
            Finalmente se anuncia cuanto cavaron todos.
            '''
            print('Metros Cavados:')
            metros_cavados_equipo = 0
            for excavador in self.equipo:
                # Chequeamos que no este descansando
                if excavador.descansando is False:
                    # Cava y se lo suma al equipo, muestra en consola cuanto cavo
                    metros_cavados_excavador = excavador.cavar(self.arena)
                    metros_cavados_equipo += metros_cavados_excavador
                    print(f'{excavador.nombre} ha cavado {metros_cavados_excavador} metros.')
                elif excavador.descansando is True:
                    # Si esta descansando no puede cavar :c
                    print(f'{excavador.nombre} esta haciendo tuto uwu mimimimi')

            print(f'El equipo ha conseguido excavar {round(metros_cavados_equipo, 2)} metros.\n')
            self.metros_cavados += metros_cavados_equipo
            self.metros_cavados = round(self.metros_cavados, 2)  # Sumamos lo que excavaron al total

            '''
            Ahora veamos si nuestros excavadores encontraron algun item :3
            Por cada excavador chequeamos si encuentran algun item, solo si no esta
            descansando. Vemos si corresponde a un consumible o un tesoro para mostrarlo
            en consola y luego lo metemos en la mochila. Finalmente mostramos los
            resultados en consola uwu.
            '''

            print('Items Econtrados:')
            cantidad_consumibles = 0
            cantidad_tesoros = 0

            for excavador in self.equipo:
                if not excavador.descansando:
                    item_encontrado = excavador.encontrar_item(self.arena)
                    if item_encontrado is None:
                        print(f'{excavador.nombre} no consiguio nada. :(')
                    else:
                        nombre_item = item_encontrado.nombre
                        nombre = excavador.nombre
                        if item_encontrado.tipo == 'Consumible':
                            print(f'{nombre} consiguio {nombre_item} del tipo consumible.')
                            cantidad_consumibles += 1
                        elif item_encontrado.tipo == 'Tesoro':
                            print(f'{nombre} consiguio {nombre_item} del tipo tesoro.')
                            cantidad_tesoros += 1
                        self.mochila.append(item_encontrado)
                else:
                    print(f'{excavador.nombre} esta muy cansade para buscar items ;_;')

            cantidad_total_encontrada = cantidad_consumibles + cantidad_tesoros
            print(f'''\n{f'Se han encontrado {cantidad_total_encontrada} items:'}
            {f'- {cantidad_consumibles} consumibles.'}
            {f'- {cantidad_tesoros} tesoros.'}\n''')

            '''
            Ahora viene la ocurrencia de evento omg :0
            La explicacion se encuentra en la funcion en si
            '''
            self.iniciar_evento()

            for excavador in self.equipo:
                excavador.un_dia_mas()
                # Se encarga de estar al tanto de si el excavador deberia estar o no descansando.

            '''
            Chequeamos si los dias totales del torneo
            son iguales a los dias transcurridos
            '''
            if self.dias_totales == self.dias_transcurridos:
                self.torneo_finalizado = True

        # Una vez finalizado el evento no ocurre nada si se simula el dia
        # aparte de los resultados finales
        if self.torneo_finalizado is True:
            print('HA FINALIZADO EL TORNEO, ESTOS SON LOS RESULTADOS')
            print(f'El equipo logro cavar {self.metros_cavados} metros de {self.meta} metros.')
            if self.metros_cavados >= self.meta:
                # Si ganaron muestra esto en consola yipie :D
                print('ENHORA BUENA LOGRARON CUMPLIR LA META')
            else:
                print('El equipo no logro pasar la meta :( Quizas para la proxima <3')

    def iniciar_evento(self):
        # Primero revisamos si ocurre o no un evento
        if random.random() <= param.PROB_INICIAR_EVENTO:
            # De ser asi se elige al azar segun las probabilidades dadas a que evento corresponde
            evento = random.choices(self.eventos, weights=self.probabilidad_eventos, k=1)[0]
            print(f'¡¡Durante el día de trabajo ocurrió un {evento}!! ;-;;')

            # Luego se aplican los efectos del dicho evento
            if evento == 'Lluvia':
                if self.arena.tipo == 'normal':
                    self.arena = random.choice(self.arenas_tipo('mojada'))
                elif self.arena.tipo == 'rocosa':
                    self.arena = random.choice(self.arenas_tipo('magnetica'))

            elif evento == 'Terremoto':
                if self.arena.tipo == 'normal':
                    self.arena = random.choice(self.arenas_tipo('rocosa'))
                elif self.arena.tipo == 'mojada':
                    self.arena = random.choice(self.arenas_tipo('magnetica'))

            elif evento == 'Derrumbe':
                print('(NOOO Farkas lo pierde todo)')
                self.arena = random.choice(self.arenas_tipo('normal'))
                self.metros_cavados -= param.METROS_PERDIDOS_DERRUMBE

            print(f'La arena final es del tipo {self.arena.tipo}')
            print('Tu equipo ha perdido 2 de felicidad\n')

            for excavador in self.equipo:
                excavador.felicidad -= 2
        else:
            print('¡¡Durante el día de trabajo ocurrió NADA!! u_u\n')

    def mostrar_estado_torneo(self):
        # Lo de abajo es para mostrar el estado del evento en consola
        # se ve feo en el codigo unu
        print(f'''{'*** Estado Torneo ***'.center(63)}
        {'-' * 63}
        {f'Dia actual: {self.dias_transcurridos}'}
        {f'Tipo de arena: {self.arena.tipo}'}
        {f'Metros excavados: {round(self.metros_cavados, 2)} / {self._meta}'}
        {'-' * 63}
        {'Excavadores'.center(63)}
        {'-' * 63}
        {'    Nombre      |   Tipo   | Energía | Fuerza | Suerte | Felicidad'}
        {'-' * 53}''')

        for excavador in self.equipo:
            nombre = f'{excavador.nombre}'.ljust(17)
            tipo = f'{excavador.tipo[0].upper() + excavador.tipo[1::]}'.center(10)
            energia = f'{excavador.energia}'.center(10)
            fuerza = f'{excavador.fuerza}'.center(8)
            suerte = f'{excavador.suerte}'.center(8)
            felicidad = f'{excavador.felicidad}'.center(9)
            texto = '|'.join([nombre, tipo, energia, fuerza, suerte, felicidad])
            print(f'''       {texto}''')  # los espacios al inicio son para que se vea centrado xD

    def ver_mochila(self, seleccion):
        '''
        La funcion es utilizada para consumir o utilizar
        algun item dentro de la mochila, es por eso que tiene
        como parametro seleccion, que es un valor valido que
        corresponde al indice de un item dentro de la mochila.
        '''
        # Revisamos si el item es consumible o tesoro puesto que tienen distintos efectos
        if self.mochila[seleccion].tipo == 'Consumible':
            nombre = self.mochila[seleccion].nombre
            descripcion = self.mochila[seleccion].descripcion
            print(f'Enhorabuena equipo ha consumido {nombre}, ojala no tenga microplasticos')
            print(f'{descripcion}')
            # Como es un consumible, se aplica a todo el equipo
            for excavador in self.equipo:
                excavador.consumir(self.mochila[seleccion])
            # Por ultimo lo removemos de la mochila
            self.mochila.remove(self.mochila[seleccion])

        elif self.mochila[seleccion].tipo == 'Tesoro':
            # Como es un tesoso utilizamos nuestra funcion de abrir_tesoro
            # que aplica el efecto del tesoro uwu (evidentemente xd)
            self.abrir_tesoro(self.mochila[seleccion])

    def abrir_tesoro(self, tesoro):
        self.mochila.remove(tesoro)  # Antes que se nos olvide, removemos el item de la mochila :D
        # Como el tesoro depende de su calidad verificamos a cual corresponde
        if tesoro.calidad == 1:
            # Esta corresponde a añadir un excavador
            # primero verificamos si hay excavadores de dicho tipo disponibles uwu
            if self.excavadores_tipo(tesoro.cambio) != []:
                # De ser asi lo añadimos uno random de ese tipo al equipo
                nuevo_excavador = random.choice(self.excavadores_tipo(tesoro.cambio))
                # y lo eliminamos de los disponibles
                self.excavadores_disponibles.remove(nuevo_excavador)
                self.equipo.append(nuevo_excavador)
                print(f'{tesoro.descripcion}')
                print(f'HA SPAWNEADO {nuevo_excavador.nombre} :O')
            else:
                print(f'No hay mas excavadores tipo {tesoro.cambio}')

        elif tesoro.calidad == 2:
            # Esta corresponde a cambiar la arena, asi que elegimos una random del tipo indicado
            self.arena = random.choice(self.arenas_tipo(tesoro.cambio))
            print(f'WA LA ARENA CAMBIO AL TIPO {self.arena.tipo}')
