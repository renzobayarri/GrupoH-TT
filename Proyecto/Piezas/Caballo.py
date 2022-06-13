from .Pieza import Pieza


class Caballo(Pieza):

    def __init__(self, es_blanca):
        super().__init__(es_blanca)
        self._nombre = "caballo_blanco" if es_blanca else "caballo_negro"

    def is_edible(self, c):
        if c.get_pieza() is not None:
            if c.get_pieza().get_es_blanca() != self.get_es_blanca():
                return True
            return False
        return True

    def get_posibles_casillas_destino(self, casilla, casillas):
        casillas_destino = []
        fila = casilla.get_fila()
        columna = casilla.get_columna()

        casillas = juego.get_tablero().get_casillas()

        direcciones = [(-2, 1), (-2, -1), (2, 1), (2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2)]
        
        for i in range(8):
            try:
                if fila + direcciones[i][0] >= 0 and fila + direcciones[i][0] <= 7 and columna + direcciones[i][1] >= 0 and columna + direcciones[i][1] <= 7:
                    c = casillas[fila + direcciones[i][0]][columna + direcciones[i][1]]
                    if self.is_edible(c):
                        if self.no_deja_rey_en_jaque(casilla, c, juego):
                            casillas_destino.append(c)
            except IndexError as e:
                pass

        return casillas_destino
