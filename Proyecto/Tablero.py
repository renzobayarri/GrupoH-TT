from Proyecto.Piezas import *
import Casilla
import tkinter as tk
from tkinter import ttk


class Tablero:

    def __init__(self):
        self._casillas = []
        for fila in range(8):
            filas = []
            for columna in range(8):
                color = "sienna4" if (fila + columna) % 2 == 1 else "white"
                casilla = Casilla.Casilla(fila, columna, color)
                filas.append(casilla)
            self._casillas.append(filas)

    def get_casillas(self):
        return self._casillas

    def crear_piezas_iniciales(self):

        for fila in range(8):
            if fila in (2, 5):
                continue

            for columna in range(8):
                if fila == 0 or fila == 1:
                    blanca = False
                elif fila == 6 or fila == 7:
                    blanca = True

                if fila == 0 or fila == 7:
                    if columna == 0 or columna == 7:
                        self._casillas[fila][columna].set_pieza(Torre.Torre(blanca))
                    elif columna == 1 or columna == 6:
                        self._casillas[fila][columna].set_pieza(Caballo.Caballo(blanca))
                    elif columna == 2 or columna == 5:
                        self._casillas[fila][columna].set_pieza(Alfil.Alfil(blanca))
                    elif columna == 3:
                        self._casillas[fila][columna].set_pieza(Reina.Reina(blanca))
                    else:
                        self._casillas[fila][columna].set_pieza(Rey.Rey(blanca))
                elif fila == 1 or fila == 6:
                    self._casillas[fila][columna].set_pieza(Peon.Peon(blanca))

    def imprimir_casillas(self):
        for fila in self._casillas:
            for casilla in fila:
                print(casilla)

    def dibujar_tablero(self):
        root = tk.Tk()
        lado_maximo = 75
        screen_height = root.winfo_screenheight()
        lado_pantalla = int((screen_height - 150)/8)
        lado = lado_maximo if lado_pantalla > lado_maximo else lado_pantalla
        self.cargar_imagenes(lado)
        for i in range(8):
            root.columnconfigure(i)
            root.rowconfigure(i)
        img = tk.PhotoImage(width=lado, height=lado)
        for fila in self._casillas:
            for casilla in fila:
                if casilla.get_pieza() is None:
                    label = tk.Label(root, background=casilla.get_color(), image=img)
                else:
                    label = tk.Label(root, image=self._images_tk[casilla.get_pieza().get_nombre()]
                                      , background=casilla.get_color())
                label.grid(column=casilla.get_columna(), row=casilla.get_fila())

        root.mainloop()

    def cargar_imagenes(self, lado):

        reductor = int(150/lado)

        self._images_tk = {
            "torre_blanca": tk.PhotoImage(file="./assets/wr.png").subsample(reductor,reductor),
            "torre_negra": tk.PhotoImage(file="./assets/br.png").subsample(reductor,reductor),
            "caballo_blanco": tk.PhotoImage(file="./assets/wn.png").subsample(reductor,reductor),
            "caballo_negro": tk.PhotoImage(file="./assets/bn.png").subsample(reductor,reductor),
            "alfil_blanco": tk.PhotoImage(file="./assets/wb.png").subsample(reductor,reductor),
            "alfil_negro": tk.PhotoImage(file="./assets/bb.png").subsample(reductor,reductor),
            "reina_blanca": tk.PhotoImage(file="./assets/wq.png").subsample(reductor,reductor),
            "reina_negra": tk.PhotoImage(file="./assets/bq.png").subsample(reductor,reductor),
            "rey_blanco": tk.PhotoImage(file="./assets/wk.png").subsample(reductor,reductor),
            "rey_negro": tk.PhotoImage(file="./assets/bk.png").subsample(reductor,reductor),
            "peon_blanco": tk.PhotoImage(file="./assets/wp.png").subsample(reductor,reductor),
            "peon_negro": tk.PhotoImage(file="./assets/bp.png").subsample(reductor,reductor),
        }