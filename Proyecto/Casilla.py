class Casilla:

    def __init__(self, fila, columna, color):
        self._fila = fila
        self._columna = columna
        self._color = color
        self._pieza = None

    def get_fila(self):
        return self._fila

    def get_columna(self):
        return self._columna

    def get_color(self):
        return self._color

    def get_pieza(self):
        return self._pieza

    def set_pieza(self, pieza):
        self._pieza = pieza

    def __str__(self):
        return f"Fila: {self._fila}. Columna: {self._columna}. " \
               f"Color: {self._color}. Pieza: {type(self._pieza).__name__}"

