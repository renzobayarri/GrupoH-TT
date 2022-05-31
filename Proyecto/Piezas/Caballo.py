from Proyecto.Piezas import Pieza as P


class Caballo(P.Pieza):

    def __init__(self, is_white):
        super().__init__(is_white)
        self._nombre = "caballo_blanco" if is_white else "caballo_negro"

    def get_is_edible(self, c):
        if c.get_pieza() is not None:
            if c.get_pieza().get_is_white() != self.get_is_white():
                print("if")
                return c
        else:
            return c
    def get_is_edible2(self, c):
        if c.get_pieza() is not None:
            if c.get_pieza().get_is_white() != self.get_is_white():
                print("if")
                return True
            else:
                return False
        else:
            return True

    def get_posibles_casillas_destino(self, casilla, casillas):
        casillas_destino = []
        fila = casilla.get_fila()
        columna = casilla.get_columna()
        """
        direcciones = [(-2, 1), (-2, -1), (2, 1), (2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2)]
        restricciones = [(7, 1), (0, 1), (6, 7), (6, 0), (6, 0), (1, 0), (7, 6), (7, 1)]
        
        for i in range(8):
            if columna < 7 and fila > 1:    #los signos < > cambian dependiendo de cada if (pensando como implementarlo)
                c = casillas[fila + direcciones[i][0]][columna + direcciones[i][1]]
                if self.get_is_edible2(c):
                    casillas_destino.append(self.get_is_edible(c))
        """
        if columna < 7 and fila > 1:
            c = casillas[fila - 2][columna + 1]
            if self.get_is_edible2(c):
                casillas_destino.append(self.get_is_edible(c))
        if columna > 0 and fila > 1:
            c = casillas[fila - 2][columna - 1]
            if self.get_is_edible2(c):
                casillas_destino.append(self.get_is_edible(c))
            #para atras
        if fila < 6 and columna < 7:
            c = casillas[fila + 2][columna + 1]
            if self.get_is_edible2(c):
                casillas_destino.append(self.get_is_edible(c))

        if fila < 6 and columna > 0:
            c = casillas[fila + 2][columna - 1]
            if self.get_is_edible2(c):
                casillas_destino.append(self.get_is_edible(c))
            # para adelante
        if columna < 6 and fila > 0:
            c = casillas[fila - 1][columna + 2]
            if self.get_is_edible2(c):
                casillas_destino.append(self.get_is_edible(c))
        if columna > 1 and fila > 0:
            c = casillas[fila - 1][columna - 2]
            if self.get_is_edible2(c):
                casillas_destino.append(self.get_is_edible(c))
            # para atras
        if fila < 7 and columna < 6:
            c = casillas[fila + 1][columna + 2]
            if self.get_is_edible2(c):
                casillas_destino.append(self.get_is_edible(c))

        if fila < 7 and columna > 1:
            c = casillas[fila + 1][columna - 2]
            if self.get_is_edible2(c):
                casillas_destino.append(self.get_is_edible(c))

        return casillas_destino



