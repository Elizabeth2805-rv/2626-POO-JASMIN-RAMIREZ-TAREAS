# -*- coding: utf-8 -*-
# servicios/restaurante.py
# Semana 11 — Persistencia JSON, colecciones, relaciones y ventas.
#
# Principio SRP: esta clase administra las colecciones en memoria de productos,
# usuarios y ventas. Ejecuta la lógica de negocio, búsquedas, registros y operaciones de venta.
# No interactúa directamente con la consola ni realiza operaciones de I/O de disco.

from typing import List, Optional, Dict, Any, Tuple
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    """
    Clase de servicio encargada de administrar las colecciones de dominio en memoria.

    Aplica SRP: administra las colecciones de objetos Producto, Usuario y Venta,
    ejecutando las reglas de negocio (unicidad de códigos, control de stock,
    relación Usuario-Producto al realizar una venta y filtrado de ventas por usuario).
    """

    def __init__(
        self,
        productos_iniciales: Optional[List[Producto]] = None,
        usuarios_iniciales: Optional[List[Usuario]] = None,
        ventas_iniciales: Optional[List[Venta]] = None,
    ) -> None:
        """
        Constructor de la clase Restaurante.

        Args:
            productos_iniciales: Lista opcional de objetos Producto precargados.
            usuarios_iniciales:  Lista opcional de objetos Usuario precargados.
            ventas_iniciales:    Lista opcional de objetos Venta precargados.
        """
        self._productos: List[Producto] = (
            list(productos_iniciales) if productos_iniciales is not None else []
        )
        self._usuarios: List[Usuario] = (
            list(usuarios_iniciales) if usuarios_iniciales is not None else []
        )
        self._ventas: List[Venta] = (
            list(ventas_iniciales) if ventas_iniciales is not None else []
        )

    # ================================================================== #
    #  Operaciones sobre la colección de Productos                         #
    # ================================================================== #

    def cargar_productos_iniciales(self, productos: List[Producto]) -> None:
        """Establece la lista inicial de productos administrados por el servicio."""
        self._productos = list(productos)

    def registrar_producto(self, producto: Producto) -> None:
        """
        Registra un nuevo producto en la colección.

        Args:
            producto: Instancia de Producto a agregar.

        Raises:
            TypeError:  Si el parámetro no es una instancia de Producto.
            ValueError: Si ya existe un producto registrado con el mismo código.
        """
        if not isinstance(producto, Producto):
            raise TypeError("El objeto a registrar debe ser una instancia de Producto.")

        if self._existe_codigo_producto(producto.codigo):
            raise ValueError(
                f"Ya existe un producto registrado con el código '{producto.codigo}'."
            )

        self._productos.append(producto)

    def listar_productos(self) -> List[Producto]:
        """Retorna una copia de la lista de productos registrados."""
        return list(self._productos)

    def buscar_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        """Busca un producto en la colección por su código único."""
        codigo_buscado = codigo.strip().upper()
        for producto in self._productos:
            if producto.codigo == codigo_buscado:
                return producto
        return None

    def actualizar_producto(
        self,
        codigo: str,
        nuevo_nombre: Optional[str] = None,
        nueva_categoria: Optional[str] = None,
        nuevo_precio: Optional[float] = None,
        nuevo_stock: Optional[int] = None,
    ) -> bool:
        """
        Actualiza los atributos de un producto existente en la colección.

        Returns:
            bool: True si se actualizó con éxito; False en caso contrario.
        """
        producto = self.buscar_producto_por_codigo(codigo)
        if producto is None:
            return False

        if nuevo_nombre is not None and nuevo_nombre.strip():
            producto.nombre = nuevo_nombre
        if nueva_categoria is not None and nueva_categoria.strip():
            producto.categoria = nueva_categoria
        if nuevo_precio is not None:
            producto.precio = nuevo_precio
        if nuevo_stock is not None:
            producto.stock = nuevo_stock

        return True

    def eliminar_producto(self, codigo: str) -> bool:
        """Elimina un producto de la colección según su código."""
        codigo_buscado = codigo.strip().upper()
        for indice, producto in enumerate(self._productos):
            if producto.codigo == codigo_buscado:
                self._productos.pop(indice)
                return True
        return False

    def obtener_productos_como_dict(self) -> List[Dict[str, Any]]:
        """Convierte toda la colección de objetos Producto a una lista de diccionarios."""
        return [producto.to_dict() for producto in self._productos]

    def _existe_codigo_producto(self, codigo: str) -> bool:
        """Verifica si ya existe un producto con el código indicado."""
        return any(p.codigo == codigo.strip().upper() for p in self._productos)

    # ================================================================== #
    #  Operaciones sobre la colección de Usuarios                         #
    # ================================================================== #

    def cargar_usuarios_iniciales(self, usuarios: List[Usuario]) -> None:
        """Establece la lista inicial de usuarios administrados por el servicio."""
        self._usuarios = list(usuarios)

    def registrar_usuario(self, usuario: Usuario) -> None:
        """
        Registra un usuario en la colección en memoria.

        Args:
            usuario: Instancia de Usuario a agregar.

        Raises:
            TypeError:  Si no es una instancia de Usuario.
            ValueError: Si la identificación del usuario ya existe.
        """
        if not isinstance(usuario, Usuario):
            raise TypeError("El objeto a registrar debe ser una instancia de Usuario.")

        if self._existe_id_usuario(usuario.identificacion):
            raise ValueError(
                f"Ya existe un usuario registrado con la ID '{usuario.identificacion}'."
            )

        self._usuarios.append(usuario)

    def listar_usuarios(self) -> List[Usuario]:
        """Retorna una copia de la lista de usuarios registrados."""
        return list(self._usuarios)

    def buscar_usuario_por_id(self, identificacion: str) -> Optional[Usuario]:
        """Busca un usuario por su número de identificación."""
        id_buscada = identificacion.strip()
        for usuario in self._usuarios:
            if usuario.identificacion == id_buscada:
                return usuario
        return None

    def obtener_usuarios_como_dict(self) -> List[Dict[str, Any]]:
        """Convierte toda la colección de objetos Usuario a una lista de diccionarios."""
        return [usuario.to_dict() for usuario in self._usuarios]

    def _existe_id_usuario(self, identificacion: str) -> bool:
        """Verifica si ya existe un usuario con la identificación dada."""
        return any(u.identificacion == identificacion.strip() for u in self._usuarios)

    # ================================================================== #
    #  Operaciones sobre la colección de Ventas (Relaciones y Reglas)     #
    # ================================================================== #

    def cargar_ventas_iniciales(self, ventas: List[Venta]) -> None:
        """Establece la lista inicial de ventas administradas por el servicio."""
        self._ventas = list(ventas)

    def vender_producto(
        self,
        codigo_producto: str,
        identificacion_usuario: str,
        cantidad: int,
    ) -> bool:
        """
        Ejecuta la operación de venta de un producto a un usuario registrado.

        Reglas de negocio:
        1. Comprobar que el usuario exista.
        2. Comprobar que el producto exista.
        3. Comprobar que la cantidad solicitada sea mayor que cero.
        4. Comprobar que exista stock suficiente del producto.
        5. Registrar la Venta en la colección `_ventas`.
        6. Disminuir el stock del producto vendido.

        Args:
            codigo_producto:        Código del producto a comprar.
            identificacion_usuario: Cédula/ID del usuario comprador.
            cantidad:               Cantidad requerida.

        Returns:
            bool: True si la venta fue procesada exitosamente; False en caso contrario.
        """
        usuario = self.buscar_usuario_por_id(identificacion_usuario)
        producto = self.buscar_producto_por_codigo(codigo_producto)

        if usuario is None or producto is None:
            return False

        if cantidad <= 0 or producto.stock < cantidad:
            return False

        # Crear objeto Venta y registrarlo en la colección
        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)

        # Disminuir stock del producto
        producto.vender(cantidad)
        return True

    def vender_producto_con_detalle(
        self,
        codigo_producto: str,
        identificacion_usuario: str,
        cantidad: int,
    ) -> Tuple[bool, str]:
        """
        Variación detallada de vender_producto que retorna el estado y una explicación.
        """
        usuario = self.buscar_usuario_por_id(identificacion_usuario)
        if usuario is None:
            return False, f"El usuario con ID '{identificacion_usuario}' no existe."

        producto = self.buscar_producto_por_codigo(codigo_producto)
        if producto is None:
            return False, f"El producto con código '{codigo_producto.upper()}' no existe."

        if cantidad <= 0:
            return False, "La cantidad solicitada debe ser mayor que cero."

        if producto.stock < cantidad:
            return (
                False,
                f"Stock insuficiente para '{producto.nombre}'. "
                f"Disponible: {producto.stock}, Solicitado: {cantidad}.",
            )

        # Ejecutar venta
        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)
        producto.vender(cantidad)

        return (
            True,
            f"Venta registrada exitosamente: {cantidad} unidad(es) de '{producto.nombre}' "
            f"para el usuario '{usuario.nombre}'.",
        )

    def consultar_ventas_por_usuario(self, identificacion_usuario: str) -> List[Venta]:
        """
        Filtra y retorna únicamente las ventas asociadas a un usuario específico.

        Demuestra el recorrido y filtrado directo de la colección de ventas.

        Args:
            identificacion_usuario: ID del usuario a consultar.

        Returns:
            List[Venta]: Lista de objetos Venta realizados por el usuario.
        """
        id_buscada = identificacion_usuario.strip()
        ventas_usuario: List[Venta] = []

        for venta in self._ventas:
            if venta.usuario_id == id_buscada:
                ventas_usuario.append(venta)

        return ventas_usuario

    def listar_ventas(self) -> List[Venta]:
        """Retorna una copia de todas las ventas registradas."""
        return list(self._ventas)

    def obtener_ventas_como_dict(self) -> List[Dict[str, Any]]:
        """Convierte toda la colección de objetos Venta a una lista de diccionarios."""
        return [venta.to_dict() for venta in self._ventas]
