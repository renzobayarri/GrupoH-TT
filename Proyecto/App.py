from Juego import Juego
from Jugador import Jugador
from Intefaz import Interfaz

def continuar_juego():
    tiempo_maximo = 100000000
    if juego.get_modo() in ["entrenamiento", "vsCPU", "vsJug2"]:
        otro_jugador = Jugador()
        otro_jugador.set_nombre("Jugador 2")
        otro_jugador.set_es_blanco(not jugador.get_es_blanco())
        if otro_jugador.get_es_blanco():
            juego.set_jugador_blanco(otro_jugador)
        else:
            juego.set_jugador_negro(otro_jugador)

    i = 0
    while jugador.get_es_blanco() == None:
        if i == 0:
            pass
            # print("Elegir color")
        if i == tiempo_maximo:
            print("Hubo algún problema. Intente nuevamente")
            exit()
        i += 1

    i = 0
    while juego.get_jugador_blanco() == None:
        if i == 0:
            print("Esperando al jugador blanco")
        elif i == tiempo_maximo:
            print("Hubo algún problema. Intente nuevamente")
            exit()
        i += 1

    i = 0
    while juego.get_jugador_negro() == None:
        if i == 0:
            print("Esperando al jugador negro")
        elif i == tiempo_maximo:
            print("Tiempo de espera máximo excedido. Intente nuevamente")
            exit()
        i += 1

    i = 0
    while juego.get_jugador_blanco().get_nombre() == "":
        if i == 0:
            print("Esperando al jugador blanco")
        elif i == tiempo_maximo:
            print("Tiempo de espera máximo excedido. Intente nuevamente")
            exit()
        i += 1

    i = 0
    while juego.get_jugador_negro().get_nombre() == "":
        if i == 0:
            print("Esperando al jugador negro")
        elif i == tiempo_maximo:
            print("Tiempo de espera máximo excedido. Intente nuevamente")
            exit()
        i += 1

    print("Todo listo para jugar!")

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

