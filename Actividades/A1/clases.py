from abc import ABC, abstractmethod

class Animal(ABC):
    identificador = 0

    def __init__(self, peso, nombre) -> None:
        self.nombre = nombre
        self.peso = peso
        self.identificador = Animal.identificador
        Animal.identificador += 1
        self.__energia = 100

    @property
    def energia(self):
        return self.__energia

    @energia.setter
    def energia(self, nueva_energia):
        if nueva_energia > 0:
            self.__energia = nueva_energia
        else:
            self.__energia = 0

    @abstractmethod
    def desplazarse(self):
        pass


class Terrestre(Animal, ABC):
    def __init__(self, cantidad_patas, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cantidad_patas = cantidad_patas

    def desplazarse(self):
        gasto = self.energia_gastada_por_desplazamiento()
        nueva_energia = self.energia - gasto
        self.energia = nueva_energia
        return 'caminando...'

    def energia_gastada_por_desplazamiento(self):
        return self.peso*5


class Acuatico(Animal, ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def desplazarse(self):
        gasto = self.energia_gastada_por_desplazamiento()
        nueva_energia = self.energia - gasto
        self.energia = nueva_energia
        return 'nadando...'

    def energia_gastada_por_desplazamiento(self):
        return self.peso*2

class Perro(Terrestre):
    def __init__(self, raza, *args, **kwargs) -> None:
        super().__init__(4, *args, **kwargs)
        self.raza = raza

    def ladrar(self):
        return 'guau guau'

    def desplazarse(self):
        return super().desplazarse()

class Pez(Acuatico):
    def __init__(self, color, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.color = color

    def nadar(self):
        return 'moviendo aleta'

class Ornitorrinco(Acuatico, Terrestre):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def desplazarse(self):
        gasto = (Acuatico.energia_gastada_por_desplazamiento(self) + Terrestre.energia_gastada_por_desplazamiento(self))//2
        nueva_energia = self.energia - gasto
        desplazarse = (Acuatico.desplazarse(self) + Terrestre.desplazarse(self))
        self.energia = nueva_energia
        return desplazarse

#No supe como hacer que no cambiara el identificador

if __name__ == '__main__':
    perro = Perro(nombre='Pongo', raza='Dalmata', peso=3)
    pez = Pez(nombre='Nemo', color='rojo', peso=1)
    ornitorrinco = Ornitorrinco(nombre='Perry', peso=2, cantidad_patas=6)

    perro.desplazarse()
    pez.desplazarse()
    ornitorrinco.desplazarse()
