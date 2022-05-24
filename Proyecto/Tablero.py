from Proyecto.Piezas import *
import Casilla
import tkinter as tk
from tkinter import ttk


class Tablero:

    def __init__(self):
        self._casillas = []
        self._casilla_seleccionada = None
        self._casillas_posibles_destino = []
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
                for columna in range(8):
                    self._casillas[fila][columna].set_pieza(None)

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

    def cargar_imagenes(self, lado):

        reductor = int(150/lado) if lado <= 75 else 2

        self._images_tk = {
            "vacia" : tk.PhotoImage(width=lado, height=lado),
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

    def asignar_labels_imagenes(self,root):
        for fila in self._casillas:
            for casilla in fila:
                casilla.set_label(tk.Label(root, background=casilla.get_color()))
                if casilla.get_pieza() is None:
                    casilla.get_label()["image"] = self._images_tk['vacia']
                    casilla.get_label().bind("<Button>", lambda event, casilla=casilla: self.click(casilla=casilla))
                else:
                    casilla.get_pieza().set_image(self._images_tk[casilla.get_pieza().get_nombre()])
                    casilla.get_label()["image"] = casilla.get_pieza().get_image()
                    casilla.get_label().bind("<Button>", lambda event, casilla=casilla: self.click(casilla=casilla))
                casilla.get_label().grid(column=casilla.get_columna(), row=casilla.get_fila())

    def dibujar_tablero(self):
        root = tk.Tk()
        Casilla.Casilla.calcular_tamanio_lado(root)

        for i in range(8):
            root.columnconfigure(i)
            root.rowconfigure(i)

        self.cargar_imagenes(Casilla.Casilla.lado)
        self.asignar_labels_imagenes(root)

        root.mainloop()

    def click(self, casilla):
        if self._casilla_seleccionada:
            if casilla in self._casillas_posibles_destino:
                self.mover(casilla)
                self.cancelar_seleccion()
            else:
                self.cancelar_seleccion()
                if casilla.get_pieza() is not None:
                    self.seleccionar_casilla(casilla)
        else:
            if casilla.get_pieza() is not None:
                self.seleccionar_casilla(casilla)

    def seleccionar_casilla(self,casilla):
        self._casilla_seleccionada = casilla
        self._casillas_posibles_destino = casilla.get_pieza().get_posibles_casillas_destino(casilla, self._casillas)
        self.pintar_casillas()

    def pintar_casillas(self):
        for casilla in self._casillas_posibles_destino:
            casilla.get_label()["background"] = "green"

    def cancelar_seleccion(self):
        self.despintar_casillas()
        self._casillas_posibles_destino = []
        self._casilla_seleccionada = None

    def despintar_casillas(self):
        for casilla in self._casillas_posibles_destino:
            casilla.get_label()["background"] = casilla.get_color()

    def mover(self, casilla):
        casilla.get_label()["image"] = self._casilla_seleccionada.get_pieza().get_image()
        casilla.set_pieza(self._casilla_seleccionada.get_pieza())
        if isinstance(self._casilla_seleccionada.get_pieza(), Peon.Peon):
            self._casilla_seleccionada.get_pieza().set_primera_jugada(False)
        self._casilla_seleccionada.get_label()["image"] = self._images_tk['vacia']
        self._casilla_seleccionada.set_pieza(None)