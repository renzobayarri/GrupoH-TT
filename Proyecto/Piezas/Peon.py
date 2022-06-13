from .Pieza import Pieza


class Peon(Pieza):

    def __init__(self, es_blanco):
        super().__init__(es_blanco)
        self._nombre = "peon_blanco" if es_blanco else "peon_negro"

    def get_posibles_casillas_destino(self, casilla, juego):
        direccion = -1 if self.get_es_blanca() else 1  # Si son blancas, se mueven hacia filas con indice menor ( 7 a 0)

        casillas_destino = []

        fila = casilla.get_fila()
        columna = casilla.get_columna()

        casillas = juego.get_tablero().get_casillas()

        if fila == 0 or fila == 7:
            # Los peones no pueden moverse
            return casillas_destino

        c = casillas[fila + direccion][columna]
        if c.get_pieza() is None:

            if self.no_deja_rey_en_jaque(casilla, c, juego):
                casillas_destino.append(c)

            if not self._cantidad_movimientos:
                c = casillas[fila + (direccion * 2)][columna]
                if c.get_pieza() is None:
                    if self.no_deja_rey_en_jaque(casilla, c, juego):
                        casillas_destino.append(c)
        if columna != 0:
            c = casillas[fila + direccion][columna - 1]
            if c.get_pieza() is not None and c.get_pieza().get_es_blanca() != self.get_es_blanca():
                if self.no_deja_rey_en_jaque(casilla, c, juego):
                    casillas_destino.append(c)
        if columna != 7:
            c = casillas[fila + direccion][columna + 1]
            if c.get_pieza() is not None and c.get_pieza().get_es_blanca() != self.get_es_blanca():
                if self.no_deja_rey_en_jaque(casilla, c, juego):
                    casillas_destino.append(c)

        return casillas_destino

    def get_info_al_paso(self, casilla, juego):
        info = []
        casillas = juego.get_tablero().get_casillas()
        ultima_pieza = juego.get_ultima_pieza_movida()

        if casilla.get_pieza().get_es_blanca():
            if casilla.get_fila() != 3:
                return info
            direcciones = [[-1, 1], [-1, -1]]
        else:
            if casilla.get_fila() != 4:
                return info
            direcciones = [[1, 1], [1, -1]]

        fila = casilla.get_fila()
        columna = casilla.get_columna()

        for direccion in direcciones:
            fila_mv, columna_mv = direccion
            if casillas[fila][columna + columna_mv].get_pieza() is not None \
                and casillas[fila][columna + columna_mv].get_pieza().get_es_blanca() != casilla.get_pieza().get_es_blanca() \
                and casillas[fila][columna + columna_mv].get_pieza().get_cantidad_movimientos() == 1 \
                    and casillas[fila][columna + columna_mv].get_pieza() == ultima_pieza:
                        peon_al_paso = {}
                        peon_al_paso["origen-peon"] = casilla
                        peon_al_paso["peon-comible"] = casillas[fila][columna + columna_mv]
                        peon_al_paso["destino-peon"] = casillas[fila + fila_mv][columna + columna_mv]
                        if self.peon_al_paso_no_deja_rey_en_jaque(peon_al_paso, juego):
                            info.append(peon_al_paso)

        return info

    def peon_al_paso_no_deja_rey_en_jaque(self, peon_al_paso, juego):

        no_deja_rey_en_jaque = False
        casillas = juego.get_tablero().get_casillas()
        pieza_destino = peon_al_paso["peon-comible"].get_pieza()
        ultima_movida = juego.get_ultima_pieza_movida()

        self.simular_movimiento(peon_al_paso["origen-peon"], peon_al_paso["peon-comible"], juego, False)
        self.simular_movimiento(peon_al_paso["peon-comible"], peon_al_paso["destino-peon"], juego, False)
        if self.get_es_blanca():
            if not juego.get_jugador_blanco().get_casilla_rey().get_pieza().esta_en_jaque(
                    juego.get_jugador_blanco().get_casilla_rey(), casillas):
                no_deja_rey_en_jaque = True
        else:
            if not juego.get_jugador_negro().get_casilla_rey().get_pieza().esta_en_jaque(
                    juego.get_jugador_negro().get_casilla_rey(), casillas):
                no_deja_rey_en_jaque = True

        self.revertir_movimiento(peon_al_paso["peon-comible"], peon_al_paso["destino-peon"], juego, None, ultima_movida,
                                 False)
        self.revertir_movimiento(peon_al_paso["origen-peon"], peon_al_paso["peon-comible"], juego, pieza_destino,
                                 ultima_movida, False)

        return no_deja_rey_en_jaque

