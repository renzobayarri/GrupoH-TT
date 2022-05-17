from Proyecto.Piezas import Pieza as P


class Reina(P.Pieza):

    def __init__(self, is_white):
        super().__init__(is_white)
        self._nombre = "reina_blanca" if is_white else "reina_negra"

    def get_posibles_casillas_destino(self):
        pass;