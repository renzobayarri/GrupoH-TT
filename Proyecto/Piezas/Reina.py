from .Pieza import Pieza

class Reina(Pieza):

    def __init__(self, es_blanca):
        super().__init__(es_blanca)
        self._nombre = "reina_blanca" if es_blanca else "reina_negra"

    def get_posibles_casillas_destino(self, casilla, juego):
        casillas_destino = []

        fila = casilla.get_fila()
        columna = casilla.get_columna()

        casillas = juego.get_tablero().get_casillas()

        direcciones = [[(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)],
                       [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)],
                       [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)],
                       [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)],
                       [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)],
                       [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)],
                       [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)],
                       [(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)]]

        for direccion in direcciones:
            for fila_mv, columna_mv in direccion:
                try:
                    if not fila + fila_mv < 0 and not fila + fila_mv > 7 and not columna + columna_mv < 0 and not columna + columna_mv > 7:
                        c = casillas[fila + fila_mv][columna + columna_mv]
                        if c.get_pieza() is not None:
                            if c.get_pieza().get_es_blanca() != casilla.get_pieza().get_es_blanca():
                                if self.no_deja_rey_en_jaque(casilla, c, juego):
                                    casillas_destino.append(c)
                            break
                        else:
                            if self.no_deja_rey_en_jaque(casilla, c, juego):
                                casillas_destino.append(c)
                except IndexError:
                    pass
        return casillas_destino
