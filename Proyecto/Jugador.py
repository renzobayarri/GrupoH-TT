

class Jugador:

    def __init__(self):
        self._nombre = ""
        self._es_blanco = None
        self._tiempo_restante = None

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre):
        self._nombre = nombre

    def get_es_blanco(self):
        return self._es_blanco

    def set_es_blanco(self, es_blanco):
        self._es_blanco = es_blanco

    def get_tiempo_restante(self):
        return self._tiempo_restante

    def set_tiempo_restante(self,tiempo_restante):
        self._tiempo_restante = tiempo_restante
