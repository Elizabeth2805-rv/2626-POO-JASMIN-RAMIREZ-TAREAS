# -*- coding: utf-8 -*-
# ui/login_view.py
# Semana 13 — Transición a Interfaz Gráfica Tkinter (Base Restaurante)
#
# Principio SRP: Esta vista es responsable exclusivamente de la presentación
# visual de la pantalla de inicio de sesión (Login) y de capturar los eventos
# del usuario para solicitar validación al servicio.

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class LoginView(tk.Frame):
    """
    Vista de inicio de sesión (Login) de la aplicación Restaurante App.

    Presenta los controles Tkinter de entrada para usuario y contraseña,
    valida campos vacíos o errores visualmente y ejecuta el callback al autenticar.
    """

    def __init__(
        self,
        master: tk.Widget,
        restaurante_servicio: RestauranteServicio,
        on_login_success: Callable[[Usuario], None],
        **kwargs
    ) -> None:
        """
        Constructor de LoginView.

        Args:
            master:               Contenedor principal Tkinter.
            restaurante_servicio: Instancia del servicio de negocio.
            on_login_success:     Callback que se ejecuta cuando el login es exitoso.
        """
        super().__init__(master, bg="#F3F4F6", **kwargs)
        self._restaurante_servicio = restaurante_servicio
        self._on_login_success = on_login_success

        self._crear_interfaz()

    def _crear_interfaz(self) -> None:
        """Construye los elementos visuales de la vista de login."""
        # Configuración del grid principal para centrar la tarjeta de login
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Tarjeta contenedora de Login
        card = tk.Frame(
            self,
            bg="#FFFFFF",
            bd=1,
            relief="solid",
            highlightbackground="#E5E7EB",
            highlightthickness=1,
            padx=35,
            pady=30,
        )
        card.grid(row=0, column=0)

        # Icono / Encabezado
        lbl_titulo_icono = tk.Label(
            card,
            text="🍽️",
            font=("Segoe UI Emoji", 40),
            bg="#FFFFFF",
        )
        lbl_titulo_icono.pack(pady=(0, 5))

        lbl_titulo = tk.Label(
            card,
            text="Restaurante App",
            font=("Segoe UI", 18, "bold"),
            fg="#1F2937",
            bg="#FFFFFF",
        )
        lbl_titulo.pack(pady=(0, 2))

        lbl_subtitulo = tk.Label(
            card,
            text="Acceso al Sistema — Semana 13 (GUI)",
            font=("Segoe UI", 10),
            fg="#6B7280",
            bg="#FFFFFF",
        )
        lbl_subtitulo.pack(pady=(0, 20))

        # Campo: Usuario / Identificación
        lbl_user = tk.Label(
            card,
            text="Usuario / Cédula / Correo:",
            font=("Segoe UI", 10, "bold"),
            fg="#374151",
            bg="#FFFFFF",
            anchor="w",
        )
        lbl_user.pack(fill="x", pady=(5, 2))

        self.txt_usuario = ttk.Entry(card, font=("Segoe UI", 11), width=30)
        self.txt_usuario.pack(fill="x", pady=(0, 12))
        self.txt_usuario.focus_set()

        # Campo: Contraseña
        lbl_pass = tk.Label(
            card,
            text="Contraseña:",
            font=("Segoe UI", 10, "bold"),
            fg="#374151",
            bg="#FFFFFF",
            anchor="w",
        )
        lbl_pass.pack(fill="x", pady=(5, 2))

        self.txt_password = ttk.Entry(
            card, font=("Segoe UI", 11), show="•", width=30
        )
        self.txt_password.pack(fill="x", pady=(0, 15))

        # Enlazar la tecla Enter (Return) para iniciar sesión directamente
        self.txt_usuario.bind("<Return>", lambda e: self._ejecutar_login())
        self.txt_password.bind("<Return>", lambda e: self._ejecutar_login())

        # Etiqueta de mensaje de error/retroalimentación visual
        self.lbl_mensaje = tk.Label(
            card,
            text="",
            font=("Segoe UI", 9, "bold"),
            fg="#DC2626",
            bg="#FFFFFF",
            wraplength=280,
            justify="center",
        )
        self.lbl_mensaje.pack(fill="x", pady=(0, 10))

        # Botón Iniciar Sesión
        btn_login = tk.Button(
            card,
            text="Iniciar Sesión",
            font=("Segoe UI", 11, "bold"),
            fg="#FFFFFF",
            bg="#2563EB",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self._ejecutar_login,
        )
        btn_login.pack(fill="x", pady=(5, 15))

        # Pista informativa para pruebas rápidas
        lbl_hint = tk.Label(
            card,
            text="💡 Credenciales de prueba:\nUsuario: 0102030405 | Clave: 1234",
            font=("Segoe UI", 8),
            fg="#6B7280",
            bg="#F9FAFB",
            padx=10,
            pady=8,
            relief="groove",
            bd=1,
        )
        lbl_hint.pack(fill="x")

    def _ejecutar_login(self) -> None:
        """
        Procesa el intento de inicio de sesión:
        1. Captura usuario y contraseña.
        2. Valida que no estén vacíos.
        3. Invoca la regla de negocio en RestauranteServicio.
        4. Muestra retroalimentación visual en caso de fallo o invoca callback si es exitoso.
        """
        usuario_val = self.txt_usuario.get().strip()
        pass_val = self.txt_password.get().strip()

        # Validación 1: Campos vacíos
        if not usuario_val or not pass_val:
            self._mostrar_error("⚠️ Por favor ingrese el usuario y la contraseña.")
            return

        # Validación 2: Autenticación mediante RestauranteServicio
        usuario_autenticado = self._restaurante_servicio.validar_acceso(
            usuario_val, pass_val
        )

        if usuario_autenticado is not None:
            # Limpiar campos y mensajes de error
            self.lbl_mensaje.config(text="")
            self.txt_usuario.delete(0, tk.END)
            self.txt_password.delete(0, tk.END)

            # Notificar éxito a la ventana principal main.py
            self._on_login_success(usuario_autenticado)
        else:
            self._mostrar_error(
                "❌ Credenciales incorrectas. Verifique el usuario o la contraseña."
            )

    def _mostrar_error(self, mensaje: str) -> None:
        """Muestra un mensaje de error visual en la interfaz."""
        self.lbl_mensaje.config(text=mensaje, fg="#DC2626")

    def enfocar(self) -> None:
        """Establece el foco en el campo de usuario."""
        self.txt_usuario.focus_set()
