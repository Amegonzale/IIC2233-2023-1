from copy import copy
from functools import reduce
from itertools import groupby
from typing import Generator

from utilidades import (
    Categoria, Producto, duplicador_generadores, generador_a_lista
)


# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------

def cargar_productos(ruta: str) -> Generator:
    with open(ruta, 'r', encoding="utf-8") as archivo:
        archivo.readline()
        for prod in archivo:
            id_producto, nombre, precio, pasillo, medida, unidad_medida = prod.strip().split(',')
            yield Producto(int(id_producto), nombre, int(precio), pasillo, int(medida), unidad_medida)


def cargar_categorias(ruta: str) -> Generator:
    with open(ruta, 'r', encoding="utf-8") as archivo:
        archivo.readline()
        for cat in archivo:
            nombre_categoria, id_producto = cat.strip().split(',')
            yield Categoria(nombre_categoria, int(id_producto))


# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------

def obtener_productos(generador_productos: Generator) -> map:
    nombres = map(lambda x: x[1], generador_productos)
    return nombres


def obtener_precio_promedio(generador_productos: Generator) -> int:
    copia1, copia2 = duplicador_generadores(generador_productos)
    suma = int(reduce(lambda x, y: x[2]+y[2], copia1))
    largo = reduce(lambda sum, element: sum + 1, copia2, 0)
    return int(suma / largo)


def filtrar_por_medida(generador_productos: Generator,
                       medida_min: float, medida_max: float, unidad: str
                       ) -> filter:
    copia1, copia2 = duplicador_generadores(generador_productos)
    filtro0 = filter(lambda x: x[5] == unidad, copia1)
    filtro1 = filter(lambda x: medida_min <= x[4], filtro0)
    filtro2 = filter(lambda x: x[4] <= medida_max, filtro1)
    return filtro2


def filtrar_por_categoria(generador_productos: Generator,
                          generador_categorias: Generator,
                          nombre_categoria: str) -> Generator:
    filtro1 = filter(lambda x: x[0] == nombre_categoria, generador_categorias)
    gen = generador_a_lista(map(lambda x: x[1], filtro1))
    filtro2 = filter(lambda x: x[0] in gen, generador_productos)
    return filtro2


def agrupar_por_pasillo(generador_productos: Generator) -> groupby:
    return groupby(generador_productos, lambda x: x[3])


# ----------------------------------------------------------------------------
# Parte 3: Iterables
# ----------------------------------------------------------------------------

class Carrito:
    def __init__(self, productos: list) -> None:
        self.productos = productos

    def __iter__(self):
        return IteradorCarrito(self.productos)


class IteradorCarrito:
    def __init__(self, iterable_productos: list) -> None:
        self.productos_iterable = copy(iterable_productos)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.productos_iterable) > 0:
            # Consigo todos los precios y el minimo entre ellos
            precios = map(lambda x: x[2], copy(self.productos_iterable))
            mini = min(precios)

            # encuentro todos los productos con ese precio
            aa = list(filter(lambda x: x[2] == mini, copy(self.productos_iterable)))

            # Consigo el index del primero
            index = self.productos_iterable.index(aa[0])

            # Le hago pop de la lista y guardo ese valor como el min para retornarlo
            menor = self.productos_iterable.pop(index)
            return menor
        raise StopIteration
