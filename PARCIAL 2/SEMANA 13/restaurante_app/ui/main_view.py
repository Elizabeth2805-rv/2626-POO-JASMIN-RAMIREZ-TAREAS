# -*- coding: utf-8 -*-
# ui/main_view.py
# Semana 13 — Transición a Interfaz Gráfica Tkinter (Base Restaurante)
#
# Principio SRP: Esta vista representa la interfaz principal del restaurante,
# mostrando la información cargada de productos y usuarios desde RestauranteServicio
# y permitiendo el retorno al login al cerrar sesión.

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class MainView(tk.Frame):
    """
    Vista principal (Dashboard) del restaurante después del inicio de sesión.

    Muestra:
    - Encabezado con información del usuario autenticado y botón de cerrar sesión.
    - Menú de navegación para cambiar entre Productos, Usuarios y Ventas (Pendiente).
    - Tablas de datos interactivas (ttk.Treeview) que solicitan la información a RestauranteServicio.
    - Barra de estado con resumen de métricas del sistema.
    """

    def __init__(
        self,
        master: tk.Widget,
        restaurante_servicio: RestauranteServicio,
        usuario_actual: Usuario,
        on_logout: Callable[[], None],
        **kwargs
    ) -> None:
        """
        Constructor de MainView.

        Args:
            master:               Contenedor principal Tkinter.
            restaurante_servicio: Instancia del servicio de negocio.
            usuario_actual:       Instancia del usuario actualmente autenticado.
            on_logout:            Callback para regresar a la pantalla de Login.
        """
        super().__init__(master, bg="#F3F4F6", **kwargs)
        self._restaurante_servicio = restaurante_servicio
        self._usuario_actual = usuario_actual
        self._on_logout = on_logout

        # Vista actualmente activa ('productos', 'usuarios', 'ventas')
        self._seccion_activa = "productos"

        self._crear_interfaz()
        self.actualizar_datos()

    def set_usuario_actual(self, usuario: Usuario) -> None:
        """Actualiza la referencia del usuario actual y refresca la interfaz."""
        self._usuario_actual = usuario
        self._lbl_usuario_info.config(
            text=f"👤 Usuario: {usuario.nombre} ({usuario.identificacion})"
        )
        self.actualizar_datos()

    def _crear_interfaz(self) -> None:
        """Construye el diseño y componentes visuales de la vista principal."""
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        # ------------------------------------------------------------------ #
        #  1. Barra Superior (Header)                                        #
        # ------------------------------------------------------------------ #
        header = tk.Frame(self, bg="#1E293B", pady=10, padx=20)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")

        lbl_app_title = tk.Label(
            header,
            text="🍽️ Restaurante App — Panel Principal",
            font=("Segoe UI", 14, "bold"),
            fg="#F8FAFC",
            bg="#1E293B",
        )
        lbl_app_title.pack(side="left")

        btn_logout = tk.Button(
            header,
            text="🚪 Cerrar Sesión",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#EF4444",
            activebackground="#DC2626",
            activeforeground="#FFFFFF",
            bd=0,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self._on_logout,
        )
        btn_logout.pack(side="right")

        self._lbl_usuario_info = tk.Label(
            header,
            text=f"👤 Usuario: {self._usuario_actual.nombre} ({self._usuario_actual.identificacion})",
            font=("Segoe UI", 10),
            fg="#94A3B8",
            bg="#1E293B",
        )
        self._lbl_usuario_info.pack(side="right", padx=15)

        # ------------------------------------------------------------------ #
        #  2. Menú Lateral de Navegación (Sidebar)                           #
        # ------------------------------------------------------------------ #
        sidebar = tk.Frame(self, bg="#0F172A", width=200, padx=10, pady=15)
        sidebar.grid(row=1, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        lbl_nav_title = tk.Label(
            sidebar,
            text="NAVEGACIÓN",
            font=("Segoe UI", 8, "bold"),
            fg="#64748B",
            bg="#0F172A",
            anchor="w",
        )
        lbl_nav_title.pack(fill="x", pady=(0, 10))

        self.btn_nav_productos = self._crear_boton_nav(
            sidebar, "📦 Productos Registrados", lambda: self._cambiar_seccion("productos")
        )
        self.btn_nav_usuarios = self._crear_boton_nav(
            sidebar, "👥 Usuarios Registrados", lambda: self._cambiar_seccion("usuarios")
        )
        self.btn_nav_ventas = self._crear_boton_nav(
            sidebar, "🛒 Ventas (Pendiente)", lambda: self._cambiar_seccion("ventas")
        )

        # ------------------------------------------------------------------ #
        #  3. Panel de Contenido Principal                                   #
        # ------------------------------------------------------------------ #
        self.panel_contenido = tk.Frame(self, bg="#F3F4F6", padx=20, pady=15)
        self.panel_contenido.grid(row=1, column=1, sticky="nsew")
        self.panel_contenido.rowconfigure(1, weight=1)
        self.panel_contenido.columnconfigure(0, weight=1)

        # Sub-encabezado de sección
        self.lbl_seccion_titulo = tk.Label(
            self.panel_contenido,
            text="📦 Productos Registrados",
            font=("Segoe UI", 16, "bold"),
            fg="#0F172A",
            bg="#F3F4F6",
            anchor="w",
        )
        self.lbl_seccion_titulo.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Contenedor para las tablas o vistas
        self.container_vistas = tk.Frame(self.panel_contenido, bg="#F3F4F6")
        self.container_vistas.grid(row=1, column=0, sticky="nsew")
        self.container_vistas.rowconfigure(0, weight=1)
        self.container_vistas.columnconfigure(0, weight=1)

        # Crear los sub-frames para cada sección
        self.frame_productos = self._crear_frame_productos(self.container_vistas)
        self.frame_usuarios = self._crear_frame_usuarios(self.container_vistas)
        self.frame_ventas = self._crear_frame_ventas(self.container_vistas)

        # ------------------------------------------------------------------ #
        #  4. Barra de Estado (Statusbar)                                    #
        # ------------------------------------------------------------------ #
        statusbar = tk.Frame(self, bg="#E2E8F0", height=25, padx=15, pady=3)
        statusbar.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.lbl_status = tk.Label(
            statusbar,
            text="🟢 Estado: Sistema conectado | Datos obtenidos desde RestauranteServicio",
            font=("Segoe UI", 8),
            fg="#334155",
            bg="#E2E8F0",
        )
        self.lbl_status.pack(side="left")

        # Seleccionar por defecto Productos
        self._cambiar_seccion("productos")

    def _crear_boton_nav(
        self, parent: tk.Widget, texto: str, comando: Callable[[], None]
    ) -> tk.Button:
        """Crea un botón de navegación estilizado para el sidebar."""
        btn = tk.Button(
            parent,
            text=texto,
            font=("Segoe UI", 9, "bold"),
            fg="#94A3B8",
            bg="#0F172A",
            activebackground="#1E293B",
            activeforeground="#F8FAFC",
            bd=0,
            anchor="w",
            padx=12,
            pady=10,
            cursor="hand2",
            command=comando,
        )
        btn.pack(fill="x", pady=2)
        return btn

    def _cambiar_seccion(self, seccion: str) -> None:
        """Cambia la sección visible en el panel principal."""
        self._seccion_activa = seccion

        # Restablecer colores de botones de navegación
        for btn in (self.btn_nav_productos, self.btn_nav_usuarios, self.btn_nav_ventas):
            btn.config(bg="#0F172A", fg="#94A3B8")

        # Ocultar todos los sub-frames
        self.frame_productos.grid_forget()
        self.frame_usuarios.grid_forget()
        self.frame_ventas.grid_forget()

        # Mostrar la sección correspondiente
        if seccion == "productos":
            self.btn_nav_productos.config(bg="#1E293B", fg="#F8FAFC")
            self.lbl_seccion_titulo.config(text="📦 Productos Registrados")
            self.frame_productos.grid(row=0, column=0, sticky="nsew")
        elif seccion == "usuarios":
            self.btn_nav_usuarios.config(bg="#1E293B", fg="#F8FAFC")
            self.lbl_seccion_titulo.config(text="👥 Usuarios Registrados")
            self.frame_usuarios.grid(row=0, column=0, sticky="nsew")
        elif seccion == "ventas":
            self.btn_nav_ventas.config(bg="#1E293B", fg="#F8FAFC")
            self.lbl_seccion_titulo.config(text="🛒 Gestión de Ventas (Pendiente)")
            self.frame_ventas.grid(row=0, column=0, sticky="nsew")

    # ------------------------------------------------------------------ #
    #  Construcción de Sub-frames                                        #
    # ------------------------------------------------------------------ #
    def _crear_frame_productos(self, parent: tk.Widget) -> tk.Frame:
        """Crea la vista y tabla ttk.Treeview de productos."""
        frame = tk.Frame(parent, bg="#F3F4F6")
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        # Tarjetas de resumen
        frame_cards = tk.Frame(frame, bg="#F3F4F6")
        frame_cards.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.lbl_card_total_prod = tk.Label(
            frame_cards,
            text="Total Productos: 0",
            font=("Segoe UI", 10, "bold"),
            fg="#1E40AF",
            bg="#DBEAFE",
            padx=12,
            pady=6,
            relief="solid",
            bd=1,
        )
        self.lbl_card_total_prod.pack(side="left", padx=(0, 10))

        self.lbl_card_total_stock = tk.Label(
            frame_cards,
            text="Stock Total: 0 unidades",
            font=("Segoe UI", 10, "bold"),
            fg="#065F46",
            bg="#D1FAE5",
            padx=12,
            pady=6,
            relief="solid",
            bd=1,
        )
        self.lbl_card_total_stock.pack(side="left")

        # Tabla Treeview para Productos
        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tree_productos = ttk.Treeview(
            frame, columns=columnas, show="headings", height=12
        )

        self.tree_productos.heading("codigo", text="Código")
        self.tree_productos.heading("nombre", text="Nombre del Producto")
        self.tree_productos.heading("categoria", text="Categoría")
        self.tree_productos.heading("precio", text="Precio ($)")
        self.tree_productos.heading("stock", text="Stock (uds)")

        self.tree_productos.column("codigo", width=90, anchor="center")
        self.tree_productos.column("nombre", width=220, anchor="w")
        self.tree_productos.column("categoria", width=140, anchor="w")
        self.tree_productos.column("precio", width=100, anchor="e")
        self.tree_productos.column("stock", width=100, anchor="center")

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.tree_productos.yview
        )
        self.tree_productos.configure(yscrollcommand=scrollbar.set)

        self.tree_productos.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        return frame

    def _crear_frame_usuarios(self, parent: tk.Widget) -> tk.Frame:
        """Crea la vista y tabla ttk.Treeview de usuarios."""
        frame = tk.Frame(parent, bg="#F3F4F6")
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        # Tarjeta de resumen
        frame_cards = tk.Frame(frame, bg="#F3F4F6")
        frame_cards.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.lbl_card_total_usr = tk.Label(
            frame_cards,
            text="Total Usuarios Registrados: 0",
            font=("Segoe UI", 10, "bold"),
            fg="#6B21A8",
            bg="#F3E8FF",
            padx=12,
            pady=6,
            relief="solid",
            bd=1,
        )
        self.lbl_card_total_usr.pack(side="left")

        # Tabla Treeview para Usuarios
        columnas = ("identificacion", "nombre", "correo")
        self.tree_usuarios = ttk.Treeview(
            frame, columns=columnas, show="headings", height=12
        )

        self.tree_usuarios.heading("identificacion", text="Identificación / Cédula")
        self.tree_usuarios.heading("nombre", text="Nombre Completo")
        self.tree_usuarios.heading("correo", text="Correo Electrónico")

        self.tree_usuarios.column("identificacion", width=150, anchor="center")
        self.tree_usuarios.column("nombre", width=250, anchor="w")
        self.tree_usuarios.column("correo", width=250, anchor="w")

        scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=self.tree_usuarios.yview
        )
        self.tree_usuarios.configure(yscrollcommand=scrollbar.set)

        self.tree_usuarios.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        return frame

    def _crear_frame_ventas(self, parent: tk.Widget) -> tk.Frame:
        """Crea la vista informativa de ventas pendientes."""
        frame = tk.Frame(parent, bg="#FFFFFF", bd=1, relief="solid", padx=30, pady=40)
        
        lbl_icon = tk.Label(
            frame, text="🚧", font=("Segoe UI Emoji", 48), bg="#FFFFFF"
        )
        lbl_icon.pack(pady=(0, 10))

        lbl_titulo = tk.Label(
            frame,
            text="Módulo de Ventas Pendiente",
            font=("Segoe UI", 16, "bold"),
            fg="#9A3412",
            bg="#FFFFFF",
        )
        lbl_titulo.pack(pady=(0, 5))

        lbl_desc = tk.Label(
            frame,
            text=(
                "Esta funcionalidad se incorporará progresivamente en las próximas semanas "
                "conforme avance la materia.\nActualmente la base gráfica de la Semana 13 "
                "permite la autenticación y consulta de Productos y Usuarios."
            ),
            font=("Segoe UI", 10),
            fg="#4B5563",
            bg="#FFFFFF",
            justify="center",
        )
        lbl_desc.pack()

        return frame

    # ------------------------------------------------------------------ #
    #  Carga de Datos desde RestauranteServicio                           #
    # ------------------------------------------------------------------ #
    def actualizar_datos(self) -> None:
        """
        Solicita la información a RestauranteServicio (NUNCA directamente desde archivos JSON)
        y actualiza las tablas ttk.Treeview y métricas de la interfaz.
        """
        # 1. Cargar Productos
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)

        productos = self._restaurante_servicio.obtener_productos()
        for prod in productos:
            self.tree_productos.insert(
                "",
                "end",
                values=(
                    prod.codigo,
                    prod.nombre,
                    prod.categoria,
                    f"${prod.precio:.2f}",
                    prod.stock,
                ),
            )

        # Actualizar métricas de productos
        total_p = self._restaurante_servicio.obtener_total_productos()
        total_s = self._restaurante_servicio.obtener_total_stock()
        self.lbl_card_total_prod.config(text=f"Total Productos: {total_p}")
        self.lbl_card_total_stock.config(text=f"Stock Total: {total_s} unidades")

        # 2. Cargar Usuarios
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)

        usuarios = self._restaurante_servicio.obtener_usuarios()
        for usr in usuarios:
            self.tree_usuarios.insert(
                "",
                "end",
                values=(
                    usr.identificacion,
                    usr.nombre,
                    usr.correo,
                ),
            )

        # Actualizar métrica de usuarios
        total_u = self._restaurante_servicio.obtener_total_usuarios()
        self.lbl_card_total_usr.config(text=f"Total Usuarios Registrados: {total_u}")
