from Network import Network
from Jugador import Jugador
import tkinter as tk
from Piezas import *


def main(jugador, juego):
    run = True
    n = Network(jugador.get_nombre())
    otroJugador = Jugador()

    while run:
        n.set_info_juego(n.send(n.get_info_juego()))

        if len(n.get_info_juego()["piezas-disponibles"]) == 2:
            elegir_color(jugador)
            if jugador.get_es_blanco():
                n.get_info_juego()["piezas-disponibles"].remove("B")
                juego.set_jugador_blanco(jugador)
                juego.set_jugador_negro(otroJugador)
            else:
                n.get_info_juego()["piezas-disponibles"].remove("N")
                juego.set_jugador_negro(jugador)
                juego.set_jugador_blanco(otroJugador)

            otroJugador.set_es_blanco(not jugador.get_es_blanco())

            n.send(n.get_info_juego())
            recibido = n.get_info_juego()
            while recibido["piezas-disponibles"] != [] or len(recibido["jugadores"]) != 2:
                recibido = n.recibir()

            n.set_info_juego(recibido)
            otroJugador.set_nombre(n.get_info_juego()["jugadores"][1])

        elif jugador.get_es_blanco() is None and len(n.get_info_juego()["piezas-disponibles"]) == 1:

            otroJugador.set_nombre(n.get_info_juego()["jugadores"][0])

            if n.get_info_juego()["piezas-disponibles"][0] == "B":
                jugador.set_es_blanco(True)
                juego.set_jugador_blanco(jugador)
                otroJugador.set_es_blanco(False)
                juego.set_jugador_negro(otroJugador)
            else:
                jugador.set_es_blanco(False)
                juego.set_jugador_negro(jugador)
                otroJugador.set_es_blanco(True)
                juego.set_jugador_blanco(otroJugador)
            n.get_info_juego()["piezas-disponibles"] = []

            n.send(n.get_info_juego())

        if n.get_info_juego()["turno-blancas"] != jugador.get_es_blanco():
            recibido = n.get_info_juego()
            while recibido["turno-blancas"] != jugador.get_es_blanco():
                recibido = n.recibir()

            n.set_info_juego(recibido)
            if n.get_info_juego()["cambios"] != []:
                juego.set_cambio(n.get_info_juego()["cambios"])
                registrar_cambios(juego)
                n.get_info_juego()["cambios"] = []
                juego.set_cambio([])
            juego.set_turno_blanco(jugador.get_es_blanco())

        if n.get_info_juego()["turno-blancas"] == jugador.get_es_blanco():

            while juego.get_turno_blanco() == jugador.get_es_blanco():
                pass

            n.get_info_juego()["turno-blancas"] = juego.get_turno_blanco()
            n.get_info_juego()["cambios"] = juego.get_cambio()
            n.send(n.get_info_juego())


def elegir_color(jugador):
    ventana_color = tk.Tk()
    btn_blancas = tk.Button(
        ventana_color, text="Blancas",
            command=lambda blancas =True, jugador=jugador, ventana=ventana_color: click_color(blancas, jugador, ventana))
    btn_negras = tk.Button(
        ventana_color, text="Negras",
        command=lambda blancas=False, jugador=jugador, ventana=ventana_color: click_color(blancas, jugador, ventana))
    btn_blancas.pack()
    btn_negras.pack()
    ventana_color.mainloop()


def click_color(blancas, jugador, ventana):
    ventana.destroy()
    jugador.set_es_blanco(blancas)

def registrar_cambios(juego):

    fila_columna_origen, fila_columna_destino = juego.get_cambio()
    casilla_origen = juego.get_tablero().get_casillas()[fila_columna_origen[0]][fila_columna_origen[1]]
    casilla_destino = juego.get_tablero().get_casillas()[fila_columna_destino[0]][fila_columna_destino[1]]

    casilla_destino.get_label()["image"] = casilla_origen.get_pieza().get_image()
    casilla_destino.set_pieza(casilla_origen.get_pieza())

    if isinstance(casilla_origen.get_pieza(), Peon.Peon):
        casilla_origen.get_pieza().set_primera_jugada(False)

    casilla_origen.get_label()["image"] = juego.get_tablero().get_images_tk()["vacia"]
    casilla_origen.set_pieza(None)

