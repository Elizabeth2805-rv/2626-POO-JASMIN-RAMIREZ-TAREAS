# -*- coding: utf-8 -*-
# servicios/restaurante.py
# Semana 12 — Rendimiento mediante colecciones, índices (dict) y conjuntos (set).
#
# Principio SRP: esta clase es el servicio de dominio que administra las colecciones
# de productos, usuarios y ventas. Mantiene colecciones principales (List) para la
# ordenación y persistencia, y estructuras auxiliares (Dict, Set) para lograr
# búsquedas, validaciones de unicidad y consultas en tiempo constante O(1).

from typing import List, Optional, Dict, Any, Tuple, Set
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    """
    Clase de servicio encargada de administrar las colecciones de dominio en memoria.

    Implementación de optimización de rendimiento para la Semana 12:
    - Conserva las colecciones principales (List) para almacenamiento, recorrido
      secuencial y persistencia en archivos JSON.
    - Incorpora índices auxiliares en memoria con `dict` para búsquedas frecuentes O(1)
      por clave única (código de producto, cédula de usuario, ventas por usuario).
    - Incorpora conjuntos `set` para validaciones de pertenencia y unicidad O(1).
    - Mantiene sincronizadas todas las estructuras auxiliares tras inserciones,
      modificaciones y eliminaciones.
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
        # -----------------------------------------------------------------
        # 1. Colecciones Principales (List) — Almacenamiento y Persistencia
        # -----------------------------------------------------------------
        self._productos: List[Producto] = (
            list(productos_iniciales) if productos_iniciales is not None else []
        )
        self._usuarios: List[Usuario] = (
            list(usuarios_iniciales) if usuarios_iniciales is not None else []
        )
        self._ventas: List[Venta] = (
            list(ventas_iniciales) if ventas_iniciales is not None else []
        )

        # -----------------------------------------------------------------
        # 2. Estructuras Auxiliares (Dict, Set) — Optimización O(1)
        # -----------------------------------------------------------------
        # Índices de Productos
        self._idx_productos: Dict[str, Producto] = {}
        self._codigos_productos: Set[str] = set()

        # Índices de Usuarios
        self._idx_usuarios: Dict[str, Usuario] = {}
        self._ids_usuarios: Set[str] = set()

        # Índice de Ventas agrupadadas por Usuario (evita recorridos completos)
        self._idx_ventas_por_usuario: Dict[str, List[Venta]] = {}

        # -----------------------------------------------------------------
        # 3. Construcción Inicial de Índices en Memoria
        # -----------------------------------------------------------------
        self.reconstruir_indices()

    # ================================================================== #
    #  Reconstrucción y Diagnóstico de Índices Auxiliares                #
    # ================================================================== #

    def reconstruir_indices(self) -> None:
        """
        Reconstruye la totalidad de las estructuras auxiliares (Dict y Set)
        a partir de las listas principales almacenadas en memoria.
        """
        self._reconstruir_indices_productos()
        self._reconstruir_indices_usuarios()
        self._reconstruir_indices_ventas()

    def _reconstruir_indices_productos(self) -> None:
        """Reconstruye el diccionario e índice de conjunto para productos."""
        self._idx_productos.clear()
        self._codigos_productos.clear()
        for producto in self._productos:
            cod = producto.codigo
            self._idx_productos[cod] = producto
            self._codigos_productos.add(cod)

    def _reconstruir_indices_usuarios(self) -> None:
        """Reconstruye el diccionario e índice de conjunto para usuarios."""
        self._idx_usuarios.clear()
        self._ids_usuarios.clear()
        for usuario in self._usuarios:
            usr_id = usuario.identificacion
            self._idx_usuarios[usr_id] = usuario
            self._ids_usuarios.add(usr_id)
            if usr_id not in self._idx_ventas_por_usuario:
                self._idx_ventas_por_usuario[usr_id] = []

    def _reconstruir_indices_ventas(self) -> None:
        """Reconstruye el diccionario indexado de ventas organizadas por usuario."""
        self._idx_ventas_por_usuario.clear()
        # Asegurar entradas vacías para todos los usuarios registrados
        for usr_id in self._ids_usuarios:
            self._idx_ventas_por_usuario[usr_id] = []

        for venta in self._ventas:
            usr_id = venta.usuario_id
            if usr_id not in self._idx_ventas_por_usuario:
                self._idx_ventas_por_usuario[usr_id] = []
            self._idx_ventas_por_usuario[usr_id].append(venta)

    def obtener_resumen_indices(self) -> Dict[str, Any]:
        """
        Retorna estadísticas de sincronización entre las listas principales
        y las estructuras auxiliares para verificación de rendimiento.
        """
        return {
            "total_productos_lista": len(self._productos),
            "total_productos_dict": len(self._idx_productos),
            "total_codigos_set": len(self._codigos_productos),
            "total_usuarios_lista": len(self._usuarios),
            "total_usuarios_dict": len(self._idx_usuarios),
            "total_ids_set": len(self._ids_usuarios),
            "total_ventas_lista": len(self._ventas),
            "total_usuarios_con_ventas_indexadas": len(self._idx_ventas_por_usuario),
        }

    # ================================================================== #
    #  Operaciones sobre la colección de Productos                         #
    # ================================================================== #

    def cargar_productos_iniciales(self, productos: List[Producto]) -> None:
        """Establece la lista inicial de productos y actualiza sus índices."""
        self._productos = list(productos)
        self._reconstruir_indices_productos()

    def registrar_producto(self, producto: Producto) -> None:
        """
        Registra un nuevo producto en la colección y actualiza los índices auxiliares.

        Optimización Semana 12:
        - Revisa la existencia mediante el `set` _codigos_productos en O(1).
        - Inserta en la lista principal `_productos` y en el índice `_idx_productos` en O(1).

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

        # 1. Colección Principal
        self._productos.append(producto)

        # 2. Estructuras Auxiliares Sincronizadas
        cod = producto.codigo
        self._idx_productos[cod] = producto
        self._codigos_productos.add(cod)

    def listar_productos(self) -> List[Producto]:
        """Retorna una copia de la lista principal de productos registrados."""
        return list(self._productos)

    def buscar_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        """
        Busca un producto en la colección por su código único.

        Optimización Semana 12:
        Utiliza el índice diccionario `_idx_productos` con acceso directo O(1),
        evitando iterar secuencialmente sobre la lista completa.
        """
        codigo_buscado = codigo.strip().upper()
        return self._idx_productos.get(codigo_buscado)

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

        Optimización Semana 12:
        Localiza el producto directamente en O(1) mediante el índice `_idx_productos`.
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
        """
        Elimina un producto de la colección según su código.

        Optimización Semana 12:
        Mantiene sincronizadas las estructuras auxiliares eliminando las referencias
        tanto de la lista principal como de `_idx_productos` y `_codigos_productos`.
        """
        codigo_buscado = codigo.strip().upper()

        if codigo_buscado not in self._codigos_productos:
            return False

        # 1. Eliminar de la lista principal
        self._productos = [p for p in self._productos if p.codigo != codigo_buscado]

        # 2. Eliminar de las estructuras auxiliares O(1)
        self._idx_productos.pop(codigo_buscado, None)
        self._codigos_productos.discard(codigo_buscado)

        return True

    def obtener_productos_como_dict(self) -> List[Dict[str, Any]]:
        """Convierte toda la colección de objetos Producto a una lista de diccionarios."""
        return [producto.to_dict() for producto in self._productos]

    def _existe_codigo_producto(self, codigo: str) -> bool:
        """
        Verifica si ya existe un producto con el código indicado.

        Optimización Semana 12:
        Consulta la pertenencia directa en el conjunto `_codigos_productos` (Set) en O(1).
        """
        return codigo.strip().upper() in self._codigos_productos

    # ================================================================== #
    #  Operaciones sobre la colección de Usuarios                         #
    # ================================================================== #

    def cargar_usuarios_iniciales(self, usuarios: List[Usuario]) -> None:
        """Establece la lista inicial de usuarios y actualiza sus índices."""
        self._usuarios = list(usuarios)
        self._reconstruir_indices_usuarios()

    def registrar_usuario(self, usuario: Usuario) -> None:
        """
        Registra un usuario en la colección en memoria y sincroniza sus índices.

        Optimización Semana 12:
        - Validación de existencia de ID mediante `set` en O(1).
        - Inserción en `_idx_usuarios` y en `_idx_ventas_por_usuario` en O(1).

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

        # 1. Colección Principal
        self._usuarios.append(usuario)

        # 2. Estructuras Auxiliares Sincronizadas
        usr_id = usuario.identificacion
        self._idx_usuarios[usr_id] = usuario
        self._ids_usuarios.add(usr_id)

        if usr_id not in self._idx_ventas_por_usuario:
            self._idx_ventas_por_usuario[usr_id] = []

    def listar_usuarios(self) -> List[Usuario]:
        """Retorna una copia de la lista principal de usuarios registrados."""
        return list(self._usuarios)

    def buscar_usuario_por_id(self, identificacion: str) -> Optional[Usuario]:
        """
        Busca un usuario por su número de identificación.

        Optimización Semana 12:
        Acceso directo O(1) a través del índice diccionario `_idx_usuarios`.
        """
        id_buscada = identificacion.strip()
        return self._idx_usuarios.get(id_buscada)

    def obtener_usuarios_como_dict(self) -> List[Dict[str, Any]]:
        """Convierte toda la colección de objetos Usuario a una lista de diccionarios."""
        return [usuario.to_dict() for usuario in self._usuarios]

    def _existe_id_usuario(self, identificacion: str) -> bool:
        """
        Verifica si ya existe un usuario con la identificación dada.

        Optimización Semana 12:
        Consulta de pertenencia en el conjunto `_ids_usuarios` (Set) en O(1).
        """
        return identificacion.strip() in self._ids_usuarios

    # ================================================================== #
    #  Operaciones sobre la colección de Ventas (Relaciones e Índices)    #
    # ================================================================== #

    def cargar_ventas_iniciales(self, ventas: List[Venta]) -> None:
        """Establece la lista inicial de ventas y reconstruye el índice agrupado."""
        self._ventas = list(ventas)
        self._reconstruir_indices_ventas()

    def vender_producto(
        self,
        codigo_producto: str,
        identificacion_usuario: str,
        cantidad: int,
    ) -> bool:
        """
        Ejecuta la operación de venta de un producto a un usuario registrado.

        Optimización Semana 12:
        - Búsquedas O(1) de usuario y producto mediante índices `dict`.
        - Sincronización inmediata del índice de ventas agrupadas por usuario `_idx_ventas_por_usuario`.
        """
        usuario = self.buscar_usuario_por_id(identificacion_usuario)
        producto = self.buscar_producto_por_codigo(codigo_producto)

        if usuario is None or producto is None:
            return False

        if cantidad <= 0 or producto.stock < cantidad:
            return False

        # Crear objeto Venta y registrarlo en la colección principal
        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)

        # Actualizar índice auxiliar de ventas por usuario
        usr_id = usuario.identificacion
        if usr_id not in self._idx_ventas_por_usuario:
            self._idx_ventas_por_usuario[usr_id] = []
        self._idx_ventas_por_usuario[usr_id].append(venta)

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

        Optimización Semana 12:
        Utiliza búsquedas O(1) y mantiene sincronizado el índice `_idx_ventas_por_usuario`.
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

        # Ejecutar venta y actualizar colecciones principales e índices
        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)

        usr_id = usuario.identificacion
        if usr_id not in self._idx_ventas_por_usuario:
            self._idx_ventas_por_usuario[usr_id] = []
        self._idx_ventas_por_usuario[usr_id].append(venta)

        producto.vender(cantidad)

        return (
            True,
            f"Venta registrada exitosamente: {cantidad} unidad(es) de '{producto.nombre}' "
            f"para el usuario '{usuario.nombre}'.",
        )

    def consultar_ventas_por_usuario(self, identificacion_usuario: str) -> List[Venta]:
        """
        Filtra y retorna únicamente las ventas asociadas a un usuario específico.

        Optimización Semana 12:
        En lugar de recorrer iterativamente toda la lista principal `_ventas` (O(V)),
        recupera la sublista de ventas directamente desde el índice `_idx_ventas_por_usuario`
        en tiempo constante O(1).
        """
        id_buscada = identificacion_usuario.strip()
        ventas_usuario = self._idx_ventas_por_usuario.get(id_buscada, [])
        return list(ventas_usuario)

    def listar_ventas(self) -> List[Venta]:
        """Retorna una copia de todas las ventas registradas."""
        return list(self._ventas)

    def obtener_ventas_como_dict(self) -> List[Dict[str, Any]]:
        """Convierte toda la colección de objetos Venta a una lista de diccionarios."""
        return [venta.to_dict() for venta in self._ventas]
