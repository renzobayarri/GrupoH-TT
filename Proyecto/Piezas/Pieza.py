from abc import ABC, abstractmethod


class Pieza(ABC):

    def __init__(self, es_blanca):
        self._es_blanca = es_blanca
        self._nombre = ""
        self._image = None
        self._cantidad_movimientos = 0

    def get_es_blanca(self):
        return self._es_blanca

    def get_nombre(self):
        return self._nombre

    def set_nombre(self,nombre):
        self._nombre = nombre

    def get_image(self):
        return self._image

    def set_image(self,image):
        self._image = image

    def get_cantidad_movimientos(self):
        return self._cantidad_movimientos

    def set_cantidad_movimientos(self, movimientos):
        self._cantidad_movimientos = movimientos

    def aumentar_cantidad_movimientos(self):
        self._cantidad_movimientos += 1

    @abstractmethod
    def get_posibles_casillas_destino(self, casilla, casillas):
        pass
