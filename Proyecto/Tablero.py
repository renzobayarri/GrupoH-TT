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
        self._info_enroque = []
        self._info_peon_al_paso = []
        self._pieza_promocion = None;

        for fila in range(8):
            filas = []
            for columna in range(8):
                color = "sienna4" if (fila + columna) % 2 == 1 else "white"
                casilla = Casilla(fila, columna, color)
                filas.append(casilla)
            self._casillas.append(filas)

    def get_casillas(self):
        return self._casillas

    def set_pieza_promocion(self, pieza):
        self._pieza_promocion = pieza

    def get_pieza_promocion(self):
        return self._pieza_promocion

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

        juego.get_jugador_blanco().set_casilla_rey(self._casillas[7][4])
        juego.get_jugador_negro().set_casilla_rey(self._casillas[0][4])

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
                if casilla.get_pieza().get_es_blanca() != juego.get_turno_blanco():
                    if casilla not in self._casillas_posibles_destino:
                        self.cancelar_seleccion()
                        return

        if self._casilla_seleccionada:
            if casilla in self._casillas_posibles_destino:
                self.mover(self._casilla_seleccionada, casilla, juego)
                if isinstance(casilla.get_pieza(), Peon.Peon) and (casilla.get_fila() == 0 or casilla.get_fila() == 7):
                    self.coronar(casilla, juego)
                self.verificar_jaque(juego)
                if self.es_tabla(juego):
                    print("tablas")
                juego.set_turno_blanco(not juego.get_turno_blanco())
                self.cancelar_seleccion()
            else:
                if self._info_enroque:
                    hacer_enroque = False
                    for enroque in self._info_enroque:
                        if casilla == enroque["origen-torre"]:
                            self.mover(self._casilla_seleccionada, enroque["destino-rey"], juego)
                            self.mover(enroque["origen-torre"], enroque["destino-torre"], juego)
                            self.cancelar_seleccion()
                            juego.set_turno_blanco(not juego.get_turno_blanco())
                            hacer_enroque = True
                            self.verificar_jaque(juego)
                            if self.es_tabla(juego):
                                print("tablas")
                    if not hacer_enroque:
                        self.cancelar_seleccion()
                        if casilla.get_pieza() is not None:
                            self.seleccionar_casilla(casilla, juego)
                else:
                    if self._info_peon_al_paso:
                        hacer_movimiento = False
                        for peon_al_paso in self._info_peon_al_paso:
                            if casilla == peon_al_paso["destino-peon"]:
                                self.mover(self._casilla_seleccionada, peon_al_paso["peon-comible"], juego)
                                self.mover(peon_al_paso["peon-comible"], peon_al_paso["destino-peon"], juego)
                                self.cancelar_seleccion()
                                juego.set_turno_blanco(not juego.get_turno_blanco())
                                hacer_movimiento = True
                                self.verificar_jaque(juego)
                                if self.es_tabla(juego):
                                    print("tablas")
                        if not hacer_movimiento:
                            self.cancelar_seleccion()
                            if casilla.get_pieza() is not None:
                                self.seleccionar_casilla(casilla, juego)
                    else:
                        self.cancelar_seleccion()
                        if casilla.get_pieza() is not None:
                            self.seleccionar_casilla(casilla, juego)
        else:
            if casilla.get_pieza() is not None:
                self.seleccionar_casilla(casilla, juego)

    def seleccionar_casilla(self, casilla, juego):
        self._casilla_seleccionada = casilla
        self._casillas_posibles_destino = casilla.get_pieza().get_posibles_casillas_destino(casilla, juego)
        if isinstance(casilla.get_pieza(), Rey.Rey):
            self._info_enroque = casilla.get_pieza().get_datos_enroque(casilla, juego)
        if isinstance(casilla.get_pieza(), Peon.Peon):
            self._info_peon_al_paso = casilla.get_pieza().get_info_al_paso(casilla, juego)
        self.pintar_casillas()

    def pintar_casillas(self):
        for casilla in self._casillas_posibles_destino:
            if casilla.get_pieza() is not None:
                casilla.get_label()["background"] = "coral1"
            else:
                casilla.get_label()["background"] = "khaki"
        if self._info_enroque:
            for enroque in self._info_enroque:
                enroque["origen-torre"].get_label()["background"] = "purple"
        if self._info_peon_al_paso:
            for peon_al_paso in self._info_peon_al_paso:
                peon_al_paso["destino-peon"].get_label()["background"] = "purple"

    def cancelar_seleccion(self):
        self.despintar_casillas()
        self._casillas_posibles_destino = []
        self._info_enroque = []
        self._info_peon_al_paso = []
        self._casilla_seleccionada = None

    def despintar_casillas(self):
        for casilla in self._casillas_posibles_destino:
            casilla.get_label()["background"] = casilla.get_color()
        if self._info_enroque:
            for enroque in self._info_enroque:
                enroque["origen-torre"].get_label()["background"] = enroque["origen-torre"].get_color()
        if self._info_peon_al_paso:
            for peon_al_paso in self._info_peon_al_paso:
                peon_al_paso["destino-peon"].get_label()["background"] = peon_al_paso["destino-peon"].get_color()

    def mover(self, origen, destino, juego):


        cambio = [
                [origen.get_fila(), origen.get_columna()],
                [destino.get_fila(), destino.get_columna()]
            ]
        juego.get_cambio().append(cambio)

        if destino.get_pieza() is not None:
            juego.get_piezas_eliminadas().append(destino.get_pieza())
            juego.get_piezas_restantes().remove(destino.get_pieza())

        # Setea la nueva casilla
        destino.get_label()["image"] = origen.get_pieza().get_image()
        destino.set_pieza(origen.get_pieza())

        origen.get_pieza().aumentar_cantidad_movimientos()
        juego.set_ultima_pieza_movida(origen.get_pieza())

        if isinstance(origen.get_pieza(), Rey.Rey):
            origen.get_label()["background"] = origen.get_color()
            if origen.get_pieza().get_es_blanca():
                juego.get_jugador_blanco().set_casilla_rey(destino)
            else:
                juego.get_jugador_negro().set_casilla_rey(destino)
        # Vacía la casilla anterior
        origen.get_label()["image"] = self._images_tk['vacia']
        origen.set_pieza(None)

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
                    if pieza.get_es_blanca():
                        alfil_blanco = True
                    else:
                        alfil_negro = True

            caballo_blanco = 0
            caballo_negro = 0

            for pieza in juego.get_piezas_restantes():
                if isinstance(pieza, Caballo.Caballo):
                    if pieza.get_es_blanca():
                        caballo_blanco = caballo_blanco + 1
                    else:
                        caballo_negro = caballo_negro + 1
            return (alfil_blanco and alfil_negro) or (caballo_negro == 2 or caballo_blanco == 2)

    def es_tablas_por_ahogamiento(self, juego):

        return self.no_hay_movimientos(juego.get_turno_blanco(), juego)

    def verificar_jaque(self, juego):

        jugadores = [juego.get_jugador_blanco(), juego.get_jugador_negro()]

        for jugador in jugadores:
            if jugador.get_casilla_rey().get_pieza().esta_en_jaque(jugador.get_casilla_rey(), self._casillas):
                self.pintar_jaque(jugador.get_casilla_rey())
                if self.no_hay_movimientos(jugador.get_es_blanco(), juego):
                    jugador.get_casilla_rey().get_label()["background"] = "red"
            else:
                self.despintar_jaque(jugador.get_casilla_rey())

    def pintar_jaque(self, casilla):
        casilla.get_label()["background"] = "coral1"

    def despintar_jaque(self, casilla):
        casilla.get_label()["background"] = casilla.get_color()

    def no_hay_movimientos(self, blancas, juego):

        casillas = juego.get_tablero().get_casillas()
        for fila in range(8):
            for columna in range(8):
                if casillas[fila][columna].get_pieza() is not None:
                    if casillas[fila][columna].get_pieza().get_es_blanca() == blancas:
                        posiblidades = casillas[fila][columna].get_pieza().get_posibles_casillas_destino(
                            casillas[fila][columna], juego)
                        if posiblidades:
                            return False
        return True

    def coronar(self, casilla, juego):
        global img
        fila = casilla.get_fila()
        if fila == 0 or fila == 7:
            if casilla.get_pieza().get_nombre() == "peon_blanco" or casilla.get_pieza().get_nombre() == "peon_negro":
                ventana = tk.Toplevel()
                ventana.geometry("150x600")
                ventana.title("Coronar peon")
                ventana.rowconfigure(0, weight= 1)
                ventana.rowconfigure(1, weight=1)
                ventana.rowconfigure(2, weight=1)
                ventana.rowconfigure(3, weight=1)
                ventana.columnconfigure(0, weight=1)
                if casilla.get_pieza().get_es_blanca():
                    img1 = tk.PhotoImage(file="./assets/wk.png")
                    img2 = tk.PhotoImage(file="./assets/wr.png")
                    img3 = tk.PhotoImage(file="./assets/wb.png")
                    img4 = tk.PhotoImage(file="./assets/wn.png")
                else:
                    img1 = tk.PhotoImage(file="./assets/bk.png")
                    img2 = tk.PhotoImage(file="./assets/br.png")
                    img3 = tk.PhotoImage(file="./assets/bb.png")
                    img4 = tk.PhotoImage(file="./assets/bn.png")
                #ventana.iconbitmap(file="./assets/bb.png")

                reina = tk.Button(
                    ventana,
                    #text="Reina",
                    image= img1,
                    command=lambda ventana=ventana,
                                   pieza=Reina.Reina,
                                   blanca=casilla.get_pieza().get_es_blanca(),
                                   casilla=casilla,
                                   juego=juego: self.cambiar_pieza(clase=pieza, blanca=blanca, casilla=casilla,
                                                                   ventana=ventana, juego=juego))
                torre = tk.Button(
                    ventana,
                    text="Torre",
                    image=img2,
                    command=lambda ventana=ventana,
                                   pieza=Torre.Torre,
                                   blanca=casilla.get_pieza().get_es_blanca(),
                                   casilla=casilla,
                                   juego=juego: self.cambiar_pieza(clase=pieza, blanca=blanca, casilla=casilla,
                                                                   ventana=ventana, juego=juego))
                alfil = tk.Button(
                    ventana, text="Alfil",
                    image=img3,
                    command=lambda ventana=ventana,
                                   pieza=Alfil.Alfil,
                                   blanca=casilla.get_pieza().get_es_blanca(),
                                   casilla=casilla,
                                   juego=juego: self.cambiar_pieza(clase=pieza, blanca=blanca, casilla=casilla,
                                                                   ventana=ventana, juego=juego))
                caballo = tk.Button(
                    ventana,
                    text="Caballo",
                    image=img4,
                    command=lambda ventana=ventana,
                                   pieza=Caballo.Caballo,
                                   blanca=casilla.get_pieza().get_es_blanca(),
                                   casilla=casilla,
                                   juego=juego: self.cambiar_pieza(clase=pieza, blanca=blanca, casilla=casilla,
                                                                   ventana=ventana, juego=juego))
                #reina.grid(row=0, column=0, sticky="NSWE")
                #torre.grid(row=1, column=0, sticky="NSWE")
                #alfil.grid(row=2, column=0, sticky="NSWE")
                #caballo.grid(row=3, column=0, sticky="NSWE")
                reina.pack()
                torre.pack()
                alfil.pack()
                caballo.pack()
                img.pack()
                ventana.mainloop()


    def cambiar_pieza(self, clase, blanca, casilla, ventana, juego):
        juego.get_piezas_restantes().remove(casilla.get_pieza())
        nueva_pieza = clase(blanca)
        nueva_pieza.set_image(self._images_tk[nueva_pieza.get_nombre()])
        casilla.set_pieza(nueva_pieza)
        casilla.get_label()["image"] = nueva_pieza.get_image()
        ventana.destroy()
        juego.get_piezas_restantes().append(nueva_pieza)
        self.set_pieza_promocion(clase)
        self.verificar_jaque(juego)
        if self.es_tabla(juego):
            print("tablas")
        juego.set_turno_blanco(not juego.get_turno_blanco())
        self.cancelar_seleccion()

    def es_tabla(self, juego):
        return self.es_tablas_por_ahogamiento(juego) or self.validar_tablas_insuficiencia(juego)