from Proyecto.Piezas import Pieza as P


class Caballo(P.Pieza):

    def __init__(self, is_white):
        super().__init__(is_white)
        self._nombre = "caballo_blanco" if is_white else "caballo_negro"

    def get_posibles_casillas_destino(self):
        pass;
