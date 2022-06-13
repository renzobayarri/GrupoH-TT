from abc import ABC, abstractmethod


class Pieza(ABC):

    def __init__(self, es_blanca):
        self._es_blanca = es_blanca
        self._nombre = ""
        self._image = None
        self._cantidad_movimientos = 0

    def get_es_blanca(self):
        return self._es_blanca

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre):
        self._nombre = nombre

    def get_image(self):
        return self._image

    def set_image(self, image):
        self._image = image

    def get_cantidad_movimientos(self):
        return self._cantidad_movimientos

    def set_cantidad_movimientos(self, movimientos):
        self._cantidad_movimientos = movimientos

    def aumentar_cantidad_movimientos(self):
        self._cantidad_movimientos += 1

    def disminuir_cantidad_movimientos(self):
        self._cantidad_movimientos -= 1

    def simular_movimiento(self, origen, destino, juego, es_rey):

        destino.set_pieza(origen.get_pieza())

        origen.get_pieza().aumentar_cantidad_movimientos()
        juego.set_ultima_pieza_movida(origen.get_pieza())

        # En la clase Rey, guardar las variables
        if es_rey:
            if origen.get_pieza().get_es_blanca():
                juego.get_jugador_blanco().set_casilla_rey(destino)
            else:
                juego.get_jugador_negro().set_casilla_rey(destino)

        origen.set_pieza(None)

    def revertir_movimiento(self, origen, destino, juego, pieza_destino_anterior, pieza_movida_anterior, es_rey):

        origen.set_pieza(destino.get_pieza())
        destino.get_pieza().disminuir_cantidad_movimientos()
        juego.set_ultima_pieza_movida(pieza_movida_anterior)

        if es_rey:
            if destino.get_pieza().get_es_blanca():
                juego.get_jugador_blanco().set_casilla_rey(origen)
            else:
                juego.get_jugador_negro().set_casilla_rey(origen)

        destino.set_pieza(pieza_destino_anterior)

    def no_deja_rey_en_jaque(self, casilla, c, juego, es_rey=False):

        no_deja_rey_en_jaque = False
        casillas = juego.get_tablero().get_casillas()
        pieza_destino = c.get_pieza()
        ultima_movida = juego.get_ultima_pieza_movida()

        self.simular_movimiento(casilla, c, juego, es_rey)
        if self.get_es_blanca():
            if not juego.get_jugador_blanco().get_casilla_rey().get_pieza().esta_en_jaque(
                    juego.get_jugador_blanco().get_casilla_rey(), casillas):
                no_deja_rey_en_jaque = True
        else:
            if not juego.get_jugador_negro().get_casilla_rey().get_pieza().esta_en_jaque(
                    juego.get_jugador_negro().get_casilla_rey(), casillas):
                no_deja_rey_en_jaque = True

        self.revertir_movimiento(casilla, c, juego, pieza_destino, ultima_movida, es_rey)

        return no_deja_rey_en_jaque

    @abstractmethod
    def get_posibles_casillas_destino(self, casilla, casillas):
        pass
