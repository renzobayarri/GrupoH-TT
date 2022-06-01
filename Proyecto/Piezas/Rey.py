from .Pieza import Pieza


class Rey(Pieza):

    def __init__(self, is_white):
        super().__init__(is_white)
        self._nombre = "rey_blanco" if is_white else "rey_negro"


    def get_posibles_casillas_destino(self, casilla, casillas):
        casillas_destino = []

        fila = casilla.get_fila()
        columna = casilla.get_columna()

        direcciones = [[(1, 0)], [(-1, 0)], [(0, 1)], [(0, -1)], [(1, -1)], [(-1, 1)], [(1, 1)], [(-1, -1)]]

        for direccion in direcciones:
            for fila_mv, columna_mv in direccion:
                try:
                    if not fila + fila_mv < 0 and not fila + fila_mv > 7 and not columna + columna_mv < 0 and not columna + columna_mv > 7:
                        c = casillas[fila + fila_mv][columna + columna_mv]
                        if c.get_pieza() is not None:
                            if c.get_pieza().get_is_white() != casilla.get_pieza().get_is_white():
                                casillas_destino.append(c)
                            break
                        else:
                            casillas_destino.append(c)
                except IndexError:
                    pass

        return casillas_destino
