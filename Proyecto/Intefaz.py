import tkinter as tk
from _thread import start_new_thread
from tkinter import ttk
import Cliente


class Interfaz:

    def __init__(self, juego, jugador, continuar_juego):
        self._ventana = tk.Tk()
        self._nombre_ingresado = tk.StringVar()
        self._juego = juego
        self._jugador = jugador
        self._continuar_juego = continuar_juego
        self._ventana.title("Ajedrez Clásico")
        self.ingreso_nombre()

    def ingreso_nombre(self):
        label_nombre = tk.Label(self._ventana, text="Nombre")
        label_nombre.pack()
        label_mensaje = tk.Label(self._ventana)
        label_mensaje.pack()
        input_nombre = tk.Entry(self._ventana, textvariable=self._nombre_ingresado)
        input_nombre.focus()
        input_nombre.pack()
        btn_ingresa_nombre = tk.Button(
            self._ventana, text="Aceptar",
            command=self.click_nombre)
        btn_ingresa_nombre.pack()
        btn_salir = tk.Button(self._ventana, text="Salir", command=self.salir).pack()

    def salir(self):
        quit()

    def click_nombre(self):
        elementos = self._ventana.pack_slaves()

        if self.nombre_valido():
            for elemento in elementos:
                if elemento._name == '!label2':
                    elemento["text"] = ""
            self._jugador.set_nombre(self._nombre_ingresado.get().capitalize())
            self.limpiar_ventana()
            self.mostrar_modos_juego()
        else:

            for elemento in elementos:
                if elemento._name == '!label2':
                    elemento["text"] = "Ingrese un nombre"

    def nombre_valido(self):
        return self._nombre_ingresado.get()

    def mostrar_modos_juego(self):
        tk.Button(self._ventana, text="Entrenamiento", command=self.click_entrenamiento).pack()
        # tk.Button(self._ventana, text="Jugador 1 VS CPU", command=self.click_vsCPU).pack()
        tk.Button(self._ventana, text="Jugador 1 VS Jugador 2", command=self.click_vsJug2).pack()
        tk.Button(self._ventana, text="Crear partida red local", command=self.click_crear_partida_red_local).pack()
        tk.Button(self._ventana, text="Unirse a partida red local", command=self.click_unirse_partida_red_local).pack()
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

    def click_crear_partida_red_local(self):
        self._juego.set_modo("online")
        self.limpiar_ventana()
        self.elegir_color()

    def click_unirse_partida_red_local(self):
        self._juego.set_modo("online")
        self.limpiar_ventana()
        self._ventana.destroy()
        self.iniciar_cliente()

    def elegir_color(self):
        self.limpiar_ventana()
        global pieza_blanca
        global pieza_negra
        pieza_blanca = tk.PhotoImage(file=r"./assets/wp.png")
        pieza_negra = tk.PhotoImage(file=r"./assets/bp.png")

        btn_blancas = ttk.Button(
            self._ventana,
            image=pieza_blanca,
            command=lambda blancas=True: self.click_color(blancas))
        btn_negras = ttk.Button(
            self._ventana,
            image=pieza_negra,
            command=lambda blancas=False: self.click_color(blancas))

        btn_blancas.pack()
        btn_negras.pack()
        ttk.Button(self._ventana, text="Volver", command=self.volver_a_modos).pack()

    def click_color(self, blancas):
        self._jugador.set_es_blanco(blancas)
        if self._jugador.get_es_blanco():
            self._juego.set_jugador_blanco(self._jugador)
        else:
            self._juego.set_jugador_negro(self._jugador)
        self._ventana.destroy()
        if self._juego.get_modo() == "online":
            self.crear_partida()
        else:
            self._continuar_juego()

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
        self._continuar_juego()

    def mostrar_ventana(self):
        self._ventana.mainloop()

    def limpiar_ventana(self):
        elementos = self._ventana.pack_slaves()
        for elemento in elementos:
            elemento.destroy()