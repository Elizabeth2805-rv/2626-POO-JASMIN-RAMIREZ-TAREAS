# -*- coding: utf-8 -*-
# servicios/archivo_servicio.py
# Semana 12 — Persistencia JSON, control de excepciones y modularidad.
#
# Principio SRP: esta clase se encarga exclusivamente de la lectura y escritura
# de archivos JSON (productos.json, usuarios.json y ventas.json) utilizando
# el módulo estándar `json` y manejando las excepciones específicas de I/O.

import json
import os
from typing import List, Dict, Any


class ArchivoServicio:
    """
    Servicio encargado de la persistencia física en formato JSON.

    Concentra las operaciones de lectura (json.load) y escritura (json.dump)
    sobre los archivos JSON del sistema y gestiona de forma transparente
    excepciones como FileNotFoundError, JSONDecodeError y PermissionError.
    """

    def __init__(self, directorio_datos: str = "datos") -> None:
        """
        Constructor del servicio de archivos.

        Args:
            directorio_datos: Ruta a la carpeta que contiene los archivos JSON.
        """
        self._directorio_datos = directorio_datos
        self._asegurar_directorio(self._directorio_datos)

    @property
    def directorio_datos(self) -> str:
        """Retorna la carpeta asignada para almacenar archivos JSON."""
        return self._directorio_datos

    def _asegurar_directorio(self, ruta_directorio: str) -> None:
        """
        Garantiza que la carpeta contenedora exista antes de intentar
        operaciones de lectura o escritura.
        """
        if ruta_directorio and not os.path.exists(ruta_directorio):
            try:
                os.makedirs(ruta_directorio, exist_ok=True)
            except PermissionError:
                print(
                    f"\n  [ERROR DE PERMISOS] No se puede crear la carpeta '{ruta_directorio}'."
                )

    def cargar_datos(self, ruta_archivo: str) -> List[Dict[str, Any]]:
        """
        Lee un archivo JSON y devuelve la lista de diccionarios recuperada.

        Manejo de excepciones:
        - FileNotFoundError: Si el archivo no existe, notifica e inicia con [].
        - json.JSONDecodeError: Si el archivo contiene JSON inválido, notifica e inicia con [].
        - PermissionError: Si no hay permisos de lectura, notifica e inicia con [].
        - OSError: Captura fallos de entrada/salida generales.

        Args:
            ruta_archivo: Ruta al archivo JSON.

        Returns:
            List[dict]: Lista de diccionarios recuperados del archivo.
        """
        nombre_base = os.path.basename(ruta_archivo)

        if not os.path.exists(ruta_archivo):
            print(
                f"  [INFO] El archivo '{nombre_base}' no existe aún. "
                f"Se iniciará con una colección vacía."
            )
            return []

        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                contenido = archivo.read().strip()
                if not contenido:
                    print(
                        f"  [AVISO] El archivo '{nombre_base}' está vacío. "
                        f"Se iniciará con colección vacía."
                    )
                    return []

                datos = json.loads(contenido)
                if isinstance(datos, list):
                    return datos
                else:
                    print(
                        f"  [AVISO] La estructura en '{nombre_base}' no es una lista válida. "
                        f"Se iniciará con colección vacía."
                    )
                    return []

        except FileNotFoundError:
            print(
                f"  [INFO] No se encontró el archivo '{nombre_base}'. "
                f"Iniciando con colección vacía."
            )
            return []
        except json.JSONDecodeError as err:
            print(
                f"  [ERROR DE LECTURA] El archivo '{nombre_base}' contiene "
                f"un formato JSON inválido o corrupto: {err}. "
                f"Se continuará con colección vacía para no detener el sistema."
            )
            return []
        except PermissionError:
            print(
                f"  [ERROR DE PERMISOS] Sin permisos suficientes para leer '{nombre_base}'."
            )
            return []
        except OSError as err:
            print(
                f"  [ERROR I/O] Error al leer el archivo '{nombre_base}': {err}."
            )
            return []

    def guardar_datos(self, ruta_archivo: str, lista_dicts: List[Dict[str, Any]]) -> bool:
        """
        Guarda la lista de diccionarios en un archivo JSON en formato estructurado.

        Args:
            ruta_archivo: Ruta completa al archivo JSON.
            lista_dicts:  Lista de diccionarios a serializar.

        Returns:
            bool: True si la escritura fue exitosa; False en caso contrario.

        Manejo de excepciones:
        - PermissionError: Notifica si la escritura está bloqueada.
        - OSError: Captura fallos generales de disco I/O.
        """
        directorio = os.path.dirname(ruta_archivo)
        if directorio:
            self._asegurar_directorio(directorio)

        try:
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(lista_dicts, archivo, ensure_ascii=False, indent=4)
            return True
        except PermissionError:
            print(
                f"  [ERROR DE PERMISOS] No se pudo guardar. Sin permisos de escritura en '{ruta_archivo}'."
            )
            return False
        except OSError as err:
            print(
                f"  [ERROR I/O] No se pudo guardar en '{ruta_archivo}': {err}."
            )
            return False

    # ------------------------------------------------------------------ #
    #  Métodos específicos para la aplicación                             #
    # ------------------------------------------------------------------ #
    def cargar_productos(self, ruta: str) -> List[Dict[str, Any]]:
        """Lee y devuelve los datos de productos.json."""
        return self.cargar_datos(ruta)

    def guardar_productos(self, ruta: str, lista_dicts: List[Dict[str, Any]]) -> bool:
        """Guarda la lista de diccionarios de productos en productos.json."""
        return self.guardar_datos(ruta, lista_dicts)

    def cargar_usuarios(self, ruta: str) -> List[Dict[str, Any]]:
        """Lee y devuelve los datos de usuarios.json."""
        return self.cargar_datos(ruta)

    def guardar_usuarios(self, ruta: str, lista_dicts: List[Dict[str, Any]]) -> bool:
        """Guarda la lista de diccionarios de usuarios en usuarios.json."""
        return self.guardar_datos(ruta, lista_dicts)

    def cargar_ventas(self, ruta: str) -> List[Dict[str, Any]]:
        """Lee y devuelve los datos de ventas.json."""
        return self.cargar_datos(ruta)

    def guardar_ventas(self, ruta: str, lista_dicts: List[Dict[str, Any]]) -> bool:
        """Guarda la lista de diccionarios de ventas en ventas.json."""
        return self.guardar_datos(ruta, lista_dicts)
