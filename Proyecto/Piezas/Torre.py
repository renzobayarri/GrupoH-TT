from Proyecto.Piezas import Pieza as P


class Torre(P.Pieza):

    def __init__(self, is_white):
        super().__init__(is_white)
        self._nombre = "torre_blanca" if is_white else "torre_negra"

    def get_posibles_casillas_destino(self):
        pass;
