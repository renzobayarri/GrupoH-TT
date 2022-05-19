from abc import ABC, abstractmethod


class Pieza(ABC):

    def __init__(self, is_white):
        self._isWhite = is_white
        self._nombre = ""
        self._image = None

    def get_is_white(self):
        return self._isWhite

    def get_nombre(self):
        return self._nombre

    def set_nombre(self,nombre):
        self._nombre = nombre

    def get_image(self):
        return self._image

    def set_image(self,image):
        self._image = image

    @abstractmethod
    def get_posibles_casillas_destino(self):
        pass
