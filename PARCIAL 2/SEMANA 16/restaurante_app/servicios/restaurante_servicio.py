# -*- coding: utf-8 -*-
# servicios/restaurante_servicio.py
# Semana 15 — Conceptos fundamentales de manejo de eventos (Evolución Restaurante App)
#
# Principio SRP: Esta clase encapsula la lógica de negocio del restaurante,
# coordinando el modelo de datos (Producto, Usuario, Venta) y la persistencia (ArchivoServicio).
# Concentra la validación de negocio y operaciones de gestión de productos, usuarios y ventas.

from datetime import datetime
from typing import List, Optional, Tuple, Any
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """
    Servicio principal que gestiona las operaciones de negocio del restaurante.

    Mantiene colecciones en memoria de objetos Producto, Usuario y Venta, proporcionando
    métodos para consultar información, autenticar acceso y coordinar operaciones de
    negocio con persistencia inmediata en archivos JSON.
    """

    def __init__(
        self,
        archivo_servicio: Optional[ArchivoServicio] = None,
        ruta_productos: str = "datos/productos.json",
        ruta_usuarios: str = "datos/usuarios.json",
        ruta_ventas: str = "datos/ventas.json",
    ) -> None:
        """
        Constructor del servicio de restaurante.

        Args:
            archivo_servicio: Instancia del servicio de archivos (I/O).
            ruta_productos:   Ruta al archivo productos.json.
            ruta_usuarios:    Ruta al archivo usuarios.json.
            ruta_ventas:      Ruta al archivo ventas.json.
        """
        self._archivo_servicio = archivo_servicio or ArchivoServicio()
        self._ruta_productos = ruta_productos
        self._ruta_usuarios = ruta_usuarios
        self._ruta_ventas = ruta_ventas

        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []
        self._ventas: List[Venta] = []

        # Cargar datos al instanciar el servicio
        self.cargar_datos_iniciales()

    @property
    def productos(self) -> List[Producto]:
        """Retorna la lista de objetos Producto registrados."""
        return self._productos

    @property
    def usuarios(self) -> List[Usuario]:
        """Retorna la lista de objetos Usuario registrados."""
        return self._usuarios

    @property
    def ventas(self) -> List[Venta]:
        """Retorna la lista de objetos Venta registrados."""
        return self._ventas

    def cargar_datos_iniciales(self) -> None:
        """
        Lee las estructuras JSON desde ArchivoServicio y las transforma
        en instancias de objetos de los modelos Producto, Usuario y Venta.
        """
        # Cargar Productos
        raw_productos = self._archivo_servicio.cargar_productos(self._ruta_productos)
        self._productos = []
        for p_dict in raw_productos:
            try:
                prod = Producto.from_dict(p_dict)
                self._productos.append(prod)
            except (KeyError, ValueError) as err:
                print(f"  [AVISO] Error al reconstruir producto: {err}")

        # Cargar Usuarios
        raw_usuarios = self._archivo_servicio.cargar_usuarios(self._ruta_usuarios)
        self._usuarios = []
        for u_dict in raw_usuarios:
            try:
                usr = Usuario.from_dict(u_dict)
                self._usuarios.append(usr)
            except (KeyError, ValueError) as err:
                print(f"  [AVISO] Error al reconstruir usuario: {err}")

        # Cargar Ventas
        raw_ventas = self._archivo_servicio.cargar_ventas(self._ruta_ventas)
        self._ventas = []
        for v_dict in raw_ventas:
            try:
                vta = Venta.from_dict(v_dict)
                self._ventas.append(vta)
            except (KeyError, ValueError) as err:
                print(f"  [AVISO] Error al reconstruir venta: {err}")

    def validar_acceso(
        self, usuario_o_id: str, contrasena: str
    ) -> Optional[Usuario]:
        """
        Valida las credenciales ingresadas en la pantalla de inicio de sesión (LoginView).

        Args:
            usuario_o_id: Identificación, correo o nombre ingresado por el usuario.
            contrasena:   Contraseña ingresada.

        Returns:
            Instancia de Usuario si la validación es exitosa; None en caso contrario.
        """
        user_clean = usuario_o_id.strip() if usuario_o_id else ""
        pass_clean = contrasena.strip() if contrasena else ""

        if not user_clean or not pass_clean:
            return None

        # Buscar coincidencia por cédula/ID, correo o nombre
        for usr in self._usuarios:
            if (
                usr.identificacion.lower() == user_clean.lower()
                or usr.correo.lower() == user_clean.lower()
                or usr.nombre.lower() == user_clean.lower()
            ):
                return usr

        return None

    def obtener_productos(self) -> List[Producto]:
        """Devuelve la lista completa de productos registrados."""
        return self._productos

    def obtener_usuarios(self) -> List[Usuario]:
        """Devuelve la lista completa de usuarios registrados."""
        return self._usuarios

    def obtener_ventas(self) -> List[Venta]:
        """Devuelve la lista completa de ventas registradas."""
        return self._ventas

    def obtener_total_productos(self) -> int:
        """Devuelve la cantidad total de tipos de productos registrados."""
        return len(self._productos)

    def obtener_total_usuarios(self) -> int:
        """Devuelve la cantidad total de usuarios registrados."""
        return len(self._usuarios)

    def obtener_total_ventas(self) -> int:
        """Devuelve la cantidad total de ventas registradas."""
        return len(self._ventas)

    def obtener_total_stock(self) -> int:
        """Devuelve la suma total de unidades en stock de todos los productos."""
        return sum(p.stock for p in self._productos)

    def obtener_monto_total_ventas(self) -> float:
        """Devuelve la suma total acumulada del valor de todas las ventas."""
        return sum(v.total for v in self._ventas)

    # ------------------------------------------------------------------ #
    #  OPERACIONES CRUD SOBRE PRODUCTOS (Lógica de Negocio + Persistencia)#
    # ------------------------------------------------------------------ #
    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        """
        Busca un producto por su código único en la colección en memoria.
        """
        if not codigo:
            return None
        cod_clean = codigo.strip().upper()
        for p in self._productos:
            if p.codigo == cod_clean:
                return p
        return None

    def registrar_producto(
        self, codigo: str, nombre: str, categoria: str, precio_val: Any, stock_val: Any
    ) -> Tuple[bool, str]:
        """
        Registra un nuevo producto en el sistema, previa validación de negocio.
        """
        if self.buscar_producto(codigo) is not None:
            return (
                False,
                f"El código '{codigo.strip().upper()}' ya se encuentra registrado.",
            )

        try:
            nuevo_prod = Producto(
                codigo=codigo,
                nombre=nombre,
                categoria=categoria,
                precio=precio_val,
                stock=stock_val,
            )
        except ValueError as err:
            return False, f"Error de validación: {err}"

        self._productos.append(nuevo_prod)
        if self._guardar_productos():
            return (
                True,
                f"Producto '{nuevo_prod.nombre}' ({nuevo_prod.codigo}) registrado con éxito.",
            )
        else:
            return (
                False,
                "El producto se agregó en memoria, pero falló el guardado en productos.json.",
            )

    def actualizar_producto(
        self, codigo: str, nombre: str, categoria: str, precio_val: Any, stock_val: Any
    ) -> Tuple[bool, str]:
        """
        Actualiza los datos de un producto existente.
        """
        prod = self.buscar_producto(codigo)
        if prod is None:
            return (
                False,
                f"No se encontró ningún producto con el código '{codigo}'.",
            )

        try:
            prod.nombre = nombre
            prod.categoria = categoria
            prod.precio = precio_val
            prod.stock = stock_val
        except ValueError as err:
            return False, f"Error de validación al actualizar: {err}"

        if self._guardar_productos():
            return (
                True,
                f"Producto '{prod.codigo}' actualizado correctamente.",
            )
        else:
            return (
                False,
                "Se actualizaron los datos en memoria, pero falló la persistencia en productos.json.",
            )

    def eliminar_producto(self, codigo: str) -> Tuple[bool, str]:
        """
        Elimina un producto del sistema por su código único.
        """
        prod = self.buscar_producto(codigo)
        if prod is None:
            return (
                False,
                f"No se encontró ningún producto con el código '{codigo}'.",
            )

        self._productos.remove(prod)
        if self._guardar_productos():
            return (
                True,
                f"Producto '{prod.nombre}' ({prod.codigo}) eliminado con éxito.",
            )
        else:
            return (
                False,
                "Se removió el producto de memoria, pero falló la actualización en productos.json.",
            )

    def _guardar_productos(self) -> bool:
        """Convierte la colección de productos a diccionarios y persiste en JSON."""
        lista_dicts = [p.to_dict() for p in self._productos]
        return self._archivo_servicio.guardar_productos(
            self._ruta_productos, lista_dicts
        )

    # ------------------------------------------------------------------ #
    #  OPERACIONES CRUD SOBRE USUARIOS (Lógica de Negocio + Persistencia) #
    # ------------------------------------------------------------------ #
    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        """
        Busca un usuario por su identificación (cédula) única en memoria.
        """
        if not identificacion:
            return None
        id_clean = identificacion.strip().lower()
        for u in self._usuarios:
            if u.identificacion.lower() == id_clean:
                return u
        return None

    def registrar_usuario(
        self, identificacion: str, nombre: str, correo: str, rol: str = "Cliente"
    ) -> Tuple[bool, str]:
        """
        Registra un nuevo usuario en el sistema, previa validación de negocio.
        """
        if self.buscar_usuario(identificacion) is not None:
            return (
                False,
                f"La identificación '{identificacion.strip()}' ya se encuentra registrada.",
            )

        try:
            nuevo_usr = Usuario(
                identificacion=identificacion,
                nombre=nombre,
                correo=correo,
                rol=rol,
            )
        except ValueError as err:
            return False, f"Error de validación: {err}"

        self._usuarios.append(nuevo_usr)
        if self._guardar_usuarios():
            return (
                True,
                f"Usuario '{nuevo_usr.nombre}' ({nuevo_usr.identificacion} - Rol: {nuevo_usr.rol}) registrado con éxito.",
            )
        else:
            return (
                False,
                "El usuario se agregó en memoria, pero falló la persistencia en usuarios.json.",
            )

    def actualizar_usuario(
        self, identificacion: str, nombre: str, correo: str, rol: str = "Cliente"
    ) -> Tuple[bool, str]:
        """
        Actualiza la información de un usuario existente.
        """
        usr = self.buscar_usuario(identificacion)
        if usr is None:
            return (
                False,
                f"No se encontró ningún usuario con la identificación '{identificacion}'.",
            )

        try:
            usr.nombre = nombre
            usr.correo = correo
            usr.rol = rol
        except ValueError as err:
            return False, f"Error de validación al actualizar: {err}"

        if self._guardar_usuarios():
            return (
                True,
                f"Usuario '{usr.identificacion}' actualizado correctamente (Rol: {usr.rol}).",
            )
        else:
            return (
                False,
                "Se actualizaron los datos en memoria, pero falló el guardado en usuarios.json.",
            )

    def eliminar_usuario(self, identificacion: str) -> Tuple[bool, str]:
        """
        Elimina un usuario del sistema por su identificación única.
        """
        usr = self.buscar_usuario(identificacion)
        if usr is None:
            return (
                False,
                f"No se encontró ningún usuario con la identificación '{identificacion}'.",
            )

        self._usuarios.remove(usr)
        if self._guardar_usuarios():
            return (
                True,
                f"Usuario '{usr.nombre}' ({usr.identificacion}) eliminado con éxito.",
            )
        else:
            return (
                False,
                "Se removió el usuario de memoria, pero falló la actualización en usuarios.json.",
            )

    def _guardar_usuarios(self) -> bool:
        """Convierte la colección de usuarios a diccionarios y persiste en JSON."""
        lista_dicts = [u.to_dict() for u in self._usuarios]
        return self._archivo_servicio.guardar_usuarios(
            self._ruta_usuarios, lista_dicts
        )

    # ------------------------------------------------------------------ #
    #  OPERACIONES SOBRE VENTAS (Evolución Semana 15 — Lógica + Eventos)  #
    # ------------------------------------------------------------------ #
    def buscar_venta(self, id_venta: str) -> Optional[Venta]:
        """
        Busca una venta por su código o identificador único.
        """
        if not id_venta:
            return None
        id_clean = id_venta.strip().upper()
        for v in self._ventas:
            if v.id_venta == id_clean:
                return v
        return None

    def registrar_venta(
        self, identificacion_usuario: str, codigo_producto: str
    ) -> Tuple[bool, str]:
        """
        Registra una venta relacionando un usuario existente con un producto existente.

        Flujo de negocio y validaciones:
        1. Valida que el usuario seleccionado exista en la base de datos.
        2. Valida que el producto seleccionado exista en la base de datos.
        3. Valida la disponibilidad de stock del producto (stock > 0).
        4. Descuenda 1 unidad del stock del producto y actualiza productos.json.
        5. Genera un ID de venta secuencial único (e.g., 'V001', 'V002', ...).
        6. Obtiene la fecha/hora actual del sistema.
        7. Construye el objeto Venta, lo agrega a memoria y lo persiste en ventas.json.

        Args:
            identificacion_usuario: Cédula / ID del usuario comprador.
            codigo_producto:        Código del producto a vender.

        Returns:
            Tuple[bool, str]: (Éxito, Mensaje explicativo)
        """
        id_usr_clean = identificacion_usuario.strip() if identificacion_usuario else ""
        cod_prod_clean = codigo_producto.strip().upper() if codigo_producto else ""

        if not id_usr_clean:
            return False, "Debe seleccionar o ingresar un usuario registrado."

        if not cod_prod_clean:
            return False, "Debe seleccionar o ingresar un producto registrado."

        # Validar existencia de usuario
        usuario = self.buscar_usuario(id_usr_clean)
        if usuario is None:
            return (
                False,
                f"El usuario con identificación '{id_usr_clean}' no está registrado.",
            )

        # Validar existencia de producto
        producto = self.buscar_producto(cod_prod_clean)
        if producto is None:
            return (
                False,
                f"El producto con código '{cod_prod_clean}' no está registrado.",
            )

        # Validar stock disponible
        if producto.stock <= 0:
            return (
                False,
                f"El producto '{producto.nombre}' no tiene stock disponible (Stock: 0).",
            )

        # Generar ID secuencial de la venta
        num_siguiente = len(self._ventas) + 1
        id_venta = f"V{num_siguiente:03d}"
        while self.buscar_venta(id_venta) is not None:
            num_siguiente += 1
            id_venta = f"V{num_siguiente:03d}"

        # Obtener fecha y hora actual
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            nueva_venta = Venta(
                id_venta=id_venta,
                identificacion_usuario=usuario.identificacion,
                codigo_producto=producto.codigo,
                fecha=fecha_actual,
                total=producto.precio,
            )
        except ValueError as err:
            return False, f"Error de validación en la venta: {err}"

        # Descontar stock del producto
        producto.stock -= 1
        self._guardar_productos()

        # Guardar la nueva venta
        self._ventas.append(nueva_venta)
        if self._guardar_ventas():
            return (
                True,
                f"Venta '{id_venta}' registrada con éxito. Cliente: {usuario.nombre} | "
                f"Producto: {producto.nombre} | Total: ${producto.precio:.2f}",
            )
        else:
            return (
                False,
                "Se procesó la venta en memoria, pero falló la persistencia en ventas.json.",
            )

    def _guardar_ventas(self) -> bool:
        """Convierte la colección de ventas a diccionarios y persiste en JSON."""
        lista_dicts = [v.to_dict() for v in self._ventas]
        return self._archivo_servicio.guardar_ventas(
            self._ruta_ventas, lista_dicts
        )
