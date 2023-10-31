class Item:
    def __init__(self, nombre, tipo, descripcion) -> None:
        self.nombre = nombre
        self.tipo = tipo  # Consumible o Tesoro
        self.descripcion = descripcion


'''
Consumibles y Tesoros se construyen desde item y
añaden sus propios atributos
'''


class Consumibles(Item):
    def __init__(self,  nombre, tipo, descripcion, energia, fuerza, suerte, felicidad) -> None:
        super().__init__(nombre, tipo, descripcion)
        self.energia = int(energia)
        self.fuerza = int(fuerza)
        self.suerte = int(suerte)
        self.felicidad = int(felicidad)


class Tesoros(Item):
    def __init__(self, nombre, tipo, descripcion, calidad, cambio) -> None:
        super().__init__(nombre, tipo, descripcion)
        self.calidad = int(calidad)
        self.cambio = cambio
