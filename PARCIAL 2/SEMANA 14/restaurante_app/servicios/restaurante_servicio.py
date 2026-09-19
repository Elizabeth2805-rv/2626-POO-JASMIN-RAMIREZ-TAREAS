# -*- coding: utf-8 -*-
# servicios/restaurante_servicio.py
# Semana 14 — Componentes y Contenedores (Evolución Restaurante App)
#
# Principio SRP: Esta clase encapsula la lógica de negocio del restaurante,
# coordinando el modelo de datos (Producto, Usuario) y la persistencia (ArchivoServicio).
# Concentra la validación de negocio y operaciones CRUD sobre productos y usuarios.

from typing import List, Optional, Tuple
from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """
    Servicio principal que gestiona las operaciones de negocio del restaurante.

    Mantiene colecciones en memoria de objetos Producto y Usuario, proporcionando
    métodos para validar acceso, consultar información y realizar operaciones
    CRUD completas sobre productos y usuarios con persistencia en JSON.
    """

    def __init__(
        self,
        archivo_servicio: Optional[ArchivoServicio] = None,
        ruta_productos: str = "datos/productos.json",
        ruta_usuarios: str = "datos/usuarios.json",
    ) -> None:
        """
        Constructor del servicio de restaurante.

        Args:
            archivo_servicio: Instancia del servicio de archivos (I/O).
            ruta_productos:   Ruta al archivo productos.json.
            ruta_usuarios:    Ruta al archivo usuarios.json.
        """
        self._archivo_servicio = archivo_servicio or ArchivoServicio()
        self._ruta_productos = ruta_productos
        self._ruta_usuarios = ruta_usuarios

        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []

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

    def cargar_datos_iniciales(self) -> None:
        """
        Lee las estructuras JSON desde ArchivoServicio y las transforma
        en instancias de objetos de los modelos Producto y Usuario.
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

    def obtener_total_productos(self) -> int:
        """Devuelve la cantidad total de tipos de productos registrados."""
        return len(self._productos)

    def obtener_total_usuarios(self) -> int:
        """Devuelve la cantidad total de usuarios registrados."""
        return len(self._usuarios)

    def obtener_total_stock(self) -> int:
        """Devuelve la suma total de unidades en stock de todos los productos."""
        return sum(p.stock for p in self._productos)

    # ------------------------------------------------------------------ #
    #  OPERACIONES CRUD SOBRE PRODUCTOS (Lógica de Negocio + Persistencia)#
    # ------------------------------------------------------------------ #
    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        """
        Busca un producto por su código único en la colección en memoria.

        Args:
            codigo: Código del producto a buscar.

        Returns:
            Instancia de Producto si se encuentra; None en caso contrario.
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

        Returns:
            Tuple[bool, str]: (Éxito, Mensaje explicativo)
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

        # Agregar a la lista y persistir en JSON
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

        Returns:
            Tuple[bool, str]: (Éxito, Mensaje explicativo)
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

        Returns:
            Tuple[bool, str]: (Éxito, Mensaje explicativo)
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

        Args:
            identificacion: Cédula o identificador del usuario.

        Returns:
            Instancia de Usuario si se encuentra; None en caso contrario.
        """
        if not identificacion:
            return None
        id_clean = identificacion.strip().lower()
        for u in self._usuarios:
            if u.identificacion.lower() == id_clean:
                return u
        return None

    def registrar_usuario(
        self, identificacion: str, nombre: str, correo: str
    ) -> Tuple[bool, str]:
        """
        Registra un nuevo usuario en el sistema, previa validación de negocio.

        Validaciones:
        - La identificación no debe estar registrada previamente.
        - El nombre y correo no deben estar vacíos.
        - El correo debe tener un formato válido con '@' y dominio.
        - Persiste los cambios en usuarios.json de forma inmediata.

        Returns:
            Tuple[bool, str]: (Éxito, Mensaje explicativo)
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
            )
        except ValueError as err:
            return False, f"Error de validación: {err}"

        # Agregar a la lista y persistir en JSON
        self._usuarios.append(nuevo_usr)
        if self._guardar_usuarios():
            return (
                True,
                f"Usuario '{nuevo_usr.nombre}' ({nuevo_usr.identificacion}) registrado con éxito.",
            )
        else:
            return (
                False,
                "El usuario se agregó en memoria, pero falló la persistencia en usuarios.json.",
            )

    def actualizar_usuario(
        self, identificacion: str, nombre: str, correo: str
    ) -> Tuple[bool, str]:
        """
        Actualiza la información de un usuario existente.

        Args:
            identificacion: Identificación / cédula del usuario a actualizar.
            nombre:         Nuevo nombre completo.
            correo:         Nuevo correo electrónico.

        Returns:
            Tuple[bool, str]: (Éxito, Mensaje explicativo)
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
        except ValueError as err:
            return False, f"Error de validación al actualizar: {err}"

        if self._guardar_usuarios():
            return (
                True,
                f"Usuario '{usr.identificacion}' actualizado correctamente.",
            )
        else:
            return (
                False,
                "Se actualizaron los datos en memoria, pero falló el guardado en usuarios.json.",
            )

    def eliminar_usuario(self, identificacion: str) -> Tuple[bool, str]:
        """
        Elimina un usuario del sistema por su identificación única.

        Args:
            identificacion: Cédula o identificador del usuario.

        Returns:
            Tuple[bool, str]: (Éxito, Mensaje explicativo)
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
