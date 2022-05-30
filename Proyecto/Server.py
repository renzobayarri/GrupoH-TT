import socket
from _thread import *
import pickle

# casa
server = "192.168.0.107"
# oficina
# server = "172.22.37.65"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

info_juego = {
    "turno-blancas": True,
    "piezas-disponibles": ["B", "N"],
    "jugadores": [],
    "cambios": []
}

def threaded_client(conn):

    conn.send(pickle.dumps(info_juego))
    reply = ""

    while True:
        try:
            datos_recibidos = pickle.loads(conn.recv(2048))
            if datos_recibidos != "Nada":
                info_juego["turno-blancas"] = datos_recibidos["turno-blancas"]
                info_juego["piezas-disponibles"] = datos_recibidos["piezas-disponibles"]
                info_juego["jugadores"] = datos_recibidos["jugadores"]
                info_juego["cambios"] = datos_recibidos["cambios"]

                if not datos_recibidos:
                    print("Disconnected")
                    break

            reply = info_juego
            conn.sendall(pickle.dumps(reply))

        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))