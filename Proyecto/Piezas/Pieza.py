class Pieza:
    images = {
        "torre_blanca": "",
        "torre_negra": "",
        "caballo_blanco": "",
        "caballo_negro": "",
        "alfil_blanco": "",
        "alfil_negro": "",
        "reina_blanca": "",
        "reina_negra": "",
        "rey_blanco": "",
        "rey_negro": "",
        "peon_blanco": "",
        "peon_negro": "",
    }

    def __init__(self, is_white):
        self._isWhite = is_white
        self._casilla = None

    def get_is_white(self):
        return self._isWhite

    def get_casilla(self):
        return self._casilla

    def set_casilla(self, casilla):
        self._casilla = casilla
