from Network import Network
from Jugador import Jugador
from Piezas import Rey, Peon


def main(jugador, juego, server):
    run = True
    n = Network(jugador.get_nombre(), server)
    otroJugador = Jugador()

    while run:
        n.set_info_juego(n.send(n.get_info_juego()))

        # Hay un jugador que ya sabe su color
        if jugador.get_es_blanco() != None and len(n.get_info_juego()["piezas-disponibles"]) == 2:
            if jugador.get_es_blanco():
                n.get_info_juego()["piezas-disponibles"].remove("B")
                juego.set_jugador_negro(otroJugador)
            else:
                n.get_info_juego()["piezas-disponibles"].remove("N")
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
                juego.get_tablero().set_pieza_promocion(n.get_info_juego()["pieza-promocion"])
                registrar_cambios(juego)
                n.get_info_juego()["cambios"] = []
                n.get_info_juego()["pieza-promocion"] = None
                juego.get_tablero().set_pieza_promocion(None)
                juego.set_cambio([])
                juego.get_tablero().validar_jaques_y_tablas(juego, jugador, True)
                juego.set_turno_blanco(jugador.get_es_blanco())

        if n.get_info_juego()["turno-blancas"] == jugador.get_es_blanco():

            while juego.get_turno_blanco() == jugador.get_es_blanco():
                pass

            n.get_info_juego()["turno-blancas"] = juego.get_turno_blanco()
            n.get_info_juego()["cambios"] = juego.get_cambio()
            n.get_info_juego()["pieza-promocion"] = juego.get_tablero().get_pieza_promocion()
            n.send(n.get_info_juego())

def registrar_cambios(juego):

    for movimiento in juego.get_cambio():

        fila_columna_origen, fila_columna_destino = movimiento
        casilla_origen = juego.get_tablero().get_casillas()[fila_columna_origen[0]][fila_columna_origen[1]]
        casilla_destino = juego.get_tablero().get_casillas()[fila_columna_destino[0]][fila_columna_destino[1]]

        if casilla_destino.get_pieza() is not None:
            juego.get_piezas_restantes().remove(casilla_destino.get_pieza())

        casilla_destino.get_label()["image"] = casilla_origen.get_pieza().get_image()
        casilla_destino.set_pieza(casilla_origen.get_pieza())

        casilla_origen.get_pieza().aumentar_cantidad_movimientos()
        juego.set_ultima_pieza_movida(casilla_origen.get_pieza())

        if isinstance(casilla_origen.get_pieza(), Rey.Rey):
            casilla_origen.get_label()["background"] = casilla_origen.get_color()
            if casilla_origen.get_pieza().get_es_blanca():
                juego.get_jugador_blanco().set_casilla_rey(casilla_destino)
            else:
                juego.get_jugador_negro().set_casilla_rey(casilla_destino)

        casilla_origen.get_label()["image"] = juego.get_tablero().get_images_tk()["vacia"]
        casilla_origen.set_pieza(None)

        if isinstance(casilla_destino.get_pieza(), Peon.Peon):
            if casilla_destino.get_fila() == 0 or casilla_destino.get_fila() == 7:
                juego.get_piezas_restantes().remove(casilla_destino.get_pieza())
                nueva_pieza = juego.get_tablero().get_pieza_promocion()(casilla_destino.get_pieza().get_es_blanca())
                nueva_pieza.set_image(juego.get_tablero().get_images_tk()[nueva_pieza.get_nombre()])
                juego.get_piezas_restantes().append(nueva_pieza)
                casilla_destino.set_pieza(nueva_pieza)
                casilla_destino.get_label()["image"] = nueva_pieza.get_image()


