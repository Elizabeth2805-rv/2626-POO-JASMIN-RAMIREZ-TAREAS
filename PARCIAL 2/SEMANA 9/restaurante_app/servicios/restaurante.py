# -*- coding: utf-8 -*-
# servicios/restaurante.py
# Semana 9 — Persistencia de datos en archivos JSON.
# Clonado y extendido desde PARCIAL 1 / SEMANA 8.
#
# Principio SRP: esta clase administra exclusivamente las colecciones de
# productos y clientes, y coordina la persistencia con el GestorJSON.
# No interactúa con la consola ni construye objetos de dominio directamente.
#
# Flujo de persistencia:
#   Al inicializar → carga productos y clientes desde los archivos JSON.
#   Al registrar / eliminar / actualizar → guarda el estado en los archivos JSON.
#
# Estructura de los archivos JSON (tipo diccionario):
#
#   productos.json:
#   [
#       {"tipo": "Producto", "codigo": "P001", "nombre": "...", ...},
#       {"tipo": "Bebida",   "codigo": "B001", "tamano": "...", ...}
#   ]
#
#   clientes.json:
#   [
#       {"identificacion": "123", "nombre": "...", "correo": "..."}
#   ]

import os
from typing import List, Optional

from modelos.producto import Producto
from modelos.bebida import Bebida
from modelos.cliente import Cliente
from almacenamiento.gestor_json import GestorJSON


class Restaurante:
    """
    Clase de servicio que administra las operaciones del restaurante
    con persistencia automática en archivos JSON.

    Responsabilidades:
    - Cargar productos y clientes desde archivos JSON al inicializar.
    - Registrar, listar, buscar, actualizar y eliminar productos.
    - Registrar y listar clientes.
    - Guardar el estado actualizado en los archivos JSON después de cada
      operación que modifique las colecciones.
    - Validar que no existan códigos de producto ni identificaciones
      de cliente duplicadas.

    Delega toda lectura/escritura de archivos al GestorJSON, manteniéndose
    desacoplado de los detalles del formato de almacenamiento.
    """

    def __init__(self, directorio_datos: str) -> None:
        """
        Constructor de la clase Restaurante.

        Inicializa el GestorJSON con la ruta de datos y carga las
        colecciones desde los archivos JSON existentes.

        Args:
            directorio_datos: Ruta al directorio donde se almacenan
                              los archivos productos.json y clientes.json.
        """
        self._gestor = GestorJSON(directorio_datos)
        self._productos: List[Producto] = []
        self._clientes: List[Cliente] = []
        self._cargar_datos()

    # ================================================================== #
    #  Carga inicial desde archivos JSON                                   #
    # ================================================================== #

    def _cargar_datos(self) -> None:
        """
        Lee los archivos JSON y reconstruye las colecciones de objetos
        usando los métodos from_dict() de cada clase.

        La clave 'tipo' del diccionario determina si el elemento debe
        reconstruirse como Producto o como Bebida.

        Los errores de reconstrucción individual se ignoran para que
        un dato corrupto no impida cargar el resto de la colección.
        """
        self._cargar_productos()
        self._cargar_clientes()

    def _cargar_productos(self) -> None:
        """
        Carga los productos desde productos.json.
        Reconstruye cada diccionario como Producto o Bebida
        según el valor de la clave 'tipo'.
        """
        lista_dicts = self._gestor.cargar_productos()
        for datos in lista_dicts:
            try:
                tipo = datos.get("tipo", "Producto")
                if tipo == "Bebida":
                    objeto = Bebida.from_dict(datos)
                else:
                    objeto = Producto.from_dict(datos)
                self._productos.append(objeto)
            except (KeyError, ValueError):
                # Registro corrupto: se omite sin detener la carga
                continue

    def _cargar_clientes(self) -> None:
        """
        Carga los clientes desde clientes.json.
        Reconstruye cada diccionario como un objeto Cliente.
        """
        lista_dicts = self._gestor.cargar_clientes()
        for datos in lista_dicts:
            try:
                cliente = Cliente.from_dict(datos)
                self._clientes.append(cliente)
            except (KeyError, ValueError):
                continue

    # ================================================================== #
    #  Guardado en archivos JSON                                           #
    # ================================================================== #

    def _guardar_productos(self) -> None:
        """
        Serializa cada producto/bebida de la colección a diccionario
        mediante to_dict() y los escribe en productos.json.
        """
        lista_dicts = [producto.to_dict() for producto in self._productos]
        self._gestor.guardar_productos(lista_dicts)

    def _guardar_clientes(self) -> None:
        """
        Serializa cada cliente de la colección a diccionario mediante
        to_dict() y los escribe en clientes.json.
        """
        lista_dicts = [cliente.to_dict() for cliente in self._clientes]
        self._gestor.guardar_clientes(lista_dicts)

    # ================================================================== #
    #  Métodos de Productos                                                #
    # ================================================================== #

    def registrar_producto(self, producto: Producto) -> None:
        """
        Registra un producto (o bebida) en la colección y guarda
        automáticamente el estado en el archivo JSON.

        Acepta cualquier objeto que sea instancia de Producto o de sus
        subclases (e.g., Bebida) gracias al principio LSP.

        Args:
            producto: Instancia de Producto o de cualquier subclase válida.

        Raises:
            TypeError:  Si el objeto no es instancia de Producto.
            ValueError: Si ya existe un producto con el mismo código.
        """
        if not isinstance(producto, Producto):
            raise TypeError(
                "Solo se pueden registrar instancias de Producto o sus subclases."
            )
        if self._existe_codigo_producto(producto.codigo):
            raise ValueError(
                f"Ya existe un producto con el código '{producto.codigo}'."
            )
        self._productos.append(producto)
        self._guardar_productos()   # Persistencia inmediata

    def listar_productos(self) -> List[Producto]:
        """
        Retorna una copia de la lista de productos registrados.

        Returns:
            Lista de objetos Producto/Bebida; vacía si no hay registros.
        """
        return list(self._productos)

    def buscar_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        """
        Busca un producto por su código único (búsqueda exacta).

        Args:
            codigo: Código del producto a buscar.

        Returns:
            El objeto Producto/Bebida si existe; None en caso contrario.
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
        Actualiza uno o más atributos de un producto existente y guarda
        los cambios en el archivo JSON.

        Solo se modifican los campos que se proporcionen (distintos de None).

        Args:
            codigo:          Código del producto a actualizar.
            nuevo_nombre:    Nuevo nombre (opcional).
            nueva_categoria: Nueva categoría (opcional).
            nuevo_precio:    Nuevo precio (opcional).

        Returns:
            True si el producto fue encontrado y actualizado.
            False si el código no corresponde a ningún producto registrado.

        Raises:
            ValueError: Si algún valor nuevo no supera las validaciones.
        """
        producto = self.buscar_producto_por_codigo(codigo)
        if producto is None:
            return False

        if nuevo_nombre is not None:
            producto.nombre = nuevo_nombre
        if nueva_categoria is not None:
            producto.categoria = nueva_categoria
        if nuevo_precio is not None:
            producto.precio = nuevo_precio

        self._guardar_productos()   # Persistencia inmediata
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        """
        Elimina un producto de la colección y actualiza el archivo JSON.

        Args:
            codigo: Código del producto a eliminar.

        Returns:
            True si fue encontrado y eliminado; False en caso contrario.
        """
        codigo_buscado = codigo.strip().upper()
        for indice, producto in enumerate(self._productos):
            if producto.codigo == codigo_buscado:
                self._productos.pop(indice)
                self._guardar_productos()   # Persistencia inmediata
                return True
        return False

    def _existe_codigo_producto(self, codigo: str) -> bool:
        """
        Verifica si ya existe un producto con el código indicado.

        Args:
            codigo: Código a verificar (ya normalizado a mayúsculas).

        Returns:
            True si el código existe; False en caso contrario.
        """
        return any(
            p.codigo == codigo.strip().upper() for p in self._productos
        )

    # ================================================================== #
    #  Métodos de Clientes                                                 #
    # ================================================================== #

    def registrar_cliente(self, cliente: Cliente) -> None:
        """
        Registra un cliente en la colección y guarda automáticamente
        el estado en el archivo JSON.

        Args:
            cliente: Instancia de la clase Cliente.

        Raises:
            TypeError:  Si el objeto no es instancia de Cliente.
            ValueError: Si ya existe un cliente con la misma identificación.
        """
        if not isinstance(cliente, Cliente):
            raise TypeError(
                "Solo se pueden registrar instancias de la clase Cliente."
            )
        if self._existe_identificacion_cliente(cliente.identificacion):
            raise ValueError(
                f"Ya existe un cliente con la identificación "
                f"'{cliente.identificacion}'."
            )
        self._clientes.append(cliente)
        self._guardar_clientes()    # Persistencia inmediata

    def listar_clientes(self) -> List[Cliente]:
        """
        Retorna una copia de la lista de clientes registrados.

        Returns:
            Lista de objetos Cliente; vacía si no hay registros.
        """
        return list(self._clientes)

    def buscar_cliente_por_id(self, identificacion: str) -> Optional[Cliente]:
        """
        Busca un cliente por su identificación única.

        Args:
            identificacion: Cédula o RUC del cliente.

        Returns:
            El objeto Cliente si existe; None en caso contrario.
        """
        id_buscada = identificacion.strip()
        for cliente in self._clientes:
            if cliente.identificacion == id_buscada:
                return cliente
        return None

    def _existe_identificacion_cliente(self, identificacion: str) -> bool:
        """
        Verifica si ya existe un cliente con la identificación indicada.

        Args:
            identificacion: Identificación a verificar.

        Returns:
            True si ya existe; False en caso contrario.
        """
        return any(
            c.identificacion == identificacion.strip() for c in self._clientes
        )
