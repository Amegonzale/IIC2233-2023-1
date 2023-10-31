from abc import ABC, abstractmethod
import parametros
import random


class Excavador(ABC):
    def __init__(self, nombre, tipo, edad, energia, fuerza, suerte, felicidad) -> None:
        self.nombre = nombre
        self.tipo = tipo
        self._edad = int(edad)
        self._energia = int(energia)
        self._fuerza = int(fuerza)
        self._suerte = int(suerte)
        self._felicidad = int(felicidad)
        self.descansando = False
        self._dias_por_descansar = 0

    '''
    A continuacion se definen los properties y
    los setters de las caracteristicas de la clase
    como corresponden :D
    '''

    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, nueva_edad):
        if nueva_edad >= 60:
            self._edad = 60
        elif nueva_edad <= 18:
            self._edad = 18
            # We dont support child labour
        else:
            self._edad = nueva_edad

    @property
    def energia(self):
        return self._energia

    @energia.setter
    def energia(self, nueva_energia):
        if nueva_energia >= 100:
            self._energia = 100
        elif nueva_energia <= 0:
            self._energia = 0
        else:
            self._energia = nueva_energia

    def setter_caracteristicas(self, caracteristica, nuevo_valor):
        '''
        Al igual que en arena, utilizo esta funcion
        para aplicarla a varios setters, ya que todos
        tienen los mismos limites. Asi el codigo queda mas
        claro y es mas consiso.
        eficiencia :D
        '''
        if nuevo_valor >= 10:
            caracteristica = 10
        elif nuevo_valor <= 1:
            caracteristica = 1
        else:
            caracteristica = nuevo_valor
        return caracteristica

    @property
    def fuerza(self):
        return self._fuerza

    @fuerza.setter
    def fuerza(self, nueva_fuerza):
        self._fuerza = self.setter_caracteristicas(self._fuerza, nueva_fuerza)

    @property
    def suerte(self):
        return self._suerte

    @suerte.setter
    def suerte(self, nueva_suerte):
        self._suerte = self.setter_caracteristicas(self._suerte, nueva_suerte)

    @property
    def felicidad(self):
        return self._felicidad

    @felicidad.setter
    def felicidad(self, nueva_felicidad):
        self._felicidad = self.setter_caracteristicas(self._felicidad, nueva_felicidad)

    '''
    El siguente atributo se encarga de ver si
    al excavador aun le corresponen dias de descanso,
    el setter esta diseñado asi por que, por cada dia
    que transcurre se le resta uno a dias_por_descansar
    '''

    @property
    def dias_por_descansar(self):
        return self._dias_por_descansar

    @dias_por_descansar.setter
    def dias_por_descansar(self, nuevo_dia):
        if nuevo_dia >= 0:
            self._dias_por_descansar = nuevo_dia
        else:
            self._dias_por_descansar = 0

    @abstractmethod
    def cavar(self, arena: object) -> float:
        '''
        La funcion de cavar es bien autodescriptiva,
        se utiliza para ver cuantos metros cava cada
        uno de los excavadores segun sus stats. Tiene
        como parametro la arena actual ya que de eso
        depende cuanto cavan. Finalmente se resta la
        energia utilizada.
        '''
        '''
        Separe la formula del enunciado en dos
        partes, de esa forma el codigo queda mas
        legible ^^ la parte 1 se multiplica con la 2
        '''
        parte1 = ((30 / self.edad) + ((self.felicidad + 2 * self.fuerza) / 10))
        parte2 = 1 / (10 * arena.dificultad_arena)
        metros_cavados = round((parte1 * parte2), 2)
        self.energia -= self.gastar_energia()
        return metros_cavados

    @abstractmethod
    def gastar_energia(self) -> int:
        '''
        Retorna la enegia gastada por el excavador
        a la hora de cavar :D
        '''
        return int(10 / self.fuerza + self.edad / 6)

    def descansar(self) -> int:
        '''
        calcula los dias que debe descansar una vez la energia
        llega a cero.
        '''
        dias_descanso = int(self.edad / 20)
        return dias_descanso

    def encontrar_item(self, arena: object) -> float:
        '''
        La funcion se encarga de encontrar items en la
        arena actual.
        '''
        # Primero calculamos la probabilidad de encontrar un item por el excavador
        probabilidad_item = arena.probabilidad_items * (self.suerte / 10)
        item_encontrado = None  # Asumimos en primera instancia que no encuentra nada
        # Vemos si la probabilidad acierta
        tipo = arena.tipo  # Si la arena es mojada o magnetica siempre encontraran items
        if random.random() <= probabilidad_item or tipo == 'mojada' or tipo == 'magnetica':
            eventos = ['Consumible', 'Tesoro']
            pesos = [arena.prob_consumible, arena.prob_tesoro]

            # Si acierta elegimos un evento segun el peso de su probabilidad de ocurrir
            # Lo guardamos y lo removemos de la arena
            tipo_item_encontrado = random.choices(eventos, weights=pesos, k=1)[0]
            if tipo_item_encontrado == 'Consumible' and arena.items_consumibles() != []:
                item_encontrado = random.choice(arena.items_consumibles())
                arena.items.remove(item_encontrado)
            elif tipo_item_encontrado == 'Tesoro' and arena.items_tesoro() != []:
                item_encontrado = random.choice(arena.items_tesoro())
                arena.items.remove(item_encontrado)
        return item_encontrado

    @abstractmethod
    def consumir(self, consumible: object):
        '''
        Bastante autodescriptivo, recive un consumible
        y aplica el stat que tiene en el excavador
        (sea positivo o negativo) uwu
        '''
        self.energia += consumible.energia
        self.fuerza += consumible.fuerza
        self.suerte += consumible.suerte
        self.felicidad += consumible.felicidad

    def un_dia_mas(self):
        '''
        Esta funcion ocurre cada dia simulado, se encarga de
        estar al tanto de si el excavador deberia estar o no
        descansando.
        '''
        dias_descansados = self.dias_por_descansar
        self.dias_por_descansar = dias_descansados - 1

        if self.energia == 0 and self.descansando is False:
            # Si la energia llega a cero y no esta descansando lo manda a acostarse xD
            self.dias_por_descansar = self.descansar()
            print(f'{self.nombre} se fue a mimir <3...')
        elif self.energia == 0 and self.descansando is True and self.dias_por_descansar == 0:
            # Si acaba de terminar de descansar lo despierta y le restaura la energia
            self.energia = 100
            print(f'{self.nombre} esta totalmente descansado uwu')

        if self.dias_por_descansar == 0:
            self.descansando = False
        else:
            self.descansando = True

    def __iter__(self):
        '''
        Utilizado con el fin de facilitar el guardado
        de los datos. retorna un iterable :P
        '''
        nombre = self.nombre
        tipo = self.tipo
        edad = self.edad
        energia = self.energia
        fuerza = self.fuerza
        suerte = self.suerte
        felicidad = self.felicidad
        return iter(map(str, [nombre, tipo, edad, energia, fuerza, suerte, felicidad]))


class ExcavadorDocencio(Excavador):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def gastar_energia(self) -> int:
        return super().gastar_energia()

    def consumir(self, consumible: object):
        return super().consumir(consumible)

    def cavar(self, arena: object) -> float:
        '''
        Reescribe el cavar de excavador ya que su
        funcion varia en ciertos elementos
        '''
        parte1 = (30 / self.edad) + ((self.felicidad + 2 * self.fuerza) / 10)
        parte2 = 1 / (10 * arena.dificultad_arena)
        metros_cavados = round((parte1 * parte2), 2)

        # felicidad y fuerza adicional luego de cavar
        self.felicidad += parametros.FELICIDAD_ADICIONAL_DOCENCIO
        self.fuerza += parametros.FUERZA_ADICIONAL_DOCENCIO
        # gasto de energia adicional luego de cavar
        gastar_energia = parametros.ENERGIA_PERDIDA_DOCENCIO + self.gastar_energia()
        self.energia -= gastar_energia
        return metros_cavados


class ExcavadorTareo(Excavador):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def cavar(self, arena: object) -> float:
        return super().cavar(arena)

    def gastar_energia(self) -> int:
        return super().gastar_energia()

    def consumir(self, consumible: object):
        '''
        Reescribe consumir ya que esta clase consigue beneficios
        extra al usar un consumible.
        '''
        self.energia += (consumible.energia + parametros.ENERGIA_ADICIONAL_TAREO)
        self.fuerza += consumible.fuerza
        self.suerte += (consumible.suerte + parametros.SUERTE_ADICIONAL_TAREO)
        self.felicidad += (consumible.felicidad - parametros.FELICIDAD_PERDIDA_TAREO)
        self.edad += parametros.EDAD_ADICIONAL_TAREO


class ExcavadorHíbrido(ExcavadorDocencio, ExcavadorTareo):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def gastar_energia(self) -> int:
        '''
        Reescribe el metodo de gastar energia
        '''
        energia_gastada = int((10 / self.fuerza + self.edad / 6) / 2)
        return energia_gastada

    @ExcavadorDocencio.energia.setter
    def energia(self, nueva_energia):
        '''
        Reescribe el setter de energia, asegurandose
        que no baje de 20 energia
        '''
        if nueva_energia >= 100:
            self._energia = 100
        elif nueva_energia <= 20:
            self._energia = 20
        else:
            self._energia = nueva_energia
