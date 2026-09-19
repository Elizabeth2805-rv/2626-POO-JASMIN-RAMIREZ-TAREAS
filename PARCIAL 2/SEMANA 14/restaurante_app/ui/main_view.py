# -*- coding: utf-8 -*-
# ui/main_view.py
# Semana 14 — Componentes y Contenedores (Evolución Restaurante App)
#
# Principio SRP: Esta vista representa la interfaz principal del restaurante,
# organizada con contenedores (Frame, LabelFrame) y componentes Tkinter/ttk (Entry,
# Combobox, Spinbox, Button, Treeview). Delega todas las reglas de negocio y
# persistencia a RestauranteServicio para las secciones de Productos y Usuarios.

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
from modelos.usuario import Usuario
from modelos.producto import Producto
from servicios.restaurante_servicio import RestauranteServicio


class MainView(tk.Frame):
    """
    Vista principal (Dashboard) del restaurante evolucionada para la Semana 14.

    Muestra:
    - Encabezado con información del usuario autenticado y botón de cerrar sesión.
    - Menú de navegación lateral (Sidebar).
    - Sección de Productos con CRUD completo (Formulario + Botones + Treeview + JSON).
    - Sección de Usuarios con CRUD completo (Formulario + Botones + Treeview + JSON).
    - Sección Informativa de Ventas (Pendiente).
    - Barra de Estado con resumen de operaciones.
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

        # Sección actualmente activa ('productos', 'usuarios', 'ventas')
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
        """Construye la distribución por capas y contenedores de la vista principal."""
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        # ------------------------------------------------------------------ #
        #  1. Contenedor Superior (Header / Barra de Título)                #
        # ------------------------------------------------------------------ #
        header = tk.Frame(self, bg="#1E293B", pady=10, padx=20)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")

        lbl_app_title = tk.Label(
            header,
            text="🍽️ Restaurante App — Panel de Gestión (Semana 14)",
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
        #  2. Contenedor Lateral (Sidebar / Menú de Navegación)             #
        # ------------------------------------------------------------------ #
        sidebar = tk.Frame(self, bg="#0F172A", width=210, padx=10, pady=15)
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
            sidebar, "📦 Gestión de Productos", lambda: self._cambiar_seccion("productos")
        )
        self.btn_nav_usuarios = self._crear_boton_nav(
            sidebar, "👥 Gestión de Usuarios", lambda: self._cambiar_seccion("usuarios")
        )
        self.btn_nav_ventas = self._crear_boton_nav(
            sidebar, "🛒 Módulo Ventas (Pendiente)", lambda: self._cambiar_seccion("ventas")
        )

        # ------------------------------------------------------------------ #
        #  3. Contenedor de Contenido Principal                             #
        # ------------------------------------------------------------------ #
        self.panel_contenido = tk.Frame(self, bg="#F3F4F6", padx=15, pady=12)
        self.panel_contenido.grid(row=1, column=1, sticky="nsew")
        self.panel_contenido.rowconfigure(1, weight=1)
        self.panel_contenido.columnconfigure(0, weight=1)

        # Sub-encabezado dinámico de la sección activa
        self.lbl_seccion_titulo = tk.Label(
            self.panel_contenido,
            text="📦 Gestión de Productos del Restaurante",
            font=("Segoe UI", 15, "bold"),
            fg="#0F172A",
            bg="#F3F4F6",
            anchor="w",
        )
        self.lbl_seccion_titulo.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        # Contenedor hijo donde alternan las pantallas del dashboard
        self.container_vistas = tk.Frame(self.panel_contenido, bg="#F3F4F6")
        self.container_vistas.grid(row=1, column=0, sticky="nsew")
        self.container_vistas.rowconfigure(0, weight=1)
        self.container_vistas.columnconfigure(0, weight=1)

        # Crear los sub-frames para cada sección
        self.frame_productos = self._crear_frame_productos(self.container_vistas)
        self.frame_usuarios = self._crear_frame_usuarios(self.container_vistas)
        self.frame_ventas = self._crear_frame_ventas(self.container_vistas)

        # ------------------------------------------------------------------ #
        #  4. Contenedor de Estado (Statusbar)                               #
        # ------------------------------------------------------------------ #
        statusbar = tk.Frame(self, bg="#E2E8F0", height=25, padx=15, pady=3)
        statusbar.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.lbl_status = tk.Label(
            statusbar,
            text="🟢 Estado: Conectado | Operaciones delegadas a RestauranteServicio (JSON Activo)",
            font=("Segoe UI", 8),
            fg="#334155",
            bg="#E2E8F0",
        )
        self.lbl_status.pack(side="left")

        # Seleccionar por defecto la sección de Productos
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

        for btn in (self.btn_nav_productos, self.btn_nav_usuarios, self.btn_nav_ventas):
            btn.config(bg="#0F172A", fg="#94A3B8")

        self.frame_productos.grid_forget()
        self.frame_usuarios.grid_forget()
        self.frame_ventas.grid_forget()

        if seccion == "productos":
            self.btn_nav_productos.config(bg="#1E293B", fg="#F8FAFC")
            self.lbl_seccion_titulo.config(text="📦 Gestión de Productos del Restaurante")
            self.frame_productos.grid(row=0, column=0, sticky="nsew")
        elif seccion == "usuarios":
            self.btn_nav_usuarios.config(bg="#1E293B", fg="#F8FAFC")
            self.lbl_seccion_titulo.config(text="👥 Gestión de Usuarios del Sistema")
            self.frame_usuarios.grid(row=0, column=0, sticky="nsew")
        elif seccion == "ventas":
            self.btn_nav_ventas.config(bg="#1E293B", fg="#F8FAFC")
            self.lbl_seccion_titulo.config(text="🛒 Módulo de Ventas (Pendiente)")
            self.frame_ventas.grid(row=0, column=0, sticky="nsew")

    # ------------------------------------------------------------------ #
    #  Construcción de Sección: PRODUCTOS (Componentes + Contenedores)   #
    # ------------------------------------------------------------------ #
    def _crear_frame_productos(self, parent: tk.Widget) -> tk.Frame:
        """
        Construye la interfaz de gestión de productos utilizando contenedores
        (ttk.LabelFrame, tk.Frame) y componentes de formulario y visualización.
        """
        frame_main = tk.Frame(parent, bg="#F3F4F6")
        frame_main.rowconfigure(1, weight=1)
        frame_main.columnconfigure(0, weight=1)
        frame_main.columnconfigure(1, weight=2)

        # Tarjetas de resumen
        frame_cards = tk.Frame(frame_main, bg="#F3F4F6")
        frame_cards.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        self.lbl_card_total_prod = tk.Label(
            frame_cards,
            text="Total Productos: 0",
            font=("Segoe UI", 9, "bold"),
            fg="#1E40AF",
            bg="#DBEAFE",
            padx=12,
            pady=5,
            relief="solid",
            bd=1,
        )
        self.lbl_card_total_prod.pack(side="left", padx=(0, 10))

        self.lbl_card_total_stock = tk.Label(
            frame_cards,
            text="Stock Total: 0 unidades",
            font=("Segoe UI", 9, "bold"),
            fg="#065F46",
            bg="#D1FAE5",
            padx=12,
            pady=5,
            relief="solid",
            bd=1,
        )
        self.lbl_card_total_stock.pack(side="left")

        # CONTENEDOR 1: Formulario y Acciones CRUD (Panel Izquierdo)
        form_frame = ttk.LabelFrame(
            frame_main, text=" 📝 Formulario de Producto ", padding=(15, 12)
        )
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        form_frame.columnconfigure(1, weight=1)

        # Campos
        lbl_codigo = ttk.Label(form_frame, text="Código:")
        lbl_codigo.grid(row=0, column=0, sticky="w", pady=4)
        self.txt_codigo = ttk.Entry(form_frame, font=("Segoe UI", 10))
        self.txt_codigo.grid(row=0, column=1, sticky="ew", pady=4)

        lbl_nombre = ttk.Label(form_frame, text="Nombre:")
        lbl_nombre.grid(row=1, column=0, sticky="w", pady=4)
        self.txt_nombre = ttk.Entry(form_frame, font=("Segoe UI", 10))
        self.txt_nombre.grid(row=1, column=1, sticky="ew", pady=4)

        lbl_categoria = ttk.Label(form_frame, text="Categoría:")
        lbl_categoria.grid(row=2, column=0, sticky="w", pady=4)
        self.cmb_categoria = ttk.Combobox(
            form_frame,
            values=[
                "Plato Fuerte",
                "Bebida",
                "Postre",
                "Entrada",
                "Acompañamiento",
            ],
            font=("Segoe UI", 10),
            state="readonly",
        )
        self.cmb_categoria.set("Plato Fuerte")
        self.cmb_categoria.grid(row=2, column=1, sticky="ew", pady=4)

        lbl_precio = ttk.Label(form_frame, text="Precio ($):")
        lbl_precio.grid(row=3, column=0, sticky="w", pady=4)
        self.txt_precio = ttk.Entry(form_frame, font=("Segoe UI", 10))
        self.txt_precio.grid(row=3, column=1, sticky="ew", pady=4)

        lbl_stock = ttk.Label(form_frame, text="Stock (uds):")
        lbl_stock.grid(row=4, column=0, sticky="w", pady=4)
        self.txt_stock = ttk.Spinbox(
            form_frame, from_=0, to=1000, font=("Segoe UI", 10)
        )
        self.txt_stock.set("0")
        self.txt_stock.grid(row=4, column=1, sticky="ew", pady=4)

        # Botones de Acción
        actions_frame = tk.Frame(form_frame, bg="#F3F4F6")
        actions_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(15, 5))
        actions_frame.columnconfigure((0, 1), weight=1)

        btn_registrar = tk.Button(
            actions_frame,
            text="➕ Registrar",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#16A34A",
            activebackground="#15803D",
            activeforeground="#FFFFFF",
            bd=0,
            padx=8,
            pady=6,
            cursor="hand2",
            command=self._on_registrar_producto,
        )
        btn_registrar.grid(row=0, column=0, sticky="ew", padx=2, pady=2)

        btn_cargar = tk.Button(
            actions_frame,
            text="🔍 Consultar",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#2563EB",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            bd=0,
            padx=8,
            pady=6,
            cursor="hand2",
            command=self._on_cargar_producto,
        )
        btn_cargar.grid(row=0, column=1, sticky="ew", padx=2, pady=2)

        btn_actualizar = tk.Button(
            actions_frame,
            text="✏️ Actualizar",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#D97706",
            activebackground="#B45309",
            activeforeground="#FFFFFF",
            bd=0,
            padx=8,
            pady=6,
            cursor="hand2",
            command=self._on_actualizar_producto,
        )
        btn_actualizar.grid(row=1, column=0, sticky="ew", padx=2, pady=2)

        btn_eliminar = tk.Button(
            actions_frame,
            text="🗑️ Eliminar",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#DC2626",
            activebackground="#B91C1C",
            activeforeground="#FFFFFF",
            bd=0,
            padx=8,
            pady=6,
            cursor="hand2",
            command=self._on_eliminar_producto,
        )
        btn_eliminar.grid(row=1, column=1, sticky="ew", padx=2, pady=2)

        btn_limpiar = tk.Button(
            actions_frame,
            text="🧹 Limpiar Campos",
            font=("Segoe UI", 9),
            fg="#374151",
            bg="#E5E7EB",
            activebackground="#D1D5DB",
            bd=0,
            padx=8,
            pady=5,
            cursor="hand2",
            command=self._limpiar_formulario,
        )
        btn_limpiar.grid(row=2, column=0, columnspan=2, sticky="ew", padx=2, pady=(4, 2))

        self.lbl_prod_feedback = tk.Label(
            form_frame,
            text="",
            font=("Segoe UI", 8, "bold"),
            fg="#16A34A",
            bg="#F3F4F6",
            wraplength=240,
            justify="center",
        )
        self.lbl_prod_feedback.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        # CONTENEDOR 2: Tabla de Presentación (Panel Derecho)
        table_frame = ttk.LabelFrame(
            frame_main, text=" 📦 Inventario Registrado ", padding=(10, 10)
        )
        table_frame.grid(row=1, column=1, sticky="nsew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tree_productos = ttk.Treeview(
            table_frame, columns=columnas, show="headings", height=12
        )

        self.tree_productos.heading("codigo", text="Código")
        self.tree_productos.heading("nombre", text="Nombre del Producto")
        self.tree_productos.heading("categoria", text="Categoría")
        self.tree_productos.heading("precio", text="Precio ($)")
        self.tree_productos.heading("stock", text="Stock (uds)")

        self.tree_productos.column("codigo", width=75, anchor="center")
        self.tree_productos.column("nombre", width=180, anchor="w")
        self.tree_productos.column("categoria", width=120, anchor="w")
        self.tree_productos.column("precio", width=85, anchor="e")
        self.tree_productos.column("stock", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree_productos.yview
        )
        self.tree_productos.configure(yscrollcommand=scrollbar.set)

        self.tree_productos.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree_productos.bind("<<TreeviewSelect>>", self._on_tree_select_producto)

        return frame_main

    # ------------------------------------------------------------------ #
    #  CONTROLADORES PRODUCTOS                                           #
    # ------------------------------------------------------------------ #
    def _on_registrar_producto(self) -> None:
        """Manejador para el botón Registrar Producto (➕)."""
        codigo = self.txt_codigo.get().strip()
        nombre = self.txt_nombre.get().strip()
        categoria = self.cmb_categoria.get().strip()
        precio_raw = self.txt_precio.get().strip()
        stock_raw = self.txt_stock.get().strip()

        if not codigo or not nombre or not categoria or not precio_raw or not stock_raw:
            self._mostrar_feedback_prod("⚠️ Por favor complete todos los campos del formulario.", es_error=True)
            return

        exito, msj = self._restaurante_servicio.registrar_producto(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio_val=precio_raw,
            stock_val=stock_raw,
        )

        if exito:
            self._mostrar_feedback_prod(f"✅ {msj}", es_error=False)
            self.actualizar_datos()
            self._limpiar_formulario(limpiar_feedback=False)
        else:
            self._mostrar_feedback_prod(f"❌ {msj}", es_error=True)

    def _on_cargar_producto(self) -> None:
        """Manejador para el botón Consultar / Cargar Producto (🔍)."""
        codigo = self.txt_codigo.get().strip()
        if not codigo:
            self._mostrar_feedback_prod("⚠️ Ingrese el código del producto a consultar.", es_error=True)
            return

        prod = self._restaurante_servicio.buscar_producto(codigo)
        if prod is not None:
            self.txt_codigo.delete(0, tk.END)
            self.txt_codigo.insert(0, prod.codigo)

            self.txt_nombre.delete(0, tk.END)
            self.txt_nombre.insert(0, prod.nombre)

            self.cmb_categoria.set(prod.categoria)

            self.txt_precio.delete(0, tk.END)
            self.txt_precio.insert(0, f"{prod.precio:.2f}")

            self.txt_stock.delete(0, tk.END)
            self.txt_stock.insert(0, str(prod.stock))

            self._mostrar_feedback_prod(f"🔍 Producto '{prod.codigo}' cargado en el formulario.", es_error=False)
        else:
            self._mostrar_feedback_prod(f"❌ No existe ningún producto con el código '{codigo}'.", es_error=True)

    def _on_actualizar_producto(self) -> None:
        """Manejador para el botón Actualizar Producto (✏️)."""
        codigo = self.txt_codigo.get().strip()
        nombre = self.txt_nombre.get().strip()
        categoria = self.cmb_categoria.get().strip()
        precio_raw = self.txt_precio.get().strip()
        stock_raw = self.txt_stock.get().strip()

        if not codigo:
            self._mostrar_feedback_prod("⚠️ Debe especificar el código del producto a actualizar.", es_error=True)
            return

        exito, msj = self._restaurante_servicio.actualizar_producto(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio_val=precio_raw,
            stock_val=stock_raw,
        )

        if exito:
            self._mostrar_feedback_prod(f"✅ {msj}", es_error=False)
            self.actualizar_datos()
        else:
            self._mostrar_feedback_prod(f"❌ {msj}", es_error=True)

    def _on_eliminar_producto(self) -> None:
        """Manejador para el botón Eliminar Producto (🗑️)."""
        codigo = self.txt_codigo.get().strip()
        if not codigo:
            self._mostrar_feedback_prod("⚠️ Ingrese el código del producto que desea eliminar.", es_error=True)
            return

        prod = self._restaurante_servicio.buscar_producto(codigo)
        if prod is None:
            self._mostrar_feedback_prod(f"❌ No existe el producto con código '{codigo}'.", es_error=True)
            return

        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el producto '{prod.nombre}' ({prod.codigo})?",
            parent=self,
        )
        if not respuesta:
            return

        exito, msj = self._restaurante_servicio.eliminar_producto(codigo)
        if exito:
            self._mostrar_feedback_prod(f"🗑️ {msj}", es_error=False)
            self.actualizar_datos()
            self._limpiar_formulario(limpiar_feedback=False)
        else:
            self._mostrar_feedback_prod(f"❌ {msj}", es_error=True)

    def _limpiar_formulario(self, limpiar_feedback: bool = True) -> None:
        """Restablece los campos del formulario de productos."""
        self.txt_codigo.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.cmb_categoria.set("Plato Fuerte")
        self.txt_precio.delete(0, tk.END)
        self.txt_stock.delete(0, tk.END)
        self.txt_stock.insert(0, "0")

        if limpiar_feedback:
            self.lbl_prod_feedback.config(text="")

    def _mostrar_feedback_prod(self, mensaje: str, es_error: bool = False) -> None:
        """Muestra un mensaje de resultado en el formulario de productos."""
        color = "#DC2626" if es_error else "#16A34A"
        self.lbl_prod_feedback.config(text=mensaje, fg=color)

    def _on_tree_select_producto(self, event: tk.Event) -> None:
        """Carga automáticamente el producto seleccionado en la tabla."""
        seleccion = self.tree_productos.selection()
        if not seleccion:
            return
        item_id = seleccion[0]
        valores = self.tree_productos.item(item_id, "values")
        if valores and len(valores) >= 5:
            cod = valores[0]
            self.txt_codigo.delete(0, tk.END)
            self.txt_codigo.insert(0, cod)
            self._on_cargar_producto()

    # ------------------------------------------------------------------ #
    #  Construcción de Sección: USUARIOS (Componentes + Contenedores)     #
    # ------------------------------------------------------------------ #
    def _crear_frame_usuarios(self, parent: tk.Widget) -> tk.Frame:
        """
        Construye la interfaz de gestión CRUD de usuarios utilizando contenedores
        (ttk.LabelFrame, tk.Frame) y componentes de formulario y visualización.
        """
        frame_main = tk.Frame(parent, bg="#F3F4F6")
        frame_main.rowconfigure(1, weight=1)
        frame_main.columnconfigure(0, weight=1)
        frame_main.columnconfigure(1, weight=2)

        # Tarjeta de resumen superior
        frame_cards = tk.Frame(frame_main, bg="#F3F4F6")
        frame_cards.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        self.lbl_card_total_usr = tk.Label(
            frame_cards,
            text="Total Usuarios Registrados: 0",
            font=("Segoe UI", 9, "bold"),
            fg="#6B21A8",
            bg="#F3E8FF",
            padx=12,
            pady=5,
            relief="solid",
            bd=1,
        )
        self.lbl_card_total_usr.pack(side="left")

        # CONTENEDOR 1: Formulario y Acciones CRUD de Usuario (Panel Izquierdo)
        form_frame = ttk.LabelFrame(
            frame_main, text=" 📝 Formulario de Usuario ", padding=(15, 12)
        )
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        form_frame.columnconfigure(1, weight=1)

        # Campos
        lbl_id = ttk.Label(form_frame, text="Cédula / ID:")
        lbl_id.grid(row=0, column=0, sticky="w", pady=6)
        self.txt_usr_id = ttk.Entry(form_frame, font=("Segoe UI", 10))
        self.txt_usr_id.grid(row=0, column=1, sticky="ew", pady=6)

        lbl_nombre = ttk.Label(form_frame, text="Nombre:")
        lbl_nombre.grid(row=1, column=0, sticky="w", pady=6)
        self.txt_usr_nombre = ttk.Entry(form_frame, font=("Segoe UI", 10))
        self.txt_usr_nombre.grid(row=1, column=1, sticky="ew", pady=6)

        lbl_correo = ttk.Label(form_frame, text="Correo:")
        lbl_correo.grid(row=2, column=0, sticky="w", pady=6)
        self.txt_usr_correo = ttk.Entry(form_frame, font=("Segoe UI", 10))
        self.txt_usr_correo.grid(row=2, column=1, sticky="ew", pady=6)

        # Botones de Acción
        actions_frame = tk.Frame(form_frame, bg="#F3F4F6")
        actions_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(15, 5))
        actions_frame.columnconfigure((0, 1), weight=1)

        btn_registrar = tk.Button(
            actions_frame,
            text="➕ Registrar",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#16A34A",
            activebackground="#15803D",
            activeforeground="#FFFFFF",
            bd=0,
            padx=8,
            pady=6,
            cursor="hand2",
            command=self._on_registrar_usuario,
        )
        btn_registrar.grid(row=0, column=0, sticky="ew", padx=2, pady=2)

        btn_cargar = tk.Button(
            actions_frame,
            text="🔍 Consultar",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#2563EB",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            bd=0,
            padx=8,
            pady=6,
            cursor="hand2",
            command=self._on_cargar_usuario,
        )
        btn_cargar.grid(row=0, column=1, sticky="ew", padx=2, pady=2)

        btn_actualizar = tk.Button(
            actions_frame,
            text="✏️ Actualizar",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#D97706",
            activebackground="#B45309",
            activeforeground="#FFFFFF",
            bd=0,
            padx=8,
            pady=6,
            cursor="hand2",
            command=self._on_actualizar_usuario,
        )
        btn_actualizar.grid(row=1, column=0, sticky="ew", padx=2, pady=2)

        btn_eliminar = tk.Button(
            actions_frame,
            text="🗑️ Eliminar",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#DC2626",
            activebackground="#B91C1C",
            activeforeground="#FFFFFF",
            bd=0,
            padx=8,
            pady=6,
            cursor="hand2",
            command=self._on_eliminar_usuario,
        )
        btn_eliminar.grid(row=1, column=1, sticky="ew", padx=2, pady=2)

        btn_limpiar = tk.Button(
            actions_frame,
            text="🧹 Limpiar Campos",
            font=("Segoe UI", 9),
            fg="#374151",
            bg="#E5E7EB",
            activebackground="#D1D5DB",
            bd=0,
            padx=8,
            pady=5,
            cursor="hand2",
            command=self._limpiar_formulario_usuario,
        )
        btn_limpiar.grid(row=2, column=0, columnspan=2, sticky="ew", padx=2, pady=(4, 2))

        self.lbl_usr_feedback = tk.Label(
            form_frame,
            text="",
            font=("Segoe UI", 8, "bold"),
            fg="#16A34A",
            bg="#F3F4F6",
            wraplength=240,
            justify="center",
        )
        self.lbl_usr_feedback.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        # CONTENEDOR 2: Tabla de Presentación de Usuarios (Panel Derecho)
        table_frame = ttk.LabelFrame(
            frame_main, text=" 👥 Usuarios Registrados ", padding=(10, 10)
        )
        table_frame.grid(row=1, column=1, sticky="nsew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columnas = ("identificacion", "nombre", "correo")
        self.tree_usuarios = ttk.Treeview(
            table_frame, columns=columnas, show="headings", height=12
        )

        self.tree_usuarios.heading("identificacion", text="Identificación / Cédula")
        self.tree_usuarios.heading("nombre", text="Nombre Completo")
        self.tree_usuarios.heading("correo", text="Correo Electrónico")

        self.tree_usuarios.column("identificacion", width=140, anchor="center")
        self.tree_usuarios.column("nombre", width=220, anchor="w")
        self.tree_usuarios.column("correo", width=220, anchor="w")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree_usuarios.yview
        )
        self.tree_usuarios.configure(yscrollcommand=scrollbar.set)

        self.tree_usuarios.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree_usuarios.bind("<<TreeviewSelect>>", self._on_tree_select_usuario)

        return frame_main

    # ------------------------------------------------------------------ #
    #  CONTROLADORES USUARIOS                                            #
    # ------------------------------------------------------------------ #
    def _on_registrar_usuario(self) -> None:
        """Manejador para el botón Registrar Usuario (➕)."""
        identificacion = self.txt_usr_id.get().strip()
        nombre = self.txt_usr_nombre.get().strip()
        correo = self.txt_usr_correo.get().strip()

        if not identificacion or not nombre or not correo:
            self._mostrar_feedback_usr("⚠️ Por favor complete todos los campos del usuario.", es_error=True)
            return

        exito, msj = self._restaurante_servicio.registrar_usuario(
            identificacion=identificacion,
            nombre=nombre,
            correo=correo,
        )

        if exito:
            self._mostrar_feedback_usr(f"✅ {msj}", es_error=False)
            self.actualizar_datos()
            self._limpiar_formulario_usuario(limpiar_feedback=False)
        else:
            self._mostrar_feedback_usr(f"❌ {msj}", es_error=True)

    def _on_cargar_usuario(self) -> None:
        """Manejador para el botón Consultar / Cargar Usuario (🔍)."""
        identificacion = self.txt_usr_id.get().strip()
        if not identificacion:
            self._mostrar_feedback_usr("⚠️ Ingrese la identificación del usuario a consultar.", es_error=True)
            return

        usr = self._restaurante_servicio.buscar_usuario(identificacion)
        if usr is not None:
            self.txt_usr_id.delete(0, tk.END)
            self.txt_usr_id.insert(0, usr.identificacion)

            self.txt_usr_nombre.delete(0, tk.END)
            self.txt_usr_nombre.insert(0, usr.nombre)

            self.txt_usr_correo.delete(0, tk.END)
            self.txt_usr_correo.insert(0, usr.correo)

            self._mostrar_feedback_usr(f"🔍 Usuario '{usr.identificacion}' cargado en el formulario.", es_error=False)
        else:
            self._mostrar_feedback_usr(f"❌ No existe ningún usuario con identificación '{identificacion}'.", es_error=True)

    def _on_actualizar_usuario(self) -> None:
        """Manejador para el botón Actualizar Usuario (✏️)."""
        identificacion = self.txt_usr_id.get().strip()
        nombre = self.txt_usr_nombre.get().strip()
        correo = self.txt_usr_correo.get().strip()

        if not identificacion:
            self._mostrar_feedback_usr("⚠️ Debe especificar la identificación del usuario a actualizar.", es_error=True)
            return

        exito, msj = self._restaurante_servicio.actualizar_usuario(
            identificacion=identificacion,
            nombre=nombre,
            correo=correo,
        )

        if exito:
            self._mostrar_feedback_usr(f"✅ {msj}", es_error=False)
            self.actualizar_datos()
        else:
            self._mostrar_feedback_usr(f"❌ {msj}", es_error=True)

    def _on_eliminar_usuario(self) -> None:
        """Manejador para el botón Eliminar Usuario (🗑️)."""
        identificacion = self.txt_usr_id.get().strip()
        if not identificacion:
            self._mostrar_feedback_usr("⚠️ Ingrese la identificación del usuario a eliminar.", es_error=True)
            return

        usr = self._restaurante_servicio.buscar_usuario(identificacion)
        if usr is None:
            self._mostrar_feedback_usr(f"❌ No existe el usuario con identificación '{identificacion}'.", es_error=True)
            return

        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar al usuario '{usr.nombre}' ({usr.identificacion})?",
            parent=self,
        )
        if not respuesta:
            return

        exito, msj = self._restaurante_servicio.eliminar_usuario(identificacion)
        if exito:
            self._mostrar_feedback_usr(f"🗑️ {msj}", es_error=False)
            self.actualizar_datos()
            self._limpiar_formulario_usuario(limpiar_feedback=False)
        else:
            self._mostrar_feedback_usr(f"❌ {msj}", es_error=True)

    def _limpiar_formulario_usuario(self, limpiar_feedback: bool = True) -> None:
        """Restablece los campos del formulario de usuarios."""
        self.txt_usr_id.delete(0, tk.END)
        self.txt_usr_nombre.delete(0, tk.END)
        self.txt_usr_correo.delete(0, tk.END)

        if limpiar_feedback:
            self.lbl_usr_feedback.config(text="")

    def _mostrar_feedback_usr(self, mensaje: str, es_error: bool = False) -> None:
        """Muestra un mensaje de resultado en el formulario de usuarios."""
        color = "#DC2626" if es_error else "#16A34A"
        self.lbl_usr_feedback.config(text=mensaje, fg=color)

    def _on_tree_select_usuario(self, event: tk.Event) -> None:
        """Carga automáticamente el usuario seleccionado en la tabla."""
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            return
        item_id = seleccion[0]
        valores = self.tree_usuarios.item(item_id, "values")
        if valores and len(valores) >= 3:
            ident = valores[0]
            self.txt_usr_id.delete(0, tk.END)
            self.txt_usr_id.insert(0, ident)
            self._on_cargar_usuario()

    # ------------------------------------------------------------------ #
    #  Construcción de Sección: VENTAS (Informativo Pendiente)           #
    # ------------------------------------------------------------------ #
    def _crear_frame_ventas(self, parent: tk.Widget) -> tk.Frame:
        """Crea la vista informativa del módulo de ventas."""
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
                "Esta funcionalidad se incorporará progresivamente en las próximas semanas.\n"
                "Actualmente la base gráfica de la Semana 14 gestiona Productos y Usuarios (CRUD completo)\n"
                "mediante formularios, contenedores Tkinter y persistencia en archivos JSON."
            ),
            font=("Segoe UI", 10),
            fg="#4B5563",
            bg="#FFFFFF",
            justify="center",
        )
        lbl_desc.pack()

        return frame

    # ------------------------------------------------------------------ #
    #  Carga y Refresco de Datos desde RestauranteServicio               #
    # ------------------------------------------------------------------ #
    def actualizar_datos(self) -> None:
        """
        Solicita la información a RestauranteServicio (NUNCA directamente desde archivos JSON)
        y actualiza las tablas ttk.Treeview y métricas de la interfaz.
        """
        # 1. Cargar Productos en Treeview
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

        # Actualizar tarjetas de métricas de productos
        total_p = self._restaurante_servicio.obtener_total_productos()
        total_s = self._restaurante_servicio.obtener_total_stock()
        self.lbl_card_total_prod.config(text=f"Total Productos: {total_p}")
        self.lbl_card_total_stock.config(text=f"Stock Total: {total_s} unidades")

        # 2. Cargar Usuarios en Treeview
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

        total_u = self._restaurante_servicio.obtener_total_usuarios()
        self.lbl_card_total_usr.config(text=f"Total Usuarios Registrados: {total_u}")
