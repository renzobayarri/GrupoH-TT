from Proyecto.Piezas import Pieza as P


class Alfil(P.Pieza):

    def __init__(self, is_white):
        super().__init__(is_white)
        self._nombre = "alfil_blanco" if is_white else "alfil_negro"

    def get_posibles_casillas_destino(self):
        pass;