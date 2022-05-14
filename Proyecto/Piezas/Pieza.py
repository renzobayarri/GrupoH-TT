class Pieza:
    images = {
        "torre_blanca": "../assets/wRook.png",
        "torre_negra": "../assets/bRook.png",
        "caballo_blanco": "../assets/wKnight.png",
        "caballo_negro": "../assets/bKnight.png",
        "alfil_blanco": "../assets/wBishop.png",
        "alfil_negro": "../assets/bBishop.png",
        "reina_blanca": "../assets/wQueen.png",
        "reina_negra": "../assets/bQueen.png",
        "rey_blanco": "../assets/wKing.png",
        "rey_negro": "../assets/bKing.png",
        "peon_blanco": "../assets/wPawn.png",
        "peon_negro": "../assets/bPawn.png",
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
