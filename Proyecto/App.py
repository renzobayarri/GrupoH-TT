import time
from _thread import *

from Juego import Juego
from Jugador import Jugador
import tkinter as tk
import Cliente


def click_nombre():
    jugador.set_nombre(input_nombre.get())
    ventana_inicial.destroy()


def click_online():
    ventana_modo.destroy()


def crear_partida():
    ventana_online.destroy()
    start_new_thread(iniciar_servidor, ())
    start_new_thread(iniciar_primer_cliente, (jugador, juego))

def crear_cliente():
    ventana_online.destroy()
    start_new_thread(iniciar_primer_cliente, (jugador, juego))


def iniciar_servidor():
    import Server

def iniciar_primer_cliente(jugador, juego):
    Cliente.main(jugador, juego)


juego = Juego()
jugador = Jugador()
ventana_inicial = tk.Tk()
tk.Label(ventana_inicial, text="Nombre").pack()
input_nombre = tk.Entry(ventana_inicial, takefocus=True)
input_nombre.pack()
tk.Button(ventana_inicial, text="Aceptar", command=click_nombre).pack()
ventana_inicial.mainloop()

ventana_modo = tk.Tk()
tk.Button(ventana_modo, text="Jugador 1 VS CPU").pack()
tk.Button(ventana_modo, text="Jugador 1 VS Jugador 2").pack()
tk.Button(ventana_modo, text="Jugar Online", command=click_online).pack()
ventana_modo.mainloop()

ventana_online = tk.Tk()
tk.Button(ventana_online, text="Crear partida", command=crear_partida).pack()
tk.Button(ventana_online, text="Unirse", command=crear_cliente).pack()
ventana_online.mainloop()

while jugador.get_es_blanco() is None:
    time.sleep(1)

juego.set_tablero(jugador.get_es_blanco())
juego.get_tablero().crear_piezas_iniciales()
juego.get_tablero().dibujar(juego,jugador)
