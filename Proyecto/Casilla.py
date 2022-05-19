class Casilla:

    LADO_MAXIMO = 200
    lado_segun_pantalla = 0
    lado = 0

    @staticmethod
    def calcular_tamanio_lado(root):
        screen_height = root.winfo_screenheight()
        Casilla.lado_segun_pantalla = int((screen_height - 150) / 8)
        Casilla.lado = Casilla.LADO_MAXIMO if Casilla.lado_segun_pantalla > Casilla.LADO_MAXIMO else Casilla.lado_segun_pantalla

    def __init__(self, fila, columna, color):
        self._fila = fila
        self._columna = columna
        self._color = color
        self._pieza = None
        self._label = None

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

    def get_label(self):
        return self._label

    def set_label(self, label):
        self._label = label

    def __str__(self):
        return f"Fila: {self._fila}. Columna: {self._columna}. " \
               f"Color: {self._color}. Pieza: {type(self._pieza).__name__}"
