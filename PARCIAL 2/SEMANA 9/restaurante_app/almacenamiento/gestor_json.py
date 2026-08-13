# -*- coding: utf-8 -*-
# almacenamiento/gestor_json.py
# Semana 9 — Persistencia de datos en archivos JSON.
#
# Responsabilidad única (SRP): este módulo es exclusivamente responsable
# de leer y escribir datos en archivos JSON. No contiene lógica de negocio,
# no construye objetos de dominio directamente y no interactúa con la consola.
#
# Los datos se almacenan como listas de diccionarios:
#
#   productos.json → lista de dicts con la estructura:
#       {"tipo": "Producto", "codigo": "P001", "nombre": "...", ...}
#       {"tipo": "Bebida",   "codigo": "B001", "tamano": "...", ...}
#
#   clientes.json → lista de dicts con la estructura:
#       {"identificacion": "12345", "nombre": "...", "correo": "..."}

import json
import os
from typing import List


class GestorJSON:
    """
    Clase responsable de la persistencia de datos en archivos JSON.

    Gestiona dos archivos independientes:
    - productos.json: almacena la lista de productos y bebidas.
    - clientes.json:  almacena la lista de clientes.

    Cada objeto se serializa como un diccionario (estructura clave → valor)
    y se guarda dentro de una lista JSON en el archivo correspondiente.
    """

    def __init__(self, directorio_datos: str) -> None:
        """
        Constructor del GestorJSON.

        Args:
            directorio_datos: Ruta absoluta al directorio donde se guardarán
                              los archivos JSON. Se crea si no existe.
        """
        self._directorio_datos = directorio_datos
        self._ruta_productos = os.path.join(directorio_datos, "productos.json")
        self._ruta_clientes = os.path.join(directorio_datos, "clientes.json")
        self._asegurar_directorio()

    # ------------------------------------------------------------------ #
    #  Métodos privados de soporte                                         #
    # ------------------------------------------------------------------ #
    def _asegurar_directorio(self) -> None:
        """
        Crea el directorio de datos si no existe.
        Garantiza que los archivos JSON siempre tengan una ubicación válida.
        """
        os.makedirs(self._directorio_datos, exist_ok=True)

    def _leer_archivo(self, ruta: str) -> List[dict]:
        """
        Lee un archivo JSON y retorna su contenido como lista de diccionarios.

        Si el archivo no existe o está vacío o contiene datos no válidos,
        retorna una lista vacía sin detener el programa.

        Args:
            ruta: Ruta completa al archivo JSON.

        Returns:
            Lista de diccionarios leídos del archivo; lista vacía si hay error.
        """
        if not os.path.exists(ruta):
            return []
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                contenido = archivo.read().strip()
                if not contenido:
                    return []
                datos = json.loads(contenido)
                if isinstance(datos, list):
                    return datos
                return []
        except (json.JSONDecodeError, OSError):
            return []

    def _escribir_archivo(self, ruta: str, datos: List[dict]) -> None:
        """
        Escribe una lista de diccionarios en un archivo JSON con formato
        indentado para facilitar la lectura humana del archivo.

        Args:
            ruta:  Ruta completa al archivo JSON de destino.
            datos: Lista de diccionarios a serializar y escribir.

        Raises:
            OSError: Si el archivo no puede abrirse para escritura.
        """
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)

    # ------------------------------------------------------------------ #
    #  Operaciones sobre productos                                         #
    # ------------------------------------------------------------------ #
    def cargar_productos(self) -> List[dict]:
        """
        Lee el archivo productos.json y retorna la lista de diccionarios
        correspondiente a los productos y bebidas almacenados.

        El servicio Restaurante utiliza estos diccionarios para reconstruir
        los objetos Producto o Bebida mediante sus métodos from_dict().

        Returns:
            Lista de dicts; cada dict representa un producto o bebida.
        """
        return self._leer_archivo(self._ruta_productos)

    def guardar_productos(self, lista_dicts: List[dict]) -> None:
        """
        Escribe la lista de diccionarios de productos en productos.json.

        El servicio Restaurante convierte cada objeto Producto/Bebida a
        diccionario con to_dict() antes de invocar este método.

        Args:
            lista_dicts: Lista de dicts; cada dict representa un producto
                         o bebida serializado.
        """
        self._escribir_archivo(self._ruta_productos, lista_dicts)

    # ------------------------------------------------------------------ #
    #  Operaciones sobre clientes                                          #
    # ------------------------------------------------------------------ #
    def cargar_clientes(self) -> List[dict]:
        """
        Lee el archivo clientes.json y retorna la lista de diccionarios
        correspondiente a los clientes almacenados.

        El servicio Restaurante utiliza estos diccionarios para reconstruir
        los objetos Cliente mediante Cliente.from_dict().

        Returns:
            Lista de dicts; cada dict representa un cliente.
        """
        return self._leer_archivo(self._ruta_clientes)

    def guardar_clientes(self, lista_dicts: List[dict]) -> None:
        """
        Escribe la lista de diccionarios de clientes en clientes.json.

        El servicio Restaurante convierte cada objeto Cliente a diccionario
        con to_dict() antes de invocar este método.

        Args:
            lista_dicts: Lista de dicts; cada dict representa un cliente
                         serializado.
        """
        self._escribir_archivo(self._ruta_clientes, lista_dicts)
