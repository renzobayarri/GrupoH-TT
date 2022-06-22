import socket
import tkinter
from _thread import *
import pickle
import Cliente
import subprocess


class Server:

    def __init__(self, juego, jugador):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        i = 0
        while True:
            response = subprocess.run(args="ifconfig wlp" + str(i) + "s0 | grep 'inet ' | cut -d: -f2 | awk '{print $2}'",
                                  capture_output=True,
                                  shell=True
                                  )
            if response.stdout.decode("utf-8") == "":
                i += 1
                if i == 20:
                    encontrado = False
                    for j in range(20):
                        for k in range(20):
                            response = subprocess.run(
                                args="ifconfig enp" + str(j) + "s" + str(k) +" | grep 'inet ' | cut -d: -f2 | awk '{print $2}'",
                                capture_output=True,
                                shell=True
                                )
                            if response.stdout.decode("utf-8") != "":
                                self.server = response.stdout.decode("utf-8").replace("\n", "")
                                encontrado = True
                                break
                        if not encontrado:
                            exit()
            else:
                self.server = response.stdout.decode("utf-8").replace("\n", "")
                break
        self.port = 5555
        self.juego = juego
        self.jugador = jugador

        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            str(e)

        self.s.listen(2)
        print("Waiting for a connection, Server Started")

        self.info_juego = {
            "turno-blancas": True,
            "piezas-disponibles": ["B", "N"],
            "jugadores": [],
            "cambios": [],
            "pieza-promocion": None
        }

        start_new_thread(Cliente.main, (jugador, juego, self.server))
        self.escuchar()

    def aceptar(self):
        self.ip.destroy()

    def threaded_client(self, conn):

        conn.send(pickle.dumps(self.info_juego))
        reply = ""

        while True:
            try:
                datos_recibidos = pickle.loads(conn.recv(2048))
                if datos_recibidos != "Nada":
                    self.info_juego["turno-blancas"] = datos_recibidos["turno-blancas"]
                    self.info_juego["piezas-disponibles"] = datos_recibidos["piezas-disponibles"]
                    self.info_juego["jugadores"] = datos_recibidos["jugadores"]
                    self.info_juego["cambios"] = datos_recibidos["cambios"]
                    self.info_juego["pieza-promocion"] = datos_recibidos["pieza-promocion"]
                    if not datos_recibidos:
                        print("Disconnected")
                        break

                reply = self.info_juego
                conn.sendall(pickle.dumps(reply))

            except:
                break

        print("Lost connection")
        conn.close()

    def escuchar(self):
        i = 0
        while True:
            conn, addr = self.s.accept()
            i += 1
            print("Connected to:", addr)
            start_new_thread(self.threaded_client, (conn,))
            if i == 1:
                self.ip = tkinter.Tk()
                tkinter.Label(self.ip, text="Comparte esta IP con el otro jugador para poder conectarse").pack()
                tkinter.Label(self.ip, text=self.server).pack()
                tkinter.Button(self.ip, text="Aceptar", command=self.aceptar).pack()
                self.ip.mainloop()

