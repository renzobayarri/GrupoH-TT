from Proyecto.Piezas import Pieza as P


class Caballo(P.Pieza):

    def __init__(self, is_white):
        super().__init__(is_white)
        self._nombre = "caballo_blanco" if is_white else "caballo_negro"

    def get_posibles_casillas_destino(self, casilla, casillas):
        casillas_destino = []

        fila = casilla.get_fila()
        columna = casilla.get_columna()

        if self._nombre == "caballo_blanco" or self._nombre == "caballo_negro":
            #para adelante
            if columna < 7 and fila > 1:
                c = casillas[fila - 2][columna + 1]
                if c.get_pieza() is not None:
                    if c.get_pieza().get_is_white() != self.get_is_white():
                        print("if")
                        casillas_destino.append(c)
                else:
                    casillas_destino.append(c)
            if columna > 0 and fila > 1:
                c = casillas[fila - 2][columna - 1]
                if c.get_pieza() is not None:
                    if c.get_pieza().get_is_white() != self.get_is_white():
                        print("if")
                        casillas_destino.append(c)
                else:
                    casillas_destino.append(c)
            #para atras
            if fila < 6 and columna < 7:
                c = casillas[fila + 2][columna + 1]
                if c.get_pieza() is not None:
                    if c.get_pieza().get_is_white() != self.get_is_white():
                        print("if")
                        casillas_destino.append(c)
                else:
                    casillas_destino.append(c)

            if fila < 6 and columna > 0:
                c = casillas[fila + 2][columna - 1]
                if c.get_pieza() is not None:
                    if c.get_pieza().get_is_white() != self.get_is_white():
                        print("if")
                        casillas_destino.append(c)
                else:
                    casillas_destino.append(c)


            # para adelante
            if columna < 6 and fila > 0:
                c = casillas[fila - 1][columna + 2]
                if c.get_pieza() is not None:
                    if c.get_pieza().get_is_white() != self.get_is_white():
                        print("if")
                        casillas_destino.append(c)
                else:
                    casillas_destino.append(c)
            if columna > 1 and fila > 0:
                c = casillas[fila - 1][columna - 2]
                if c.get_pieza() is not None:
                    if c.get_pieza().get_is_white() != self.get_is_white():
                        print("if")
                        casillas_destino.append(c)
                else:
                    casillas_destino.append(c)
            # para atras
            if fila < 7 and columna < 6:
                c = casillas[fila + 1][columna + 2]
                if c.get_pieza() is not None:
                    if c.get_pieza().get_is_white() != self.get_is_white():
                        print("if")
                        casillas_destino.append(c)
                else:
                    casillas_destino.append(c)

            if fila < 7 and columna > 1:
                c = casillas[fila + 1][columna - 2]
                if c.get_pieza() is not None:
                    if c.get_pieza().get_is_white() != self.get_is_white():
                        print("if")
                        casillas_destino.append(c)
                else:
                    casillas_destino.append(c)

        return casillas_destino

    def get_is_edible(self, casilla, casillas):
        pass;

