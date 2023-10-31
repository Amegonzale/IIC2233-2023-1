import parametros
import random


class Arena ():
    def __init__(self, nombre, tipo, rareza, humedad, dureza, estatica, items) -> None:
        self.nombre = nombre
        self.tipo = tipo
        self._rareza = int(rareza)
        self._humedad = int(humedad)
        self._dureza = int(dureza)
        self._estatica = int(estatica)
        self.items = items
        self._dificultad_arena = round(
            (self.rareza + self.humedad + self.dureza + self.estatica) / 40, 2)
        self.probabilidad_items = parametros.PROB_ENCONTRAR_ITEM
        self.prob_consumible = parametros.PROB_ENCONTRAR_CONSUMIBLE
        self.prob_tesoro = parametros.PROB_ENCONTRAR_TESORO

    def setter_caracteristicas(self, caracteristica, nuevo_valor):
        '''
        Como hay varias caracteristicas de la clase
        que tienen un setter con las mismos limites
        (no puede ser menor que 1 y mayor que 10)
        entonces se define esta funcion que sera llamada
        en esos setters.
        '''
        if nuevo_valor >= 10:
            caracteristica = 10
        elif nuevo_valor <= 1:
            caracteristica = 1
        else:
            caracteristica = nuevo_valor
        return caracteristica

    '''
    Los artributos privados fueron definidos con un
    solo _ ya que ocacionaba problemas si utilizaba
    dos __. Para efectos del codigo cumplen la misma
    funcion y funcionan correctamente.
    '''

    @property
    def rareza(self):
        return self._rareza

    @rareza.setter
    def rareza(self, nueva_rareza):
        self._rareza = self.setter_caracteristicas(self._rareza, nueva_rareza)

    @property
    def humedad(self):
        return self._humedad

    @humedad.setter
    def humedad(self, nueva_humedad):
        self._humedad = self.setter_caracteristicas(self._humedad, nueva_humedad)

    @property
    def dureza(self):
        return self._dureza

    @dureza.setter
    def dureza(self, nueva_dureza):
        self._dureza = self.setter_caracteristicas(self._dureza, nueva_dureza)

    @property
    def estatica(self):
        return self._estatica

    @estatica.setter
    def estatica(self, nueva_estatica):
        self._estatica = self.setter_caracteristicas(self._estatica, nueva_estatica)

    @property
    def dificultad_arena(self):
        return self._dificultad_arena

    '''
    Luego de definir los properties y setters
    necesarios se definen dos funciones, que tienen
    como finalidad retornar una lista con un tipo de
    item en especifico dentro de la arena.
    '''

    def items_consumibles(self) -> list:
        '''
        Esta funcion esta hecha con el fin de tener
        en una lista todos los items del tipo consumibles
        dentro de la arena.
        '''
        consumibles = []
        for item in self.items:
            if item.tipo == 'Consumible':
                consumibles.append(item)
        return consumibles

    def items_tesoro(self) -> list:
        '''
        Esta funcion esta hecha con el fin de tener
        en una lista todos los items del tipo tesoro
        dentro de la arena.
        '''
        tesoros = []
        for item in self.items:
            if item.tipo == 'Tesoro':
                tesoros.append(item)
        return tesoros

    '''
    El __iter__ tiene el fin de facilitar el guardado
    de los datos de la partida.
    '''
    def __iter__(self):
        nombre = self.nombre
        tipo = self.tipo
        rareza = self.rareza
        humedad = self.humedad
        dureza = self.dureza
        estatica = self.estatica
        return iter(map(str, [nombre, tipo, rareza, humedad, dureza, estatica]))


'''
A continuacion se definen los distintos tipos de arenas
variando sus caracteristicas segun establece el enunciado.
'''


class ArenaNormal(Arena):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._dificultad_arena = round(parametros.POND_ARENA_NORMAL * self.dificultad_arena, 2)


class ArenaMojada(Arena):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.prob_consumible = 0.5
        self.prob_tesoro = 0.5


class ArenaRocosa(Arena):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._dificultad_arena = round(
            (self._rareza + self._humedad + 2 * self._dureza + self._estatica) / 50, 2)


class ArenaMagnetica(ArenaRocosa, ArenaMojada):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def nuevo_dia(self):
        '''
        Esta funcion sera llamada cada vez que se inicie
        el proceso de simular dia torneo, entonces estos
        atributos tomaran valores del 1 al 10 cada que eso
        ocurra
        '''
        self.humedad = random.randint(1, 10)
        self.dureza = random.randint(1, 10)
