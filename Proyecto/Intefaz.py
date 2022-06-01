import tkinter as tk
from _thread import start_new_thread
import Cliente


class Interfaz:

    def __init__(self, juego, jugador):
        self._ventana = tk.Tk()
        self._nombre_ingresado = tk.StringVar()
        self._juego = juego
        self._jugador = jugador
        self.ingreso_nombre()

    def ingreso_nombre(self):
        label_nombre = tk.Label(self._ventana, text="Nombre")
        label_nombre.pack()
        input_nombre = tk.Entry(self._ventana, textvariable=self._nombre_ingresado)
        input_nombre.pack()
        btn_ingresa_nombre = tk.Button(
            self._ventana, text="Aceptar",
            command=self.click_nombre)
        btn_ingresa_nombre.pack()

    def click_nombre(self):
        self._jugador.set_nombre(self._nombre_ingresado.get())
        self.limpiar_ventana()
        self.mostrar_modos_juego()

    def limpiar_ventana(self):
        elementos = self._ventana.pack_slaves()
        for elemento in elementos:
            elemento.destroy()


    def mostrar_modos_juego(self):
        tk.Button(self._ventana, text="Entrenamiento", command=self.click_entrenamiento).pack()
        tk.Button(self._ventana, text="Jugador 1 VS CPU", command=self.click_vsCPU).pack()
        tk.Button(self._ventana, text="Jugador 1 VS Jugador 2", command=self.click_vsJug2).pack()
        tk.Button(self._ventana, text="Online", command=self.click_online).pack()
        tk.Button(self._ventana, text="Volver", command=self.volver_a_nombre).pack()

    def volver_a_nombre(self):
        self.limpiar_ventana()
        self.ingreso_nombre()

    def click_entrenamiento(self):
        self._juego.set_modo("entrenamiento")
        self.limpiar_ventana()
        self.elegir_color()

    def click_vsCPU(self):
        self._juego.set_modo("vsCPU")
        self.limpiar_ventana()
        self.elegir_color()

    def click_vsJug2(self):
        self._juego.set_modo("vsJug2")
        self.limpiar_ventana()
        self.elegir_color()

    def click_online(self):
        self._juego.set_modo("online")
        self.limpiar_ventana()
        self.opciones_online()

    def opciones_online(self):
        tk.Button(self._ventana, text="Crear partida", command=self.elegir_color).pack()
        tk.Button(self._ventana, text="Unirse", command=self.iniciar_cliente).pack()
        tk.Button(self._ventana, text="Volver", command=self.volver_a_modos).pack()

    def volver_a_modos(self):
        self.limpiar_ventana()
        self.mostrar_modos_juego()

    def crear_partida(self):
        start_new_thread(self.iniciar_servidor, ())
        self.iniciar_cliente()

    def iniciar_servidor(self):
        import Server

    def iniciar_cliente(self):
        start_new_thread(Cliente.main, (self._jugador, self._juego))
        self._ventana.destroy()

    def mostrar_ventana(self):
        self._ventana.mainloop()

    def elegir_color(self):
        self.limpiar_ventana()
        btn_blancas = tk.Button(
            self._ventana, text="Blancas",
            command=lambda blancas=True: self.click_color(blancas))
        btn_negras = tk.Button(
            self._ventana, text="Negras",
            command=lambda blancas=False: self.click_color(blancas))
        btn_blancas.pack()
        btn_negras.pack()

    def click_color(self, blancas):
        self._jugador.set_es_blanco(blancas)
        if self._jugador.get_es_blanco():
            self._juego.set_jugador_blanco(self._jugador)
        else:
            self._juego.set_jugador_negro(self._jugador)
        self._ventana.destroy()
        if self._juego.get_modo() == "online":
            self.crear_partida()