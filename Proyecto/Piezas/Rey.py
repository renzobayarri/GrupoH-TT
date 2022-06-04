from .Pieza import Pieza
from .Torre import Torre


class Rey(Pieza):

    def __init__(self, es_blanco):
        super().__init__(es_blanco)
        self._nombre = "rey_blanco" if es_blanco else "rey_negro"

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
                            if c.get_pieza().get_es_blanca() != casilla.get_pieza().get_es_blanca():
                                casillas_destino.append(c)
                            break
                        else:
                            casillas_destino.append(c)
                except IndexError:
                    pass

        return casillas_destino

    def get_datos_enroque(self, casilla, casillas):
        datos_enroque = []

        direcciones = [
            [1, 2, 3],
            [-1, -2, -3, -4],
        ]

        fila = casilla.get_fila()
        columna = casilla.get_columna()

        # Falta validar que el rey no esté en jaque
        # Falta validar que el camino que hace el rey no esté en jaque

        if not self._cantidad_movimientos:
            for direccion in direcciones:
                for col in direccion:
                    c = casillas[fila][columna+col]
                    if col != 3 and col != -4:
                        if c.get_pieza() is not None:
                            # Hay piezas en el camino
                            break
                    else:
                        if c.get_pieza() is not None and isinstance(c.get_pieza(), Torre) and not c.get_pieza().get_cantidad_movimientos():
                            enroque = {
                                "origen-torre": c,
                                "destino-torre" : casillas[fila][columna+col-2] if col > 0 else casillas[fila][columna+col+3],
                                "destino-rey" : casillas[fila][columna+col-1] if col > 0 else casillas[fila][columna+col+2]
                            }
                            datos_enroque.append(enroque)
        return datos_enroque
