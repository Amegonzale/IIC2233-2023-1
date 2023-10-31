from collections import defaultdict, deque


class Jugador:
    def __init__(self, nombre: str, velocidad: int) -> None:
        self.nombre = nombre
        self.velocidad = velocidad
    
    def __repr__(self) -> None:
        return f'Jugador: {self.nombre}, Velocidad: {self.velocidad}'


class Equipo:
    def __init__(self) -> None:
        self.jugadores = dict()
        self.dict_adyacencia = defaultdict(set)
    
    def agregar_jugador(self, id_jugador: int, jugador: Jugador) -> bool:
        if id_jugador in self.jugadores:
            return False
        else:
            self.jugadores[id_jugador] = jugador
            return True

    def agregar_vecinos(self, id_jugador: int, vecinos: list[int]) -> int:
        if id_jugador not in self.jugadores:
            return -1
        else:
            if id_jugador not in self.dict_adyacencia:
                self.dict_adyacencia[id_jugador] = set()
            num_new_vecinos = 0
            for vecino in vecinos:
                if vecino not in self.dict_adyacencia[id_jugador]:
                    num_new_vecinos += 1
                    self.dict_adyacencia[id_jugador].add(vecino)
            return num_new_vecinos

    def mejor_amigo(self, id_jugador: int) -> Jugador:
        jugador = self.jugadores[id_jugador]
        # lista de todos los vecinos
        vecinos = []
        for id_j in self.dict_adyacencia[id_jugador]:
            vecinos.append(self.jugadores[id_j])

        if vecinos == []:
            return None

        # Ahora comparamos velocidades
        menor_dif = abs(jugador.velocidad - vecinos[0].velocidad)
        bestie = vecinos[0]
        for vecino in vecinos:
            dif = abs(jugador.velocidad - vecino.velocidad)
            if dif < menor_dif:
                bestie = vecino
                menor_dif = dif
        return bestie

    def peor_compañero(self, id_jugador: int) -> Jugador:
        if len(self.dict_adyacencia.keys()) == 1:
            return None

        jugador = self.jugadores[id_jugador]
        mayor_dif = 0
        peor = None
        for ide in self.jugadores.keys():
            dif = abs(jugador.velocidad-self.jugadores[ide].velocidad)
            if dif > mayor_dif:
                peor = self.jugadores[ide]
                mayor_dif = dif
        return peor

    def peor_conocido(self, id_jugador: int) -> Jugador:
        # primero haremos una lista con los ides de todos los compañeros con los que conecta
        # lo hare con bfs pq puedo xd

        visitados = []
        queue = deque([id_jugador])
        while len(queue)>0:
            compa = queue.popleft()
            if compa in visitados:
                continue
            visitados.append(compa)
            for vecino in self.dict_adyacencia[compa]:
                if vecino not in visitados:
                    queue.append(vecino)

        # ahora q tenemos la lista buscamos
        jugador = self.jugadores[id_jugador]
        mayor_dif = 0
        peor = None
        for ide in visitados:
            dif = abs(jugador.velocidad-self.jugadores[ide].velocidad)
            if dif > mayor_dif:
                peor = self.jugadores[ide]
                mayor_dif = dif
        return peor

    def distancia(self, id_jugador_1: int, id_jugador_2: int) -> int:
        if id_jugador_1 == id_jugador_2:
            return 0
        caminos = [[id_jugador_1]]
        index_camino = 0

        visitados = []

        while index_camino < len(caminos):
            camino_actual = caminos[index_camino]
            ultimo = camino_actual[-1]
            siguente = self.dict_adyacencia[ultimo]

            if id_jugador_2 in siguente:
                camino_actual.append(id_jugador_2)
                return len(camino_actual)-1

            for sig in siguente:
                if sig not in visitados:
                    nuevo_camino = camino_actual[:]
                    nuevo_camino.append(sig)
                    caminos.append(nuevo_camino)
                    visitados.append(sig)

            index_camino += 1
            
        return -1
    

if __name__ == '__main__':
    equipo = Equipo()
    jugadores = {
        0: Jugador('Alonso', 1),
        1: Jugador('Alba', 3),
        2: Jugador('Alicia', 6),
        3: Jugador('Alex', 10)
    }
    adyacencia = {
        0: [1],
        1: [0, 2],
        2: [1],
    }
    for idj, jugador in jugadores.items():
        equipo.agregar_jugador(id_jugador=idj, jugador=jugador)
    for idj, vecinos in adyacencia.items():
        equipo.agregar_vecinos(id_jugador=idj, vecinos=vecinos)
    
    print(f'El mejor amigo de Alba es {equipo.mejor_amigo(1)}') 
    print(f'El peor compañero de Alonso es {equipo.peor_compañero(0)}')
    print(f'El peor amigo de Alicia es {equipo.peor_compañero(2)}')
    print(f'La distancia entre Alicia y Alonso es {equipo.distancia(2, 0)}')
    print(f'La distancia entre Alba y Alex es {equipo.distancia(1, 3)}')
    