import os
from PyQt5.QtCore import QObject, pyqtSignal
import parametros


class ProcesadorInicio(QObject):

    senal_mapas = pyqtSignal(list)
    senal_valid_username = pyqtSignal(int)
    senal_username = pyqtSignal(str)

    def lista_mapas(self):
        mapas = os.listdir(os.path.join('mapas'))
        mapas = [mapa.split('.')[0] for mapa in mapas]
        self.senal_mapas.emit(mapas)

    def username_valido(self, username):
        largo_username = len(username)
        minimo = parametros.MIN_CARACTERES
        maximo = parametros.MAX_CARACTERES

        if username.isalnum() and largo_username >= minimo and largo_username <= maximo:
            self.senal_valid_username.emit(0)
            self.senal_username.emit(username)

        elif username.isalnum() is not True:
            self.senal_valid_username.emit(1)

        elif largo_username < minimo:
            self.senal_valid_username.emit(2)

        elif largo_username > maximo:
            self.senal_valid_username.emit(3)
