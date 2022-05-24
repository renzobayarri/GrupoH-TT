from Proyecto.Piezas import Pieza as P


class Peon(P.Pieza):

    def __init__(self, is_white):
        super().__init__(is_white)
        self._primera_jugada = True
        self._nombre = "peon_blanco" if is_white else "peon_negro"

    def get_primera_jugada(self):
        return self._primera_jugada

    def set_primera_jugada(self, primera_jugada):
        self._primera_jugada = primera_jugada

    def get_posibles_casillas_destino(self, casilla, casillas):
        direccion = -1 if self.get_is_white() else 1 # Si son blancas, se mueven hacia filas con indice menor ( 7 a 0)
        casillas_destino = []

        fila = casilla.get_fila()
        columna = casilla.get_columna()

        if fila == 0 or fila == 7:
            # Los peones no pueden moverse
            return casillas_destino

        c = casillas[fila+direccion][columna]
        if c.get_pieza() is None:
            casillas_destino.append(c)
        if columna != 0:
            c = casillas[fila+direccion][columna-1]
            if c.get_pieza() is not None and c.get_pieza().get_is_white() != self.get_is_white():
                casillas_destino.append(c)
        if columna != 7:
            c = casillas[fila+direccion][columna+1]
            if c.get_pieza() is not None and c.get_pieza().get_is_white() != self.get_is_white():
                casillas_destino.append(c)
        if self._primera_jugada:
            c = casillas[fila+(direccion*2)][columna]
            if c.get_pieza() is None:
                casillas_destino.append(c)

        return casillas_destino
