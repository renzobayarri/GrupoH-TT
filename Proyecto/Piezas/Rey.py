from .Pieza import Pieza
from .Torre import Torre
from .Caballo import Caballo
from .Reina import Reina
from .Alfil import Alfil
from .Peon import Peon


class Rey(Pieza):

    def __init__(self, es_blanco):
        super().__init__(es_blanco)
        self._nombre = "rey_blanco" if es_blanco else "rey_negro"

    def get_posibles_casillas_destino(self, casilla, juego):
        casillas_destino = []

        fila = casilla.get_fila()
        columna = casilla.get_columna()

        casillas = juego.get_tablero().get_casillas()

        direcciones = [[(1, 0)], [(-1, 0)], [(0, 1)], [(0, -1)], [(1, -1)], [(-1, 1)], [(1, 1)], [(-1, -1)]]

        for direccion in direcciones:
            for fila_mv, columna_mv in direccion:
                try:
                    if not fila + fila_mv < 0 and not fila + fila_mv > 7 and not columna + columna_mv < 0 and not columna + columna_mv > 7:
                        c = casillas[fila + fila_mv][columna + columna_mv]
                        if c.get_pieza() is not None:
                            if c.get_pieza().get_es_blanca() != casilla.get_pieza().get_es_blanca():
                                if self.no_deja_rey_en_jaque(casilla, c, juego, True):
                                    casillas_destino.append(c)
                            break
                        else:
                            if self.no_deja_rey_en_jaque(casilla, c, juego, True):
                                casillas_destino.append(c)
                except IndexError:
                    pass

        return casillas_destino

    def get_datos_enroque(self, casilla, juego):
        datos_enroque = []

        direcciones = [
            [1, 2, 3],
            [-1, -2, -3, -4],
        ]

        fila = casilla.get_fila()
        columna = casilla.get_columna()

        casillas = juego.get_tablero().get_casillas()

        # Si el rey está en jaque, no puede hacer enroque
        if self.esta_en_jaque(casilla, casillas):
            return datos_enroque

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
                                "destino-torre": casillas[fila][columna+col-2] if col > 0 else casillas[fila][columna+col+3],
                                "destino-rey": casillas[fila][columna+col-1] if col > 0 else casillas[fila][columna+col+2]
                            }
                            if not self.esta_en_jaque_en_camino(casilla, enroque, juego):
                                datos_enroque.append(enroque)
        return datos_enroque

    def esta_en_jaque(self, casilla_rey, casillas):

        fila = casilla_rey.get_fila()
        columna = casilla_rey.get_columna()

        # simular movimiento caballo
        direcciones = [(-2, 1), (-2, -1), (2, 1), (2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2)]

        for i in range(8):
            try:
                if 0 <= fila + direcciones[i][0] <= 7 and 0 <= columna + direcciones[i][1] <= 7:
                    c = casillas[fila + direcciones[i][0]][columna + direcciones[i][1]]
                    if c.get_pieza() is not None and c.get_pieza().get_es_blanca() != self.get_es_blanca() \
                            and isinstance(c.get_pieza(), Caballo):
                        return True
            except IndexError:
                pass

        # Simular movimientos alfil
        direcciones = [[(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)],
                       [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)],
                       [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)],
                       [(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)]
                       ]
        for direccion in direcciones:
            for fila_mv, columna_mv in direccion:
                try:
                    if 0 <= fila + fila_mv <= 7 and 0 <= columna + columna_mv <= 7:
                        c = casillas[fila + fila_mv][columna + columna_mv]
                        if c.get_pieza() is not None:
                            if c.get_pieza().get_es_blanca() != self.get_es_blanca() \
                                    and isinstance(c.get_pieza(), (Alfil, Reina)):
                                return True
                            else:
                                break
                except IndexError:
                    pass

        # Simular movimientos torre:
        direcciones = [[(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)],
                       [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)],
                       [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)],
                       [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)]
                       ]

        for direccion in direcciones:
            for fila_mv, columna_mv in direccion:
                try:
                    if 0 <= fila + fila_mv <= 7 and 0 <= columna + columna_mv <= 7:
                        c = casillas[fila + fila_mv][columna + columna_mv]
                        if c.get_pieza() is not None:
                            if c.get_pieza().get_es_blanca() != self.get_es_blanca() \
                                    and isinstance(c.get_pieza(), (Torre, Reina)):
                                return True
                            else:
                                break
                except IndexError:
                    pass

        direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1), (1, 1), (-1, -1)]

        for direccion in direcciones:
            fila_mv, columna_mv = direccion
            try:
                if 0 <= fila + fila_mv <= 7 and 0 <= columna + columna_mv <= 7:
                    c = casillas[fila + fila_mv][columna + columna_mv]
                    if c.get_pieza() is not None \
                            and c.get_pieza().get_es_blanca() != casilla_rey.get_pieza().get_es_blanca():
                        if c.get_pieza().get_es_blanca():
                            if fila_mv == 1 and (columna_mv == -1 or columna_mv == 1):
                                if isinstance(c.get_pieza(), (Peon, Rey)):
                                    return True
                        else:
                            if fila_mv == -1 and (columna_mv == -1 or columna_mv == 1):
                                if isinstance(c.get_pieza(), (Peon, Rey)):
                                    return True
            except IndexError:
                pass

        return False

    def esta_en_jaque_en_camino(self, casilla, enroque, juego):

        rey_en_jaque = True

        casillas = juego.get_tablero().get_casillas()
        ultima_movida = juego.get_ultima_pieza_movida()

        self.simular_movimiento(casilla, enroque["destino-torre"], juego, True)
        if self.get_es_blanca():
            if not juego.get_jugador_blanco().get_casilla_rey().get_pieza().esta_en_jaque(
                    juego.get_jugador_blanco().get_casilla_rey(), casillas):
                self.simular_movimiento(enroque["destino-torre"], enroque["destino-rey"], juego, True)
                if not juego.get_jugador_blanco().get_casilla_rey().get_pieza().esta_en_jaque(
                        juego.get_jugador_blanco().get_casilla_rey(), casillas):
                    rey_en_jaque = False
                self.revertir_movimiento(enroque["destino-torre"], enroque["destino-rey"], juego, None, ultima_movida,
                                         True)
        else:
            if not juego.get_jugador_negro().get_casilla_rey().get_pieza().esta_en_jaque(
                    juego.get_jugador_negro().get_casilla_rey(), casillas):
                self.simular_movimiento(enroque["destino-torre"], enroque["destino-rey"], juego, True)
                if not juego.get_jugador_negro().get_casilla_rey().get_pieza().esta_en_jaque(
                        juego.get_jugador_negro().get_casilla_rey(), casillas):
                    rey_en_jaque = False
                self.revertir_movimiento(enroque["destino-torre"], enroque["destino-rey"], juego, None, ultima_movida,
                                         True)

        self.revertir_movimiento(casilla, enroque["destino-torre"], juego, None, ultima_movida, True)

        return rey_en_jaque
