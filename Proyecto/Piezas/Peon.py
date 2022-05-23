from Proyecto.Piezas import Pieza as P


class Peon(P.Pieza):

    def __init__(self, is_white):
        super().__init__(is_white)
        self.primera_jugada = True
        self._nombre = "peon_blanco" if is_white else "peon_negro"

    def get_posibles_casillas_destino(self, fila, columna):

        if self.primera_jugada == True:
            if self._nombre == "peon_blanco":
                return f"peon se puede a mover fila:{fila - 2} y columna {columna}" \
                       f" o fila:{fila - 1} y columna {columna}"
            else:
                return f"peon se puede a mover fila:{fila + 2} y columna {columna}" \
                       f" o fila:{fila + 1} y columna {columna}"
        else:
            if self._nombre == "peon_blanco":
                return f"peon se puede a mover fila:{fila - 1} y columna {columna}"
            else:
                return f"peon se puede a mover fila:{fila + 1} y columna {columna}"