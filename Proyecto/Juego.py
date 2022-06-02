from Tablero import Tablero


class Juego:

    def __init__(self):
        self._jugador_blanco = None
        self._jugador_negro = None
        self._turno_blanco = True
        self._tablero = None
        self._modo = None  # entrenamiento, vsCPU, vsJug2, online
        self._cambio = None
        self._piezas_restantes = []
        self._piezas_eliminadas = []



    def get_jugador_blanco(self):
        return self._jugador_blanco

    def set_jugador_blanco(self, jugador_blanco):
        self._jugador_blanco = jugador_blanco

    def get_jugador_negro(self):
        return self._jugador_negro

    def set_jugador_negro(self, jugador_negro):
        self._jugador_negro = jugador_negro

    def get_turno_blanco(self):
        return self._turno_blanco

    def set_turno_blanco(self, turno_blanco):
        self._turno_blanco = turno_blanco

    def get_tablero(self):
        return self._tablero

    def set_tablero(self, vista_blanca):
        self._tablero = Tablero(vista_blanca)

    def get_modo(self):
        return self._modo

    def set_modo(self, modo):
        self._modo = modo

    def get_cambio(self):
        return self._cambio

    def set_cambio(self, cambio):
        self._cambio = cambio

    def get_piezas_restantes(self):
        return self._piezas_restantes

    def set_piezas_restantes(self, piezas_restantes):
        self._piezas_restantes = piezas_restantes

    def get_piezas_eliminadas(self):
        return self._piezas_eliminadas

    def set_piezas_eliminadas(self, piezas_eliminadas):
        self._piezas_eliminadas = piezas_eliminadas