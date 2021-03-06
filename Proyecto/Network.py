import socket
import pickle


class Network:
    def __init__(self, nombre, server):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server = server
        self._port = 5555
        self._addr = (self._server, self._port)
        self._nombre = nombre
        self._info_juego = self.connect()
        self._info_juego["jugadores"].append(self._nombre)

    def connect(self):
        dato_recibido = None
        i = 0
        while dato_recibido == None:
            try:
                if i == 0:
                    print("Conectando con servidor... " + self._server)
                elif i == 300:
                    print("No se pudo conectar al servidor. Verifique la IP ingresada y su conexión a la red local")
                    exit()
                self._client.connect(self._addr)
                print("Conectado")
                dato_recibido = pickle.loads(self._client.recv(2048))
                return dato_recibido
            except:
                i += 1
                pass

    def send(self, data):
        try:
            self._client.send(pickle.dumps(data))
            return pickle.loads(self._client.recv(2048))
        except socket.error as e:
            print(e)

    def recibir(self):
        try:
            self._client.send(pickle.dumps("Nada"))
            return pickle.loads(self._client.recv(2048))
        except socket.error as e:
            print(e)

    def get_info_juego(self):
        return self._info_juego

    def set_info_juego(self, info_juego):
        self._info_juego = info_juego
