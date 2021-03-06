from Piezas import *
from Casilla import Casilla
import tkinter as tk
import Ai
import pieces
import board


class Tablero:

    def __init__(self, vista_blanca):
        self._casillas = []
        self._casilla_seleccionada = None
        self._casillas_posibles_destino = []
        self._vista_blanca = vista_blanca
        self._info_enroque = []
        self._info_peon_al_paso = []
        self._pieza_promocion = None;
        self.board = board.Board.new()

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
        self._root = root
        root.title(juego.get_jugador_blanco().get_nombre() + " vs " + juego.get_jugador_negro().get_nombre())
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

        if not juego.get_terminado():
            if self._casilla_seleccionada:
                if casilla in self._casillas_posibles_destino:
                    self.mover(self._casilla_seleccionada, casilla, juego)
                    self.cancelar_seleccion()
                    if isinstance(casilla.get_pieza(), Peon.Peon) and (casilla.get_fila() == 0 or casilla.get_fila() == 7):
                        self.coronar(casilla, juego)
                    juego.set_turno_blanco(not juego.get_turno_blanco())
                    self.validar_jaques_y_tablas(juego, jugador)
                    if juego.get_modo() == "vsCPU":
                        ai_move = Ai.AI.get_ai_move(self.board, [])
                        self.mover(self._casillas[ai_move.yfrom][ai_move.xfrom], self._casillas[ai_move.yto][ai_move.xto], juego)
                        self.validar_jaques_y_tablas(juego, jugador)
                        juego.set_turno_blanco(not juego.get_turno_blanco())
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
                                self.validar_jaques_y_tablas(juego, jugador)
                                if juego.get_modo() == "vsCPU":
                                    ai_move = Ai.AI.get_ai_move(self.board, [])
                                    self.mover(self._casillas[ai_move.yfrom][ai_move.xfrom],
                                               self._casillas[ai_move.yto][ai_move.xto], juego)
                                    self.validar_jaques_y_tablas(juego, jugador)
                                    juego.set_turno_blanco(not juego.get_turno_blanco())

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
                                    self.validar_jaques_y_tablas(juego, jugador)
                                    if juego.get_modo() == "vsCPU":
                                        ai_move = Ai.AI.get_ai_move(self.board, [])
                                        self.mover(self._casillas[ai_move.yfrom][ai_move.xfrom],
                                                   self._casillas[ai_move.yto][ai_move.xto], juego)
                                        self.validar_jaques_y_tablas(juego, jugador)
                                        juego.set_turno_blanco(not juego.get_turno_blanco())
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

        move = Ai.Move(origen.get_columna(), origen.get_fila(), destino.get_columna(), destino.get_fila(), False)
        self.board.perform_move(move)

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
        # Vac??a la casilla anterior
        origen.get_label()["image"] = self._images_tk['vacia']
        origen.set_pieza(None)

    def coronar(self, casilla, juego):
        global img
        fila = casilla.get_fila()
        if fila == 0 or fila == 7:
            if casilla.get_pieza().get_nombre() == "peon_blanco" or casilla.get_pieza().get_nombre() == "peon_negro":
                ventana = tk.Toplevel()
                ventana.title("Coronar peon")
                ventana.rowconfigure(0, weight= 1)
                ventana.rowconfigure(1, weight=1)
                ventana.rowconfigure(2, weight=1)
                ventana.rowconfigure(3, weight=1)
                ventana.columnconfigure(0, weight=1)
                if casilla.get_pieza().get_es_blanca():
                    img1 = tk.PhotoImage(file="./assets/wq.png").subsample(2,2)
                    img2 = tk.PhotoImage(file="./assets/wr.png").subsample(2,2)
                    img3 = tk.PhotoImage(file="./assets/wb.png").subsample(2,2)
                    img4 = tk.PhotoImage(file="./assets/wn.png").subsample(2,2)
                else:
                    img1 = tk.PhotoImage(file="./assets/bq.png").subsample(2,2)
                    img2 = tk.PhotoImage(file="./assets/br.png").subsample(2,2)
                    img3 = tk.PhotoImage(file="./assets/bb.png").subsample(2,2)
                    img4 = tk.PhotoImage(file="./assets/bn.png").subsample(2,2)

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
                reina.pack()
                torre.pack()
                alfil.pack()
                caballo.pack()
                ventana.mainloop()


    def cambiar_pieza(self, clase, blanca, casilla, ventana, juego):
        if blanca:
            jugador = juego.get_jugador_blanco()
        else:
            jugador = juego.get_jugador_negro()
        juego.get_piezas_restantes().remove(casilla.get_pieza())
        nueva_pieza = clase(blanca)
        nueva_pieza.set_image(self._images_tk[nueva_pieza.get_nombre()])
        casilla.set_pieza(nueva_pieza)
        casilla.get_label()["image"] = nueva_pieza.get_image()
        ventana.destroy()
        juego.get_piezas_restantes().append(nueva_pieza)
        self.set_pieza_promocion(clase)
        juego.set_turno_blanco(not juego.get_turno_blanco())
        self.validar_jaques_y_tablas(juego, jugador)
        fila = casilla.get_fila()
        columna = casilla.get_columna()
        color = pieces.Piece.WHITE if blanca else pieces.Piece.BLACK
        if clase == Reina.Reina:
            self.board.chesspieces[columna][fila] = pieces.Queen(columna, fila, color)
        elif clase == Torre.Torre:
            self.board.chesspieces[columna][fila] = pieces.Rook(columna, fila, color)
        elif clase == Caballo.Caballo:
            self.board.chesspieces[columna][fila] = pieces.Knight(columna, fila, color)
        elif clase == Alfil.Alfil:
            self.board.chesspieces[columna][fila] = pieces.Bishop(columna, fila, color)
        if juego.get_modo() == "vsCPU":
            ai_move = Ai.AI.get_ai_move(self.board, [])
            self.mover(self._casillas[ai_move.yfrom][ai_move.xfrom],
                       self._casillas[ai_move.yto][ai_move.xto], juego)
            self.validar_jaques_y_tablas(juego, jugador)
            juego.set_turno_blanco(not juego.get_turno_blanco())
            self.validar_jaques_y_tablas(juego, jugador)


    def validar_jaques_y_tablas(self, juego, jugador, turno_sin_cambiar=False):
        if not self.es_jaque(juego, jugador):
            if self.es_tabla(juego, turno_sin_cambiar):
                self.finalizar_juego(juego, jugador)

    def es_jaque(self, juego, yo):

        jugadores = [juego.get_jugador_blanco(), juego.get_jugador_negro()]

        for jugador in jugadores:
            if jugador.get_casilla_rey().get_pieza().esta_en_jaque(jugador.get_casilla_rey(), self._casillas):
                if self.no_hay_movimientos(jugador.get_es_blanco(), juego):
                    jugador.get_casilla_rey().get_label()["background"] = "red"
                    self.finalizar_juego(juego, yo, jugador)
                else:
                    self.pintar_jaque(jugador.get_casilla_rey())
                return True
            self.despintar_jaque(jugador.get_casilla_rey())
        return False

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

    def es_tabla(self, juego, turno_sin_cambiar=False):
        return self.es_tablas_por_ahogamiento(juego, turno_sin_cambiar) or self.validar_tablas_insuficiencia(juego)

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

    def es_tablas_por_ahogamiento(self, juego, turno_sin_cambiar=False):

        if juego.get_modo() == "entrenamiento":
            return self.no_hay_movimientos(False, juego) or self.no_hay_movimientos(True, juego)
        if turno_sin_cambiar:
            return self.no_hay_movimientos(not juego.get_turno_blanco(), juego)
        return self.no_hay_movimientos(juego.get_turno_blanco(), juego)

    def finalizar_juego(self, juego, jugador, perdedor=None):
        ventana_finaliza = tk.Tk()
        ventana_finaliza.title("Resultado de la partida")
        juego.set_terminado(True)
        if not perdedor:
            lbl_resultado = tk.Label(ventana_finaliza, text="El juego finaliz?? en tablas").pack()
        else:
            if perdedor == jugador:
                lbl_resultado = tk.Label(ventana_finaliza, text="Perdiste " + jugador.get_nombre()).pack()
            else:
                lbl_resultado = tk.Label(ventana_finaliza,text="??Ganaste " + jugador.get_nombre() + "!").pack()
        btn_finalizar = tk.Button(ventana_finaliza, text="Finalizar", command=lambda ventana=ventana_finaliza: self.cerrar_ventana(ventana=ventana)).pack()
        ventana_finaliza.mainloop()


    def cerrar_ventana(self, ventana):
        ventana.destroy()
        self._root.destroy()
