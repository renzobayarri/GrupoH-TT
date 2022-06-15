from Juego import Juego
from Jugador import Jugador
from Intefaz import Interfaz

def continuar_juego():
    if juego.get_modo() in ["entrenamiento", "vsCPU", "vsJug2"]:
        otro_jugador = Jugador()
        otro_jugador.set_nombre("Jugador 2")
        otro_jugador.set_es_blanco(not jugador.get_es_blanco())
        if otro_jugador.get_es_blanco():
            juego.set_jugador_blanco(otro_jugador)
        else:
            juego.set_jugador_negro(otro_jugador)

    while jugador.get_es_blanco() == None:
        print("Todavía no he elegido color")

    while juego.get_jugador_blanco() == None:
        print("No hay jugador blanco")

    while juego.get_jugador_negro() == None:
        print("No hay jugador negro")

    while juego.get_jugador_blanco().get_nombre() == "":
        print("Todavía no hay jugador blanco")

    while juego.get_jugador_negro().get_nombre() == "":
        print("Todavía no hay jugador negro")

    print("Ya cumplí todos los requisitos")

    juego.set_tablero(jugador.get_es_blanco())
    juego.get_tablero().crear_piezas_iniciales(juego)
    juego.get_tablero().dibujar(juego, jugador)

while True:
    juego = Juego()
    jugador = Jugador()
    interfaz = Interfaz(juego, jugador, continuar_juego)
    interfaz.mostrar_ventana()
    del juego
    del jugador
    del interfaz

