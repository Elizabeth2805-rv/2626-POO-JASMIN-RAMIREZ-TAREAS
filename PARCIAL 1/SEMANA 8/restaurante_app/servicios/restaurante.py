# -*- coding: utf-8 -*-
# servicios/restaurante.py
# Principio SRP: Esta clase es exclusivamente responsable de administrar
# las colecciones de productos y clientes, y de aplicar las reglas
# de negocio (sin duplicados, validación de tipos).
#
# Principio LSP aplicado al servicio: los métodos de Restaurante
# operan sobre la clase base Producto. Gracias a esto, aceptan tanto
# objetos Producto como objetos Bebida sin necesidad de condicionales
# del tipo isinstance(obj, Bebida).

from typing import List, Optional
from modelos.producto import Producto
from modelos.cliente import Cliente


class Restaurante:
    """
    Clase de servicio que administra las operaciones del restaurante.

    Responsabilidades:
    - Registrar y listar productos (Producto y Bebida en una sola colección).
    - Registrar y listar clientes.
    - Validar que no existan códigos de producto ni identificaciones
      de cliente duplicadas.

    No interactúa directamente con la consola: recibe objetos ya
    construidos y retorna colecciones o lanza excepciones descriptivas.
    """

    def __init__(self) -> None:
        # Una sola colección para Producto y Bebida (LSP en acción)
        self._productos: List[Producto] = []
        self._clientes: List[Cliente] = []

    # ================================================================== #
    #  Métodos de Productos                                                #
    # ================================================================== #

    def registrar_producto(self, producto: Producto) -> None:
        """
        Registra un producto (o bebida) en el sistema.

        Acepta cualquier objeto que sea instancia de Producto o de sus
        subclases (e.g., Bebida) gracias al principio LSP.

        Args:
            producto: Instancia de Producto o de cualquier subclase válida.

        Raises:
            TypeError:  Si el objeto no es una instancia de Producto.
            ValueError: Si ya existe un producto con el mismo código.
        """
        if not isinstance(producto, Producto):
            raise TypeError(
                "Solo se pueden registrar instancias de Producto o sus subclases."
            )
        if self._existe_codigo_producto(producto.codigo):
            raise ValueError(
                f"Ya existe un producto registrado con el código '{producto.codigo}'."
            )
        self._productos.append(producto)

    def listar_productos(self) -> List[Producto]:
        """
        Retorna la lista completa de productos registrados (incluye bebidas).
        """
        return list(self._productos)

    def buscar_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        """
        Busca un producto por su código único (búsqueda exacta).

        Args:
            codigo: Código del producto a buscar.

        Returns:
            El objeto Producto/Bebida si existe, None en caso contrario.
        """
        codigo_buscado = codigo.strip().upper()
        for producto in self._productos:
            if producto.codigo == codigo_buscado:
                return producto
        return None

    def _existe_codigo_producto(self, codigo: str) -> bool:
        """
        Verifica si ya existe un producto registrado con el código dado.

        Método privado de apoyo para evitar duplicados.

        Args:
            codigo: Código a verificar.

        Returns:
            True si el código ya existe, False en caso contrario.
        """
        return any(p.codigo == codigo.strip().upper() for p in self._productos)

    # ================================================================== #
    #  Métodos de Clientes                                                 #
    # ================================================================== #

    def registrar_cliente(self, cliente: Cliente) -> None:
        """
        Registra un cliente en el sistema.

        Args:
            cliente: Instancia de la clase Cliente.

        Raises:
            TypeError:  Si el objeto no es una instancia de Cliente.
            ValueError: Si ya existe un cliente con la misma identificación.
        """
        if not isinstance(cliente, Cliente):
            raise TypeError(
                "Solo se pueden registrar instancias de la clase Cliente."
            )
        if self._existe_identificacion_cliente(cliente.identificacion):
            raise ValueError(
                f"Ya existe un cliente registrado con la identificación "
                f"'{cliente.identificacion}'."
            )
        self._clientes.append(cliente)

    def listar_clientes(self) -> List[Cliente]:
        """
        Retorna la lista completa de clientes registrados.
        """
        return list(self._clientes)

    def buscar_cliente_por_id(self, identificacion: str) -> Optional[Cliente]:
        """
        Busca un cliente por su identificación única (búsqueda exacta).

        Args:
            identificacion: Cédula o RUC del cliente.

        Returns:
            El objeto Cliente si existe, None en caso contrario.
        """
        id_buscada = identificacion.strip()
        for cliente in self._clientes:
            if cliente.identificacion == id_buscada:
                return cliente
        return None

    def _existe_identificacion_cliente(self, identificacion: str) -> bool:
        """
        Verifica si ya existe un cliente con la identificación dada.

        Método privado de apoyo para evitar duplicados.

        Args:
            identificacion: Identificación a verificar.

        Returns:
            True si ya existe, False en caso contrario.
        """
        return any(
            c.identificacion == identificacion.strip() for c in self._clientes
        )
