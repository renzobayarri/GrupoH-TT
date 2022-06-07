from Piezas import *
from Casilla import Casilla
import tkinter as tk
from tkinter import ttk

class Tablero:

    def __init__(self, vista_blanca):
        self._casillas = []
        self._casilla_seleccionada = None
        self._casillas_posibles_destino = []
        self._vista_blanca = vista_blanca
        self._coronar_peon = "caballo"

        for fila in range(8):
            filas = []
            for columna in range(8):
                color = "sienna4" if (fila + columna) % 2 == 1 else "white"
                casilla = Casilla(fila, columna, color)
                filas.append(casilla)
            self._casillas.append(filas)

    def get_casillas(self):
        return self._casillas

    def crear_piezas_iniciales(self, juego):

        for fila in range(8):
            if fila in (2, 5):
                pass

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

                if self._casillas[fila][columna].get_pieza() is not None:
                    juego.get_piezas_restantes().append(self._casillas[fila][columna].get_pieza())


    def cargar_imagenes(self, lado):

        reductor = int(150 / lado) if lado <= 75 else 2

        self._images_tk = {
            "vacia": tk.PhotoImage(width=lado, height=lado),
            "torre_blanca": tk.PhotoImage(file="./assets/wr.png").subsample(reductor, reductor),
            "torre_negra": tk.PhotoImage(file="./assets/br.png").subsample(reductor, reductor),
            "caballo_blanco": tk.PhotoImage(file="./assets/wn.png").subsample(reductor, reductor),
            "caballo_negro": tk.PhotoImage(file="./assets/bn.png").subsample(reductor, reductor),
            "alfil_blanco": tk.PhotoImage(file="./assets/wb.png").subsample(reductor, reductor),
            "alfil_negro": tk.PhotoImage(file="./assets/bb.png").subsample(reductor, reductor),
            "reina_blanca": tk.PhotoImage(file="./assets/wq.png").subsample(reductor, reductor),
            "reina_negra": tk.PhotoImage(file="./assets/bq.png").subsample(reductor, reductor),
            "rey_blanco": tk.PhotoImage(file="./assets/wk.png").subsample(reductor, reductor),
            "rey_negro": tk.PhotoImage(file="./assets/bk.png").subsample(reductor, reductor),
            "peon_blanco": tk.PhotoImage(file="./assets/wp.png").subsample(reductor, reductor),
            "peon_negro": tk.PhotoImage(file="./assets/bp.png").subsample(reductor, reductor),
        }

    def get_images_tk(self):
        return self._images_tk;

    def asignar_labels_imagenes(self, root, juego, jugador):
        for fila in self._casillas:
            for casilla in fila:
                casilla.set_label(tk.Label(root, background=casilla.get_color(), borderwidth=1, relief="solid"))
                if casilla.get_pieza() is None:
                    casilla.get_label()["image"] = self._images_tk['vacia']
                    casilla.get_label().bind(
                        "<Button>",
                        lambda event, casilla=casilla, juego=juego, jugador=jugador: self.click(casilla=casilla,
                                                                                                juego=juego,
                                                                                                jugador=jugador))
                else:
                    casilla.get_pieza().set_image(self._images_tk[casilla.get_pieza().get_nombre()])
                    casilla.get_label()["image"] = casilla.get_pieza().get_image()
                    casilla.get_label().bind(
                        "<Button>",
                        lambda event, casilla=casilla, juego=juego, jugador=jugador: self.click(casilla=casilla,
                                                                                                juego=juego,
                                                                                                jugador=jugador))
                if self._vista_blanca:
                    casilla.get_label().grid(column=casilla.get_columna(), row=casilla.get_fila())
                else:
                    casilla.get_label().grid(column=7 - casilla.get_columna(), row=7 - casilla.get_fila())

    def dibujar(self, juego, jugador):
        root = tk.Tk()
        Casilla.calcular_tamanio_lado(root)

        for i in range(8):
            root.columnconfigure(i)
            root.rowconfigure(i)

        self.cargar_imagenes(Casilla.lado)
        self.asignar_labels_imagenes(root, juego, jugador)

        root.mainloop()

    def click(self, casilla, juego, jugador):

        if juego.get_modo() in ["online", "vsCPU"]:
            if juego.get_turno_blanco() != jugador.get_es_blanco():
                return

        if juego.get_modo() != "entrenamiento":
            if casilla.get_pieza() is not None:
                if casilla.get_pieza().get_is_white() != juego.get_turno_blanco():
                    if casilla not in self._casillas_posibles_destino:
                        self.cancelar_seleccion()
                        return

        if self._casilla_seleccionada:
            if casilla in self._casillas_posibles_destino:
                self.mover(casilla, juego)
                self.cancelar_seleccion()
            else:
                self.cancelar_seleccion()
                if casilla.get_pieza() is not None:
                    self.seleccionar_casilla(casilla)
        else:
            if casilla.get_pieza() is not None:
                self.seleccionar_casilla(casilla)

    def seleccionar_casilla(self, casilla):
        self._casilla_seleccionada = casilla
        self._casillas_posibles_destino = casilla.get_pieza().get_posibles_casillas_destino(casilla, self._casillas)
        self.pintar_casillas()

    def pintar_casillas(self):
        for casilla in self._casillas_posibles_destino:
            if casilla.get_pieza() is not None:
                casilla.get_label()["background"] = "coral1"
            else:
                casilla.get_label()["background"] = "khaki"

    def cancelar_seleccion(self):
        self.despintar_casillas()
        self._casillas_posibles_destino = []
        self._casilla_seleccionada = None

    def despintar_casillas(self):
        for casilla in self._casillas_posibles_destino:
            casilla.get_label()["background"] = casilla.get_color()

    def mover(self, casilla, juego):

        cambio = [
            [self._casilla_seleccionada.get_fila(), self._casilla_seleccionada.get_columna()],
            [casilla.get_fila(), casilla.get_columna()]
        ]
        juego.set_cambio(cambio)

        if casilla.get_pieza() is not None:
            juego.get_piezas_eliminadas().append(casilla.get_pieza())
            juego.get_piezas_restantes().remove(casilla.get_pieza())


        # Setea la nueva casilla
        casilla.get_label()["image"] = self._casilla_seleccionada.get_pieza().get_image()
        casilla.set_pieza(self._casilla_seleccionada.get_pieza())

        if isinstance(self._casilla_seleccionada.get_pieza(), Peon.Peon):
            self._casilla_seleccionada.get_pieza().set_primera_jugada(False)

        # Vacía la casilla anterior
        self._casilla_seleccionada.get_label()["image"] = self._images_tk['vacia']
        self._casilla_seleccionada.set_pieza(None)


        juego.set_turno_blanco(not juego.get_turno_blanco())

    def validar_tablas_insuficiencia(self, juego):
        lista = juego.get_piezas_restantes()

        if len(lista) == 2:
            if isinstance(lista[0], Rey.Rey) and isinstance(lista[1], Rey.Rey):
                return True
        elif len(lista) == 3:
            if isinstance(lista[0], Caballo.Caballo) or isinstance(lista[1], Caballo.Caballo) or isinstance(lista[2], Caballo.Caballo) or \
            isinstance(lista[0], Alfil.Alfil) or isinstance(lista[1], Alfil.Alfil) or isinstance(lista[2], Alfil.Alfil):
                return True
        elif len(lista) == 4:

            alfil_blanco = False
            alfil_negro = False
            for pieza in juego.get_piezas_restantes():
                if isinstance(pieza, Alfil.Alfil):
                    if pieza.get_is_white():
                        alfil_blanco = True
                    else:
                        alfil_negro = True

            return alfil_blanco and alfil_negro

            caballo_blanco = 0
            caballo_negro = 0

            for pieza in juego.get_piezas_restantes():
                if isinstance(pieza, Caballo.Caballo):
                    if pieza.get_is_white():
                        caballo_blanco = caballo_blanco + 1
                    else:
                        caballo_negro = caballo_negro + 1
            return caballo_negro == 2 or caballo_blanco == 2

    def coronar(self, casilla):
        fila = casilla.get_fila()
        if fila == 0 or fila == 7:
            if casilla.get_pieza().get_nombre() == "peon_blanco" or casilla.get_pieza().get_nombre() == "peon_negro":
                ventana = tk.Tk()
                ventana.geometry("200x150")
                ventana.title("Coronar peon")
                ventana.rowconfigure(0, weight= 1)
                ventana.rowconfigure(1, weight=1)
                ventana.rowconfigure(2, weight=1)
                ventana.rowconfigure(3, weight=1)
                ventana.columnconfigure(0, weight=1)
                #ventana.iconbitmap(file="./assets/bb.png")
                reina = ttk.Button(ventana, text="Reina", command=self.coronar_tipo_reina)
                torre = ttk.Button(ventana, text="Torre", command=self.coronar_tipo_torre)
                alfil = ttk.Button(ventana, text="Alfil", command=self.coronar_tipo_alfil)
                caballo = ttk.Button(ventana, text="Caballo", command=self.coronar_tipo_caballo)
                reina.grid(row=0, column=0, sticky="NSWE")
                torre.grid(row=1, column=0, sticky="NSWE")
                alfil.grid(row=2, column=0, sticky="NSWE")
                caballo.grid(row=3, column=0, sticky="NSWE")
                ventana.mainloop()
            casilla.set_pieza(self.cambiar_peon(casilla, self._coronar_peon))
            return casilla

    def coronar_tipo_reina(self):
        self._coronar_peon = "reina"
        print(self._coronar_peon)

    def coronar_tipo_torre(self):
        self._coronar_peon = "torre"
        print(self._coronar_peon)

    def coronar_tipo_alfil(self):
        self._coronar_peon = "alfil"
        print(self._coronar_peon)

    def coronar_tipo_caballo(self):
        self._coronar_peon = "caballo"
        print(self._coronar_peon)

    def Coronar_reina(self, casilla):
        if (casilla.get_pieza().get_is_white()):
            casilla.set_pieza(Torre.Torre(True))
            casilla.get_pieza().set_image(self._images_tk["torre_blanca"])
        else:
            casilla.set_pieza(Torre.Torre(False))
            casilla.get_pieza().set_image(self._images_tk["torre_negra"])

    def Coronar_torre(self, casilla):
        if(casilla.get_pieza().get_is_white()):
            casilla.set_pieza(Torre.Torre(True))
            casilla.get_pieza().set_image(self._images_tk["torre_blanca"])
        else:
            casilla.set_pieza(Torre.Torre(False))
            casilla.get_pieza().set_image(self._images_tk["torre_negra"])

    def Coronar_alfil(self, casilla):
        if(casilla.get_pieza().get_is_white()):
            casilla.set_pieza(Alfil.Alfil(True))
            casilla.get_pieza().set_image(self._images_tk["alfil_blanco"])
        else:
            casilla.set_pieza(Alfil.Alfil(False))
            casilla.get_pieza().set_image(self._images_tk["alfil_negro"])

    def Coronar_caballo(self, casilla):
        if(casilla.get_pieza().get_is_white()):
            casilla.set_pieza(Caballo.Caballo(True))
            casilla.get_pieza().set_image(self._images_tk["caballo_blanco"])
        else:
            casilla.set_pieza(Caballo.Caballo(False))
            casilla.get_pieza().set_image(self._images_tk["caballo_negro"])

    def cambiar_peon(self, casilla, text):
        if(casilla.get_pieza().get_is_white()):
            if(text == "reina"):
                casilla.set_pieza(Reina.Reina(True))
                casilla.get_pieza().set_image(self._images_tk["reina_blanca"])
            if (text == "torre"):
                casilla.set_pieza(Torre.Torre(True))
                casilla.get_pieza().set_image(self._images_tk["torre_blanca"])
            if (text == "alfil"):
                casilla.set_pieza(Alfil.Alfil(True))
                casilla.get_pieza().set_image(self._images_tk["alfil_blanco"])
                print("entro")
            if (text == "caballo"):
                casilla.set_pieza(Caballo.Caballo(True))
                casilla.get_pieza().set_image(self._images_tk["caballo_blanco"])
        else:
            if (text == "reina"):
                casilla.set_pieza(Reina.Reina(False))
                casilla.get_pieza().set_image(self._images_tk["reina_negra"])
            if (text == "torre"):
                casilla.set_pieza(Torre.Torre(False))
                casilla.get_pieza().set_image(self._images_tk["torre_negra"])
            if (text == "alfil"):
                casilla.set_pieza(Alfil.Alfil(False))
                casilla.get_pieza().set_image(self._images_tk["alfil_negro"])
            if (text == "caballo"):
                casilla.set_pieza(Caballo.Caballo(False))
                casilla.get_pieza().set_image(self._images_tk["caballo_negro"])
        return casilla




