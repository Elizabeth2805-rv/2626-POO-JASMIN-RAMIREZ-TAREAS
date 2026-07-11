# -*- coding: utf-8 -*-
# servicios/restaurante.py

from typing import List, Optional
from modelos.producto import Producto
from modelos.cliente import Cliente

class Restaurante:
    """
    Clase de Servicio que implementa la lógica de negocio para la administración
    del restaurante. Se encarga de gestionar el almacenamiento en memoria y las búsquedas.
    De acuerdo con la Arquitectura en Capas, esta clase no interactúa con la consola directamente,
    sino que recibe y retorna objetos y colecciones.
    """

    def __init__(self):
        # Listas para almacenar los objetos creados
        self._productos: List[Producto] = []
        self._clientes: List[Cliente] = []

    # --- MÉTODOS PARA PRODUCTOS ---

    def registrar_producto(self, producto: Producto) -> None:
        """
        Agrega un nuevo producto a la lista del restaurante.
        Valida que el parámetro recibido sea una instancia válida de Producto.
        """
        if not isinstance(producto, Producto):
            raise TypeError("Error de Servicio: El objeto a registrar debe ser una instancia de la clase Producto.")
        self._productos.append(producto)

    def listar_productos(self) -> List[Producto]:
        """
        Retorna la lista completa de productos registrados en el sistema.
        """
        return self._productos

    def buscar_producto(self, nombre: str) -> List[Producto]:
        """
        Busca productos en la lista cuyo nombre coincida parcialmente (sin importar mayúsculas/minúsculas).
        Retorna una lista de productos coincidentes.
        """
        nombre_buscar = nombre.strip().lower()
        if not nombre_buscar:
            return []
        
        # Filtramos los productos que contienen la subcadena
        return [p for p in self._productos if nombre_buscar in p.nombre.lower()]


    # --- MÉTODOS PARA CLIENTES ---

    def registrar_cliente(self, cliente: Cliente) -> None:
        """
        Registra un cliente en el sistema del restaurante.
        Valida que sea una instancia de la clase de datos Cliente.
        """
        if not isinstance(cliente, Cliente):
            raise TypeError("Error de Servicio: El objeto a registrar debe ser una instancia de la clase Cliente.")
        
        # Opcional: Validar que el ID del cliente no esté duplicado
        for c in self._clientes:
            if c.id_cliente == cliente.id_cliente:
                raise ValueError(f"Error de Servicio: Ya existe un cliente registrado con el ID '{cliente.id_cliente}'.")
                
        self._clientes.append(cliente)

    def listar_clientes(self) -> List[Cliente]:
        """
        Retorna la lista completa de clientes registrados.
        """
        return self._clientes

    def buscar_cliente(self, id_cliente: str) -> Optional[Cliente]:
        """
        Busca un cliente por su ID único (búsqueda exacta).
        Retorna el objeto Cliente si se encuentra, de lo contrario retorna None.
        """
        id_buscar = id_cliente.strip()
        for cliente in self._clientes:
            if cliente.id_cliente == id_buscar:
                return cliente
        return None
