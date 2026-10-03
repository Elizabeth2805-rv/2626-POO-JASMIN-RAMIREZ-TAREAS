# -*- coding: utf-8 -*-
# ui/main_view.py
# Semana 16 — Manejo de eventos en Tkinter (Evolución Restaurante App - Gestión de Usuarios)
#
# Principio SRP: Esta vista representa la interfaz principal del restaurante.
# En esta evolución de la Semana 16, se profundiza el manejo de eventos en Tkinter
# integrando <<TreeviewSelect>>, <Return>, <Escape> y <<ComboboxSelected>> sobre la
# sección de Gestión de Usuarios. Delega todas las validaciones y operaciones a RestauranteServicio.

import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional, List, Dict
from modelos.usuario import Usuario
from modelos.producto import Producto
from modelos.venta import Venta
from servicios.restaurante_servicio import RestauranteServicio


class MainView(tk.Frame):
    """
    Vista principal (Dashboard) del restaurante evolucionada para la Semana 16.

    Muestra:
    - Encabezado con logo de assets/, datos del usuario autenticado y su rol, y botón de cerrar sesión.
    - Menú de navegación lateral (Sidebar) con íconos integrados.
    - Sección de Productos con CRUD completo (Formulario + Botones + Treeview + JSON).
    - Sección de Usuarios con Gestión de Eventos completos:
      * <<TreeviewSelect>> -> Cargar datos del usuario en el formulario mediante RestauranteServicio.
      * <<ComboboxSelected>> -> Responder a la selección del rol.
      * <Return> -> Atajo de teclado para confirmar registro de usuario.
      * <Escape> -> Atajo de teclado para limpiar formulario y cancelar selección.
      * command= -> Botones Registrar, Consultar, Actualizar, Eliminar y Limpiar.
      * Control de acceso por rol Administrador.
      * Protección contra auto-eliminación de la cuenta en sesión.
    - Sección de Ventas activa.
    - Barra de Estado con retroalimentación visual de eventos en tiempo real.
    """

    def __init__(
        self,
        master: tk.Widget,
        restaurante_servicio: RestauranteServicio,
        usuario_actual: Usuario,
        on_logout: Callable[[], None],
        ruta_assets: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        Constructor de MainView.

        Args:
            master:               Contenedor principal Tkinter.
            restaurante_servicio: Instancia del servicio de negocio.
            usuario_actual:       Instancia del usuario actualmente autenticado.
            on_logout:            Callback para regresar a la pantalla de Login.
            ruta_assets:          Ruta a la carpeta de recursos visuales assets/.
        """
        super().__init__(master, bg="#F3F4F6", **kwargs)
        self._restaurante_servicio = restaurante_servicio
        self._usuario_actual = usuario_actual
        self._on_logout = on_logout
        self._ruta_assets = ruta_assets or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "assets"
        )

        # Referencias de imágenes de assets/
        self._imgs_assets: Dict[str, tk.PhotoImage] = {}
        self._cargar_recursos_assets()

        # Sección actualmente activa ('ventas', 'productos', 'usuarios')
        self._seccion_activa = "usuarios"

        # Mapas auxiliares para la selección en Comboboxes de Ventas
        self._mapa_usuarios_combo: Dict[str, str] = {}
        self._mapa_productos_combo: Dict[str, str] = {}

        self._crear_interfaz()
        self.actualizar_datos()

    def _cargar_recursos_assets(self) -> None:
        """Carga las imágenes PNG contenidas en assets/ para ser usadas en la interfaz."""
        nombres = ["logo.png", "app_icon.png", "icon_producto.png", "icon_usuario.png", "icon_venta.png"]
        for nombre in nombres:
            ruta = os.path.join(self._ruta_assets, nombre)
            if os.path.exists(ruta):
                try:
                    clave = os.path.splitext(nombre)[0]
                    self._imgs_assets[clave] = tk.PhotoImage(file=ruta)
                except Exception as e:
                    print(f"  [AVISO] No se pudo cargar imagen '{nombre}': {e}")

    def set_usuario_actual(self, usuario: Usuario) -> None:
        """Actualiza la referencia del usuario actual y refresca la interfaz."""
        self._usuario_actual = usuario
        self._lbl_usuario_info.config(
            text=f"👤 Sesión: {usuario.nombre} ({usuario.identificacion}) — [{usuario.rol}]"
        )
        self.actualizar_datos()

    def _crear_interfaz(self) -> None:
        """Construye la distribución por capas y contenedores de la vista principal."""
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        # ------------------------------------------------------------------ #
        #  1. Contenedor Superior (Header / Barra de Título con Logo)        #
        # ------------------------------------------------------------------ #
        header = tk.Frame(self, bg="#1E293B", pady=8, padx=20)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Contenedor logo + título
        header_left = tk.Frame(header, bg="#1E293B")
        header_left.pack(side="left")

        if "logo" in self._imgs_assets:
            lbl_logo = tk.Label(header_left, image=self._imgs_assets["logo"], bg="#1E293B")
            lbl_logo.pack(side="left", padx=(0, 10))

        lbl_app_title = tk.Label(
            header_left,
            text="Restaurante App — Eventos en Tkinter (Semana 16)",
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
            text=f"👤 Sesión: {self._usuario_actual.nombre} ({self._usuario_actual.identificacion}) — [{self._usuario_actual.rol}]",
            font=("Segoe UI", 10),
            fg="#94A3B8",
            bg="#1E293B",
        )
        self._lbl_usuario_info.pack(side="right", padx=15)

        # ------------------------------------------------------------------ #
        #  2. Contenedor Lateral (Sidebar / Menú de Navegación)             #
        # ------------------------------------------------------------------ #
        sidebar = tk.Frame(self, bg="#0F172A", width=220, padx=10, pady=15)
        sidebar.grid(row=1, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        lbl_nav_title = tk.Label(
            sidebar,
            text="NAVEGACIÓN DEL SISTEMA",
            font=("Segoe UI", 8, "bold"),
            fg="#64748B",
            bg="#0F172A",
            anchor="w",
        )
        lbl_nav_title.pack(fill="x", pady=(0, 10))

        self.btn_nav_usuarios = self._crear_boton_nav(
            sidebar,
            " 👥 Gestión Usuarios",
            lambda: self._cambiar_seccion("usuarios"),
            imagen=self._imgs_assets.get("icon_usuario"),
        )
        self.btn_nav_productos = self._crear_boton_nav(
            sidebar,
            " 📦 Gestión Productos",
            lambda: self._cambiar_seccion("productos"),
            imagen=self._imgs_assets.get("icon_producto"),
        )
        self.btn_nav_ventas = self._crear_boton_nav(
            sidebar,
            " 🛒 Registro de Ventas",
            lambda: self._cambiar_seccion("ventas"),
            imagen=self._imgs_assets.get("icon_venta"),
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
            text="👥 Gestión de Usuarios y Manejo de Eventos (Semana 16)",
            font=("Segoe UI", 14, "bold"),
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
        self.frame_usuarios = self._crear_frame_usuarios(self.container_vistas)
        self.frame_productos = self._crear_frame_productos(self.container_vistas)
        self.frame_ventas = self._crear_frame_ventas(self.container_vistas)

        # ------------------------------------------------------------------ #
        #  4. Contenedor de Estado (Statusbar)                               #
        # ------------------------------------------------------------------ #
        statusbar = tk.Frame(self, bg="#E2E8F0", height=25, padx=15, pady=3)
        statusbar.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.lbl_status = tk.Label(
            statusbar,
            text="🟢 Estado: Sistema listo | Eventos: <<TreeviewSelect>>, <Return>, <Escape>, <<ComboboxSelected>>, command=",
            font=("Segoe UI", 8),
            fg="#334155",
            bg="#E2E8F0",
        )
        self.lbl_status.pack(side="left")

        # Seleccionar por defecto la sección de Usuarios
        self._cambiar_seccion("usuarios")

    def _crear_boton_nav(
        self,
        parent: tk.Widget,
        texto: str,
        comando: Callable[[], None],
        imagen: Optional[tk.PhotoImage] = None,
    ) -> tk.Button:
        """Crea un botón de navegación estilizado para el sidebar."""
        btn = tk.Button(
            parent,
            text=texto,
            image=imagen if imagen else None,
            compound="left" if imagen else "none",
            font=("Segoe UI", 9, "bold"),
            fg="#94A3B8",
            bg="#0F172A",
            activebackground="#1E293B",
            activeforeground="#F8FAFC",
            bd=0,
            anchor="w",
            padx=10,
            pady=8,
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

        self.frame_ventas.grid_forget()
        self.frame_productos.grid_forget()
        self.frame_usuarios.grid_forget()

        if seccion == "usuarios":
            self.btn_nav_usuarios.config(bg="#1E293B", fg="#F8FAFC")
            self.lbl_seccion_titulo.config(text="👥 Gestión de Usuarios y Manejo de Eventos en Tkinter")
            self.frame_usuarios.grid(row=0, column=0, sticky="nsew")
        elif seccion == "productos":
            self.btn_nav_productos.config(bg="#1E293B", fg="#F8FAFC")
            self.lbl_seccion_titulo.config(text="📦 Gestión de Productos del Restaurante")
            self.frame_productos.grid(row=0, column=0, sticky="nsew")
        elif seccion == "ventas":
            self.btn_nav_ventas.config(bg="#1E293B", fg="#F8FAFC")
            self.lbl_seccion_titulo.config(text="🛒 Operación de Ventas (Manejo de Eventos)")
            self.frame_ventas.grid(row=0, column=0, sticky="nsew")

        # Refrescar listas al cambiar de pestaña
        self.actualizar_datos()

    # ------------------------------------------------------------------ #
    #  SECCIÓN: USUARIOS (Manejo de Eventos en Tkinter — Semana 16)       #
    # ------------------------------------------------------------------ #
    def _crear_frame_usuarios(self, parent: tk.Widget) -> tk.Frame:
        """
        Construye la interfaz de gestión de usuarios aplicando el manejo de eventos (Semana 16):
        - <<TreeviewSelect>> via bind() para cargar datos en el formulario desde el servicio.
        - <<ComboboxSelected>> via bind() para reaccionar al cambio de rol.
        - <Return> para confirmar registro desde campos del formulario.
        - <Escape> para limpiar el formulario y deseleccionar elementos de la tabla.
        - command= en los botones principales (Registrar, Consultar, Actualizar, Eliminar, Limpiar).
        - Control de acceso basado en el rol Administrador.
        - Protección contra eliminación accidental de la propia cuenta en sesión.
        """
        frame_main = tk.Frame(parent, bg="#F3F4F6")
        frame_main.rowconfigure(1, weight=1)
        frame_main.columnconfigure(0, weight=1)
        frame_main.columnconfigure(1, weight=2)

        # Tarjetas de resumen de usuarios
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
        self.lbl_card_total_usr.pack(side="left", padx=(0, 10))

        self.lbl_card_rol_sesion = tk.Label(
            frame_cards,
            text=f"Rol en Sesión: {self._usuario_actual.rol}",
            font=("Segoe UI", 9, "bold"),
            fg="#0369A1",
            bg="#E0F2FE",
            padx=12,
            pady=5,
            relief="solid",
            bd=1,
        )
        self.lbl_card_rol_sesion.pack(side="left")

        # Verificar si el usuario actual tiene permisos de Administrador
        es_admin = self._usuario_actual.rol.lower() == "administrador"

        # CONTENEDOR 1: Formulario de Usuario (Panel Izquierdo)
        form_frame = ttk.LabelFrame(
            frame_main, text=" 📝 Formulario de Usuario ", padding=(15, 12)
        )
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        form_frame.columnconfigure(1, weight=1)

        row_idx = 0
        if not es_admin:
            lbl_restriccion = tk.Label(
                form_frame,
                text="⚠️ ACCESO RESTRINGIDO:\nSolo el Administrador puede registrar, actualizar o eliminar usuarios. Puede consultar la tabla.",
                font=("Segoe UI", 8, "bold"),
                fg="#B91C1C",
                bg="#FEE2E2",
                padx=8,
                pady=6,
                relief="solid",
                bd=1,
                justify="center",
                wraplength=230,
            )
            lbl_restriccion.grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=(0, 10))
            row_idx += 1
        else:
            lbl_event_info = tk.Label(
                form_frame,
                text="💡 Eventos: <Return> (Registrar) | <Escape> (Limpiar) | <<ComboboxSelected>> (Rol) | <<TreeviewSelect>> (Selección)",
                font=("Segoe UI", 8, "italic"),
                fg="#374151",
                bg="#E5E7EB",
                padx=6,
                pady=4,
                relief="flat",
                wraplength=230,
                justify="center",
            )
            lbl_event_info.grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=(0, 10))
            row_idx += 1

        lbl_id = ttk.Label(form_frame, text="Cédula / ID:")
        lbl_id.grid(row=row_idx, column=0, sticky="w", pady=5)
        self.txt_usr_id = ttk.Entry(form_frame, font=("Segoe UI", 10))
        self.txt_usr_id.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        lbl_nombre = ttk.Label(form_frame, text="Nombre:")
        lbl_nombre.grid(row=row_idx, column=0, sticky="w", pady=5)
        self.txt_usr_nombre = ttk.Entry(form_frame, font=("Segoe UI", 10))
        self.txt_usr_nombre.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        lbl_correo = ttk.Label(form_frame, text="Correo:")
        lbl_correo.grid(row=row_idx, column=0, sticky="w", pady=5)
        self.txt_usr_correo = ttk.Entry(form_frame, font=("Segoe UI", 10))
        self.txt_usr_correo.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        lbl_rol = ttk.Label(form_frame, text="Rol de Usuario:")
        lbl_rol.grid(row=row_idx, column=0, sticky="w", pady=5)
        self.cmb_usr_rol = ttk.Combobox(
            form_frame,
            values=["Administrador", "Empleado", "Cliente"],
            font=("Segoe UI", 10),
            state="readonly" if es_admin else "disabled",
        )
        self.cmb_usr_rol.set("Cliente")
        self.cmb_usr_rol.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        # Evento virtual ComboboxSelected sobre el Combobox de rol
        self.cmb_usr_rol.bind("<<ComboboxSelected>>", self._on_combobox_rol_selected)

        # Enlazar atajos de teclado <Return> y <Escape> a los campos del formulario
        for widget in (self.txt_usr_id, self.txt_usr_nombre, self.txt_usr_correo, self.cmb_usr_rol):
            widget.bind("<Return>", lambda e: self._on_registrar_usuario() if es_admin else None)
            widget.bind("<Escape>", lambda e: self._limpiar_formulario_usuario())

        actions_frame = tk.Frame(form_frame, bg="#F3F4F6")
        actions_frame.grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=(15, 5))
        actions_frame.columnconfigure((0, 1), weight=1)
        row_idx += 1

        estado_btn = "normal" if es_admin else "disabled"

        self.btn_usr_registrar = tk.Button(
            actions_frame,
            text="➕ Registrar",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#16A34A" if es_admin else "#9CA3AF",
            activebackground="#15803D",
            activeforeground="#FFFFFF",
            bd=0,
            padx=8,
            pady=6,
            cursor="hand2" if es_admin else "arrow",
            state=estado_btn,
            command=self._on_registrar_usuario,
        )
        self.btn_usr_registrar.grid(row=0, column=0, sticky="ew", padx=2, pady=2)

        self.btn_usr_cargar = tk.Button(
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
        self.btn_usr_cargar.grid(row=0, column=1, sticky="ew", padx=2, pady=2)

        self.btn_usr_actualizar = tk.Button(
            actions_frame,
            text="✏️ Actualizar",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#D97706" if es_admin else "#9CA3AF",
            activebackground="#B45309",
            activeforeground="#FFFFFF",
            bd=0,
            padx=8,
            pady=6,
            cursor="hand2" if es_admin else "arrow",
            state=estado_btn,
            command=self._on_actualizar_usuario,
        )
        self.btn_usr_actualizar.grid(row=1, column=0, sticky="ew", padx=2, pady=2)

        self.btn_usr_eliminar = tk.Button(
            actions_frame,
            text="🗑️ Eliminar",
            font=("Segoe UI", 9, "bold"),
            fg="#FFFFFF",
            bg="#DC2626" if es_admin else "#9CA3AF",
            activebackground="#B91C1C",
            activeforeground="#FFFFFF",
            bd=0,
            padx=8,
            pady=6,
            cursor="hand2" if es_admin else "arrow",
            state=estado_btn,
            command=self._on_eliminar_usuario,
        )
        self.btn_usr_eliminar.grid(row=1, column=1, sticky="ew", padx=2, pady=2)

        self.btn_usr_limpiar = tk.Button(
            actions_frame,
            text="🧹 Limpiar (<Escape>)",
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
        self.btn_usr_limpiar.grid(row=2, column=0, columnspan=2, sticky="ew", padx=2, pady=(4, 2))

        self.lbl_usr_feedback = tk.Label(
            form_frame,
            text="",
            font=("Segoe UI", 8, "bold"),
            fg="#16A34A",
            bg="#F3F4F6",
            wraplength=240,
            justify="center",
        )
        self.lbl_usr_feedback.grid(row=row_idx, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        # CONTENEDOR 2: Tabla Treeview de Usuarios (Panel Derecho)
        table_frame = ttk.LabelFrame(
            frame_main, text=" 👥 Usuarios Registrados (Tabla Treeview) ", padding=(10, 10)
        )
        table_frame.grid(row=1, column=1, sticky="nsew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columnas = ("identificacion", "nombre", "correo", "rol")
        self.tree_usuarios = ttk.Treeview(
            table_frame, columns=columnas, show="headings", height=12
        )

        self.tree_usuarios.heading("identificacion", text="Identificación / Cédula")
        self.tree_usuarios.heading("nombre", text="Nombre Completo")
        self.tree_usuarios.heading("correo", text="Correo Electrónico")
        self.tree_usuarios.heading("rol", text="Rol del Usuario")

        self.tree_usuarios.column("identificacion", width=120, anchor="center")
        self.tree_usuarios.column("nombre", width=190, anchor="w")
        self.tree_usuarios.column("correo", width=190, anchor="w")
        self.tree_usuarios.column("rol", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree_usuarios.yview
        )
        self.tree_usuarios.configure(yscrollcommand=scrollbar.set)

        self.tree_usuarios.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Evento <<TreeviewSelect>> mediante bind()
        self.tree_usuarios.bind("<<TreeviewSelect>>", self._on_tree_select_usuario)
        self.tree_usuarios.bind("<Escape>", lambda e: self._limpiar_formulario_usuario())

        return frame_main

    # ------------------------------------------------------------------ #
    #  CONTROLADORES Y MANEJADORES DE EVENTOS DE USUARIOS (SEMANA 16)    #
    # ------------------------------------------------------------------ #
    def _on_combobox_rol_selected(self, event: Optional[tk.Event] = None) -> None:
        """
        Callback ejecutado por el evento virtual <<ComboboxSelected>>.
        Responde visualmente a la selección del rol en el formulario.
        """
        rol_seleccionado = self.cmb_usr_rol.get().strip()
        self.lbl_status.config(
            text=f"🔵 Evento <<ComboboxSelected>>: Rol seleccionado en combobox -> '{rol_seleccionado}'"
        )
        self._mostrar_feedback_usr(
            f"ℹ️ Rol asignado en formulario: {rol_seleccionado}", es_error=False
        )

    def _on_registrar_usuario(self) -> None:
        """
        Callback ejecutado por:
        - Botón Registrar (command=).
        - Atajo de teclado <Return> (bind()).
        Reutiliza el servicio de negocio evitando duplicación de código.
        """
        if self._usuario_actual.rol.lower() != "administrador":
            messagebox.showerror(
                "Permiso Denegado",
                "Únicamente los usuarios con rol Administrador pueden registrar nuevos usuarios.",
                parent=self,
            )
            return

        identificacion = self.txt_usr_id.get().strip()
        nombre = self.txt_usr_nombre.get().strip()
        correo = self.txt_usr_correo.get().strip()
        rol = self.cmb_usr_rol.get().strip()

        if not identificacion or not nombre or not correo or not rol:
            self._mostrar_feedback_usr(
                "⚠️ Por favor complete todos los campos del usuario (ID, Nombre, Correo y Rol).",
                es_error=True,
            )
            return

        exito, msj = self._restaurante_servicio.registrar_usuario(
            identificacion=identificacion,
            nombre=nombre,
            correo=correo,
            rol=rol,
        )

        if exito:
            self._mostrar_feedback_usr(f"✅ {msj}", es_error=False)
            self.lbl_status.config(
                text=f"🟢 Usuario registrado mediante evento -> Persistencia en usuarios.json | {msj}"
            )
            self.actualizar_datos()
            self._limpiar_formulario_usuario(limpiar_feedback=False)
        else:
            self._mostrar_feedback_usr(f"❌ {msj}", es_error=True)
            self.lbl_status.config(text=f"⚠️ Error al registrar usuario: {msj}")

    def _on_cargar_usuario(self) -> None:
        """Manejador para consultar un usuario por su ID en el formulario."""
        identificacion = self.txt_usr_id.get().strip()
        if not identificacion:
            self._mostrar_feedback_usr(
                "⚠️ Ingrese la identificación del usuario a consultar.", es_error=True
            )
            return

        usr = self._restaurante_servicio.buscar_usuario(identificacion)
        if usr is not None:
            self.txt_usr_id.delete(0, tk.END)
            self.txt_usr_id.insert(0, usr.identificacion)

            self.txt_usr_nombre.delete(0, tk.END)
            self.txt_usr_nombre.insert(0, usr.nombre)

            self.txt_usr_correo.delete(0, tk.END)
            self.txt_usr_correo.insert(0, usr.correo)

            self.cmb_usr_rol.set(usr.rol)

            self._mostrar_feedback_usr(
                f"🔍 Usuario '{usr.identificacion}' cargado desde RestauranteServicio.",
                es_error=False,
            )
            self.lbl_status.config(
                text=f"🟢 Usuario encontrado en servicio: {usr.nombre} ({usr.rol})"
            )
        else:
            self._mostrar_feedback_usr(
                f"❌ No existe ningún usuario con identificación '{identificacion}'.",
                es_error=True,
            )

    def _on_actualizar_usuario(self) -> None:
        """Manejador para actualizar los datos de un usuario existente."""
        if self._usuario_actual.rol.lower() != "administrador":
            messagebox.showerror(
                "Permiso Denegado",
                "Únicamente los usuarios con rol Administrador pueden actualizar usuarios.",
                parent=self,
            )
            return

        identificacion = self.txt_usr_id.get().strip()
        nombre = self.txt_usr_nombre.get().strip()
        correo = self.txt_usr_correo.get().strip()
        rol = self.cmb_usr_rol.get().strip()

        if not identificacion:
            self._mostrar_feedback_usr(
                "⚠️ Debe especificar la identificación del usuario a actualizar.",
                es_error=True,
            )
            return

        exito, msj = self._restaurante_servicio.actualizar_usuario(
            identificacion=identificacion,
            nombre=nombre,
            correo=correo,
            rol=rol,
        )

        if exito:
            self._mostrar_feedback_usr(f"✅ {msj}", es_error=False)
            self.lbl_status.config(
                text=f"🟢 Usuario actualizado -> Persistencia en usuarios.json | {msj}"
            )
            self.actualizar_datos()
        else:
            self._mostrar_feedback_usr(f"❌ {msj}", es_error=True)

    def _on_eliminar_usuario(self) -> None:
        """
        Manejador para el botón Eliminar Usuario (🗑️).
        Incluye validación de seguridad para evitar que la cuenta actualmente en sesión se elimine.
        """
        if self._usuario_actual.rol.lower() != "administrador":
            messagebox.showerror(
                "Permiso Denegado",
                "Únicamente los usuarios con rol Administrador pueden eliminar usuarios.",
                parent=self,
            )
            return

        identificacion = self.txt_usr_id.get().strip()
        if not identificacion:
            self._mostrar_feedback_usr(
                "⚠️ Ingrese la identificación del usuario a eliminar.", es_error=True
            )
            return

        # Protección contra auto-eliminación de la cuenta en sesión activa
        if identificacion.lower() == self._usuario_actual.identificacion.lower():
            self._mostrar_feedback_usr(
                "⚠️ No puede eliminar su propia cuenta actualmente autenticada.",
                es_error=True,
            )
            messagebox.showwarning(
                "Acción Denegada",
                "No está permitido eliminar la cuenta del administrador que tiene la sesión activa.",
                parent=self,
            )
            return

        usr = self._restaurante_servicio.buscar_usuario(identificacion)
        if usr is None:
            self._mostrar_feedback_usr(
                f"❌ No existe el usuario con identificación '{identificacion}'.",
                es_error=True,
            )
            return

        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar al usuario '{usr.nombre}' ({usr.identificacion} - Rol: {usr.rol})?",
            parent=self,
        )
        if not respuesta:
            return

        exito, msj = self._restaurante_servicio.eliminar_usuario(identificacion)
        if exito:
            self._mostrar_feedback_usr(f"🗑️ {msj}", es_error=False)
            self.lbl_status.config(
                text=f"🟢 Usuario eliminado -> Persistencia en usuarios.json | {msj}"
            )
            self.actualizar_datos()
            self._limpiar_formulario_usuario(limpiar_feedback=False)
        else:
            self._mostrar_feedback_usr(f"❌ {msj}", es_error=True)

    def _limpiar_formulario_usuario(self, limpiar_feedback: bool = True) -> None:
        """
        Callback para el evento <Escape> y botón Limpiar (command=).
        Limpia los campos del formulario, deselecciona filas del Treeview y restablece el foco.
        """
        self.txt_usr_id.delete(0, tk.END)
        self.txt_usr_nombre.delete(0, tk.END)
        self.txt_usr_correo.delete(0, tk.END)
        self.cmb_usr_rol.set("Cliente")

        if hasattr(self, "tree_usuarios"):
            seleccion = self.tree_usuarios.selection()
            if seleccion:
                self.tree_usuarios.selection_remove(seleccion)

        if limpiar_feedback:
            self.lbl_usr_feedback.config(text="")

        self.txt_usr_id.focus_set()
        self.lbl_status.config(
            text="🟢 Formulario de usuario restablecido a estado inicial (<Escape>)"
        )

    def _mostrar_feedback_usr(self, mensaje: str, es_error: bool = False) -> None:
        """Muestra un mensaje de resultado en el formulario de usuarios."""
        color = "#DC2626" if es_error else "#16A34A"
        self.lbl_usr_feedback.config(text=mensaje, fg=color)

    def _on_tree_select_usuario(self, event: Optional[tk.Event] = None) -> None:
        """
        Callback ejecutado por el evento virtual <<TreeviewSelect>> al hacer clic en una fila de usuarios.
        Recupera el identificador de la fila seleccionada y busca el objeto en RestauranteServicio.
        Evita guardar información sensible directamente en la tabla.
        """
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            return
        item_id = seleccion[0]
        valores = self.tree_usuarios.item(item_id, "values")
        if valores and len(valores) >= 1:
            ident = valores[0]
            # Consultar objeto Usuario mediante el servicio
            usr = self._restaurante_servicio.buscar_usuario(ident)
            if usr is not None:
                self.txt_usr_id.delete(0, tk.END)
                self.txt_usr_id.insert(0, usr.identificacion)

                self.txt_usr_nombre.delete(0, tk.END)
                self.txt_usr_nombre.insert(0, usr.nombre)

                self.txt_usr_correo.delete(0, tk.END)
                self.txt_usr_correo.insert(0, usr.correo)

                self.cmb_usr_rol.set(usr.rol)

                self._mostrar_feedback_usr(
                    f"📋 Evento <<TreeviewSelect>>: Datos de '{usr.nombre}' ({usr.rol}) cargados.",
                    es_error=False,
                )
                self.lbl_status.config(
                    text=f"🔵 Evento <<TreeviewSelect>> -> Usuario '{usr.identificacion}' recuperado del servicio"
                )

    # ------------------------------------------------------------------ #
    #  SECCIÓN: VENTAS (Manejo de Eventos)                               #
    # ------------------------------------------------------------------ #
    def _crear_frame_ventas(self, parent: tk.Widget) -> tk.Frame:
        """
        Construye la vista interactiva del Módulo de Ventas demostrando el fundamento de eventos:
        Selección Usuario + Selección Producto -> Botón command= -> Callback -> Servicio -> Persistencia -> UI.
        """
        frame_main = tk.Frame(parent, bg="#F3F4F6")
        frame_main.rowconfigure(1, weight=1)
        frame_main.columnconfigure(0, weight=1)
        frame_main.columnconfigure(1, weight=2)

        # Tarjetas de resumen de ventas
        frame_cards = tk.Frame(frame_main, bg="#F3F4F6")
        frame_cards.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        self.lbl_card_total_ventas = tk.Label(
            frame_cards,
            text="Ventas Registradas: 0",
            font=("Segoe UI", 9, "bold"),
            fg="#065F46",
            bg="#D1FAE5",
            padx=12,
            pady=5,
            relief="solid",
            bd=1,
        )
        self.lbl_card_total_ventas.pack(side="left", padx=(0, 10))

        self.lbl_card_monto_ventas = tk.Label(
            frame_cards,
            text="Recaudación Total: $0.00",
            font=("Segoe UI", 9, "bold"),
            fg="#1E40AF",
            bg="#DBEAFE",
            padx=12,
            pady=5,
            relief="solid",
            bd=1,
        )
        self.lbl_card_monto_ventas.pack(side="left")

        # CONTENEDOR 1: Formulario de Operación de Venta (Panel Izquierdo)
        form_frame = ttk.LabelFrame(
            frame_main, text=" 🛒 Registrar Nueva Venta ", padding=(15, 12)
        )
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        form_frame.columnconfigure(0, weight=1)

        # Explicación de Fundamentos de Eventos
        lbl_info = tk.Label(
            form_frame,
            text=(
                "💡 Fundamento de Eventos:\n"
                "Seleccione un usuario y un producto. El botón invoca el callback mediante "
                "command=, el cual delega la operación a RestauranteServicio."
            ),
            font=("Segoe UI", 8, "italic"),
            fg="#4B5563",
            bg="#F9FAFB",
            padx=8,
            pady=6,
            relief="groove",
            bd=1,
            justify="left",
            wraplength=230,
        )
        lbl_info.pack(fill="x", pady=(0, 12))

        # Seleccionar Usuario
        lbl_usr = ttk.Label(form_frame, text="1. Seleccionar Usuario / Cliente:")
        lbl_usr.pack(anchor="w", pady=(4, 2))

        self.cmb_usuario_venta = ttk.Combobox(
            form_frame, font=("Segoe UI", 10), state="readonly"
        )
        self.cmb_usuario_venta.pack(fill="x", pady=(0, 12))

        # Seleccionar Producto
        lbl_prod = ttk.Label(form_frame, text="2. Seleccionar Producto:")
        lbl_prod.pack(anchor="w", pady=(4, 2))

        self.cmb_producto_venta = ttk.Combobox(
            form_frame, font=("Segoe UI", 10), state="readonly"
        )
        self.cmb_producto_venta.pack(fill="x", pady=(0, 15))

        # BOTÓN PRINCIPAL DE VENTA (Se utiliza command=self._on_registrar_venta como callback)
        btn_registrar_venta = tk.Button(
            form_frame,
            text="🛍️ Registrar Venta (command=)",
            font=("Segoe UI", 10, "bold"),
            fg="#FFFFFF",
            bg="#16A34A",
            activebackground="#15803D",
            activeforeground="#FFFFFF",
            bd=0,
            padx=10,
            pady=10,
            cursor="hand2",
            command=self._on_registrar_venta,
        )
        btn_registrar_venta.pack(fill="x", pady=(5, 10))

        # Etiqueta para retroalimentación visual del callback
        self.lbl_venta_feedback = tk.Label(
            form_frame,
            text="",
            font=("Segoe UI", 8, "bold"),
            fg="#16A34A",
            bg="#F3F4F6",
            wraplength=230,
            justify="center",
        )
        self.lbl_venta_feedback.pack(fill="x", pady=(5, 0))

        # CONTENEDOR 2: Tabla de Ventas Registradas (Panel Derecho)
        table_frame = ttk.LabelFrame(
            frame_main, text=" 📜 Historial de Ventas Registradas ", padding=(10, 10)
        )
        table_frame.grid(row=1, column=1, sticky="nsew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columnas = ("id_venta", "fecha", "usuario", "producto", "total")
        self.tree_ventas = ttk.Treeview(
            table_frame, columns=columnas, show="headings", height=12
        )

        self.tree_ventas.heading("id_venta", text="ID Venta")
        self.tree_ventas.heading("fecha", text="Fecha y Hora")
        self.tree_ventas.heading("usuario", text="Cliente / Usuario")
        self.tree_ventas.heading("producto", text="Producto Adquirido")
        self.tree_ventas.heading("total", text="Total ($)")

        self.tree_ventas.column("id_venta", width=70, anchor="center")
        self.tree_ventas.column("fecha", width=140, anchor="center")
        self.tree_ventas.column("usuario", width=160, anchor="w")
        self.tree_ventas.column("producto", width=170, anchor="w")
        self.tree_ventas.column("total", width=80, anchor="e")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree_ventas.yview
        )
        self.tree_ventas.configure(yscrollcommand=scrollbar.set)

        self.tree_ventas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        return frame_main

    # ------------------------------------------------------------------ #
    #  CALLBACK DE VENTA                                                 #
    # ------------------------------------------------------------------ #
    def _on_registrar_venta(self) -> None:
        """
        CALLBACK activado por el evento de clic en el botón 'Registrar Venta' (command=).
        """
        sel_usr_str = self.cmb_usuario_venta.get().strip()
        sel_prod_str = self.cmb_producto_venta.get().strip()

        if not sel_usr_str or not sel_prod_str:
            self._mostrar_feedback_venta(
                "⚠️ Seleccione un usuario y un producto para registrar la venta.",
                es_error=True,
            )
            return

        id_usuario = self._mapa_usuarios_combo.get(sel_usr_str)
        cod_producto = self._mapa_productos_combo.get(sel_prod_str)

        if not id_usuario or not cod_producto:
            self._mostrar_feedback_venta(
                "❌ Error de mapeo en los datos seleccionados.", es_error=True
            )
            return

        exito, msj = self._restaurante_servicio.registrar_venta(
            identificacion_usuario=id_usuario,
            codigo_producto=cod_producto,
        )

        if exito:
            self._mostrar_feedback_venta(f"✅ {msj}", es_error=False)
            self.lbl_status.config(
                text=f"🟢 Venta realizada con éxito | Persistencia en ventas.json | {msj}"
            )
            self.actualizar_datos()
            messagebox.showinfo(
                "Venta Exitosa",
                f"Operación coordinada con éxito mediante callback (command=):\n\n{msj}",
                parent=self,
            )
        else:
            self._mostrar_feedback_venta(f"❌ {msj}", es_error=True)
            self.lbl_status.config(text=f"⚠️ Fallo al registrar venta: {msj}")
            messagebox.showwarning("Venta Rechazada", msj, parent=self)

    def _mostrar_feedback_venta(self, mensaje: str, es_error: bool = False) -> None:
        """Muestra una respuesta visual en la sección de ventas."""
        color = "#DC2626" if es_error else "#16A34A"
        self.lbl_venta_feedback.config(text=mensaje, fg=color)

    # ------------------------------------------------------------------ #
    #  SECCIÓN: PRODUCTOS (Componentes + Contenedores)                   #
    # ------------------------------------------------------------------ #
    def _crear_frame_productos(self, parent: tk.Widget) -> tk.Frame:
        """Construye la interfaz de gestión de productos."""
        frame_main = tk.Frame(parent, bg="#F3F4F6")
        frame_main.rowconfigure(1, weight=1)
        frame_main.columnconfigure(0, weight=1)
        frame_main.columnconfigure(1, weight=2)

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

        form_frame = ttk.LabelFrame(
            frame_main, text=" 📝 Formulario de Producto ", padding=(15, 12)
        )
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        form_frame.columnconfigure(1, weight=1)

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
    #  Carga y Refresco de Datos desde RestauranteServicio               #
    # ------------------------------------------------------------------ #
    def actualizar_datos(self) -> None:
        """
        Solicita la información a RestauranteServicio (NUNCA directamente desde archivos JSON)
        y actualiza las tablas ttk.Treeview, comboboxes y métricas de la interfaz.
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
                    usr.rol,
                ),
            )

        total_u = self._restaurante_servicio.obtener_total_usuarios()
        self.lbl_card_total_usr.config(text=f"Total Usuarios Registrados: {total_u}")

        # 3. Cargar Ventas en Treeview
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)

        ventas = self._restaurante_servicio.obtener_ventas()
        for vta in ventas:
            usr_obj = self._restaurante_servicio.buscar_usuario(vta.identificacion_usuario)
            prod_obj = self._restaurante_servicio.buscar_producto(vta.codigo_producto)

            usr_nombre = usr_obj.nombre if usr_obj else vta.identificacion_usuario
            prod_nombre = prod_obj.nombre if prod_obj else vta.codigo_producto

            self.tree_ventas.insert(
                "",
                "end",
                values=(
                    vta.id_venta,
                    vta.fecha,
                    f"{vta.identificacion_usuario} - {usr_nombre}",
                    f"{vta.codigo_producto} - {prod_nombre}",
                    f"${vta.total:.2f}",
                ),
            )

        total_v = self._restaurante_servicio.obtener_total_ventas()
        monto_v = self._restaurante_servicio.obtener_monto_total_ventas()
        self.lbl_card_total_ventas.config(text=f"Ventas Registradas: {total_v}")
        self.lbl_card_monto_ventas.config(text=f"Recaudación Total: ${monto_v:.2f}")

        # 4. Actualizar las opciones en los Comboboxes de Ventas
        self._actualizar_comboboxes_ventas(usuarios, productos)

    def _actualizar_comboboxes_ventas(
        self, usuarios: List[Usuario], productos: List[Producto]
    ) -> None:
        """Refresca las opciones seleccionables en los Comboboxes de la sección Ventas."""
        self._mapa_usuarios_combo.clear()
        opciones_usuarios = []
        for u in usuarios:
            label = f"{u.identificacion} — {u.nombre} [{u.rol}]"
            opciones_usuarios.append(label)
            self._mapa_usuarios_combo[label] = u.identificacion

        self.cmb_usuario_venta["values"] = opciones_usuarios
        if opciones_usuarios and not self.cmb_usuario_venta.get():
            self.cmb_usuario_venta.current(0)

        self._mapa_productos_combo.clear()
        opciones_productos = []
        for p in productos:
            estado_stock = f"Stock: {p.stock}" if p.stock > 0 else "SIN STOCK"
            label = f"{p.codigo} — {p.nombre} (${p.precio:.2f}) [{estado_stock}]"
            opciones_productos.append(label)
            self._mapa_productos_combo[label] = p.codigo

        self.cmb_producto_venta["values"] = opciones_productos
        if opciones_productos and not self.cmb_producto_venta.get():
            self.cmb_producto_venta.current(0)
