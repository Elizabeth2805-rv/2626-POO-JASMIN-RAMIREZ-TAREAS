# -*- coding: utf-8 -*-
# servicios/restaurante.py
# Semana 10 — Persistencia JSON, control de excepciones y modularidad.
#
# Principio SRP: esta clase administra exclusivamente la colección de productos
# y usuarios en memoria, realizando operaciones de búsqueda, registro, actualización,
# eliminación y listado. No interactúa con archivos de disco ni con la consola.

from typing import List, Optional, Dict, Any
from modelos.producto import Producto
from modelos.usuario import Usuario


class Restaurante:
    """
    Clase de servicio encargada de administrar las colecciones de dominio.

    Aplica SRP: administra los productos y usuarios en memoria y ejecuta la
    lógica de negocio asociada (búsquedas, unicidad de código, actualizaciones).
    No contiene lógica de entrada/salida a disco ni de interfaz de consola.
    """

    def __init__(self, productos_iniciales: Optional[List[Producto]] = None) -> None:
        """
        Constructor de la clase Restaurante.

        Args:
            productos_iniciales: Lista opcional de objetos Producto precargados.
        """
        self._productos: List[Producto] = productos_iniciales if productos_iniciales is not None else []
        self._usuarios: List[Usuario] = []

    # ================================================================== #
    #  Operaciones sobre la colección de Productos                         #
    # ================================================================== #

    def cargar_productos_iniciales(self, productos: List[Producto]) -> None:
        """
        Establece la lista inicial de productos administrados por el servicio.

        Args:
            productos: Lista de objetos Producto reconstruidos.
        """
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
        """
        Retorna una copia de la lista de productos registrados.

        Returns:
            List[Producto]: Copia de la lista de objetos Producto.
        """
        return list(self._productos)

    def buscar_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        """
        Busca un producto en la colección por su código único.

        Args:
            codigo: Código del producto a buscar.

        Returns:
            Optional[Producto]: Objeto Producto si se encuentra, None en caso contrario.
        """
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
    ) -> bool:
        """
        Actualiza los atributos de un producto existente en la colección.

        Args:
            codigo:          Código del producto a actualizar.
            nuevo_nombre:    Nuevo nombre (opcional).
            nueva_categoria: Nueva categoría (opcional).
            nuevo_precio:    Nuevo precio (opcional).

        Returns:
            bool: True si el producto existía y se actualizó; False en caso contrario.

        Raises:
            ValueError: Si alguno de los nuevos valores no supera la validación.
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

        return True

    def eliminar_producto(self, codigo: str) -> bool:
        """
        Elimina un producto de la colección según su código.

        Args:
            codigo: Código del producto a eliminar.

        Returns:
            bool: True si fue encontrado y eliminado; False en caso contrario.
        """
        codigo_buscado = codigo.strip().upper()
        for indice, producto in enumerate(self._productos):
            if producto.codigo == codigo_buscado:
                self._productos.pop(indice)
                return True
        return False

    def obtener_productos_como_dict(self) -> List[Dict[str, Any]]:
        """
        Convierte toda la colección de objetos Producto a una lista de diccionarios.

        Returns:
            List[dict]: Lista de diccionarios listos para ser serializados en JSON.
        """
        return [producto.to_dict() for producto in self._productos]

    def _existe_codigo_producto(self, codigo: str) -> bool:
        """Verifica si ya existe un producto con el código indicado."""
        return any(p.codigo == codigo.strip().upper() for p in self._productos)

    # ================================================================== #
    #  Operaciones sobre la colección de Usuarios                         #
    # ================================================================== #

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
        """
        Retorna una copia de la lista de usuarios en memoria.

        Returns:
            List[Usuario]: Copia de la lista de objetos Usuario.
        """
        return list(self._usuarios)

    def buscar_usuario_por_id(self, identificacion: str) -> Optional[Usuario]:
        """
        Busca un usuario por su número de identificación.

        Args:
            identificacion: Cédula o número de documento del usuario.

        Returns:
            Optional[Usuario]: Objeto Usuario si existe, None en caso contrario.
        """
        id_buscada = identificacion.strip()
        for usuario in self._usuarios:
            if usuario.identificacion == id_buscada:
                return usuario
        return None

    def _existe_id_usuario(self, identificacion: str) -> bool:
        """Verifica si ya existe un usuario con la identificación dada."""
        return any(u.identificacion == identificacion.strip() for u in self._usuarios)
