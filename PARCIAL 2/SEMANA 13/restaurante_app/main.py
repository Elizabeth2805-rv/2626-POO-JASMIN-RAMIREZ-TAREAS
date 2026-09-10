# -*- coding: utf-8 -*-
# main.py
# Semana 13 — Transición a Interfaz Gráfica Tkinter (Base Restaurante)
#
# Punto de entrada de la aplicación Restaurante App.
# Responsabilidades:
# 1. Crear una ÚNICA ventana principal de Tkinter (`tk.Tk()`).
# 2. Instanciar los servicios (`ArchivoServicio` y `RestauranteServicio`).
# 3. Entregar las dependencias a las vistas (`LoginView` y `MainView`).
# 4. Controlar el cambio de pantallas (Login ↔ Main) manteniendo el mismo mainloop.

import os
import sys
import tkinter as tk
from typing import Optional

# Asegurar que el directorio raíz de restaurante_app esté en el sys.path
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
if DIRECTORIO_BASE not in sys.path:
    sys.path.insert(0, DIRECTORIO_BASE)

from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class RestauranteApp:
    """
    Clase principal que orquesta el ciclo de vida de la aplicación con interfaz gráfica.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Constructor de RestauranteApp.

        Args:
            root: Instancia principal de la ventana Tkinter.
        """
        self.root = root
        self._configurar_ventana_principal()

        # Rutas absolutas a los datos JSON
        ruta_productos = os.path.join(DIRECTORIO_BASE, "datos", "productos.json")
        ruta_usuarios = os.path.join(DIRECTORIO_BASE, "datos", "usuarios.json")

        # Preparación de servicios (Inyección de dependencias)
        self.archivo_servicio = ArchivoServicio(
            directorio_datos=os.path.join(DIRECTORIO_BASE, "datos")
        )
        self.restaurante_servicio = RestauranteServicio(
            archivo_servicio=self.archivo_servicio,
            ruta_productos=ruta_productos,
            ruta_usuarios=ruta_usuarios,
        )

        # Referencia al usuario en sesión
        self.usuario_actual: Optional[Usuario] = None

        # Contenedor principal de vistas (Frame dinámico)
        self.container = tk.Frame(self.root, bg="#F3F4F6")
        self.container.pack(fill="both", expand=True)
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        # Instanciar vistas
        self.login_view = LoginView(
            master=self.container,
            restaurante_servicio=self.restaurante_servicio,
            on_login_success=self.al_iniciar_sesion_exitosa,
        )

        self.main_view: Optional[MainView] = None

        # Mostrar pantalla inicial de Login
        self.mostrar_login()

    def _configurar_ventana_principal(self) -> None:
        """Establece títulos, dimensiones y centrados de la única ventana Tkinter."""
        self.root.title("Restaurante App — Gestión Base con Tkinter (Semana 13)")
        self.root.geometry("900x600")
        self.root.minsize(800, 550)

        # Centrar ventana en pantalla
        self.root.update_idletasks()
        ancho_ventana = self.root.winfo_width()
        alto_ventana = self.root.winfo_height()
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        pos_x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        pos_y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.root.geometry(f"+{pos_x}+{pos_y}")

    def mostrar_login(self) -> None:
        """Muestra la vista de inicio de sesión (LoginView) dentro de la misma ventana."""
        if self.main_view is not None:
            self.main_view.grid_forget()

        self.login_view.grid(row=0, column=0, sticky="nsew")
        self.login_view.enfocar()

    def mostrar_main(self) -> None:
        """Muestra la vista principal (MainView) tras un login correcto."""
        self.login_view.grid_forget()

        if self.usuario_actual is None:
            self.mostrar_login()
            return

        if self.main_view is None:
            self.main_view = MainView(
                master=self.container,
                restaurante_servicio=self.restaurante_servicio,
                usuario_actual=self.usuario_actual,
                on_logout=self.al_cerrar_sesion,
            )
        else:
            self.main_view.set_usuario_actual(self.usuario_actual)

        self.main_view.grid(row=0, column=0, sticky="nsew")

    def al_iniciar_sesion_exitosa(self, usuario: Usuario) -> None:
        """Callback ejecutado cuando LoginView autentica un usuario."""
        self.usuario_actual = usuario
        self.mostrar_main()

    def al_cerrar_sesion(self) -> None:
        """Callback ejecutado cuando MainView solicita cerrar sesión."""
        self.usuario_actual = None
        self.mostrar_login()


def main() -> None:
    """Punto de entrada principal para iniciar la aplicación."""
    root = tk.Tk()
    app = RestauranteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
