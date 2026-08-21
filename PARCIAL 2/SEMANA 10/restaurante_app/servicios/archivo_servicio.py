# -*- coding: utf-8 -*-
# servicios/archivo_servicio.py
# Semana 10 — Persistencia JSON, control de excepciones y modularidad.
#
# Principio SRP: esta clase se encarga exclusivamente de la lectura y escritura
# del archivo productos.json utilizando el módulo estándar `json` y manejando
# las excepciones específicas asociadas a la manipulación de archivos.

import json
import os
from typing import List, Dict, Any


class ArchivoServicio:
    """
    Servicio encargado de la persistencia física de productos en formato JSON.

    Concentra las operaciones de lectura (json.load) y escritura (json.dump)
    sobre el archivo `datos/productos.json` y gestiona de forma transparente
    las excepciones asociadas como FileNotFoundError, JSONDecodeError y PermissionError.
    """

    def __init__(self, ruta_archivo: str) -> None:
        """
        Constructor del servicio de archivos.

        Args:
            ruta_archivo: Ruta completa al archivo JSON de productos.
        """
        self._ruta_archivo = ruta_archivo
        self._asegurar_directorio()

    @property
    def ruta_archivo(self) -> str:
        """Retorna la ruta completa del archivo JSON asignado."""
        return self._ruta_archivo

    def _asegurar_directorio(self) -> None:
        """
        Garantiza que la carpeta contenedora exista antes de intentar
        operaciones de escritura.
        """
        directorio = os.path.dirname(self._ruta_archivo)
        if directorio and not os.path.exists(directorio):
            try:
                os.makedirs(directorio, exist_ok=True)
            except PermissionError:
                print(
                    f"\n  [ERROR] No hay permisos para crear la carpeta '{directorio}'."
                )

    def cargar_productos(self) -> List[Dict[str, Any]]:
        """
        Lee el archivo JSON de productos y devuelve la lista de diccionarios recuperada.

        Manejo de excepciones:
        - FileNotFoundError: Si el archivo no existe, no falla la aplicación y devuelve [].
        - json.JSONDecodeError: Si el contenido del archivo no es JSON válido, notifica y devuelve [].
        - PermissionError: Si no hay permisos de lectura, notifica y devuelve [].

        Returns:
            List[dict]: Lista de diccionarios que representan productos.
        """
        if not os.path.exists(self._ruta_archivo):
            print(
                f"\n  [INFO] El archivo '{os.path.basename(self._ruta_archivo)}' "
                f"no existe aún. Se iniciará con una colección vacía."
            )
            return []

        try:
            with open(self._ruta_archivo, "r", encoding="utf-8") as archivo:
                contenido = archivo.read().strip()
                if not contenido:
                    print(
                        f"\n  [AVISO] El archivo '{os.path.basename(self._ruta_archivo)}' "
                        f"está vacío. Se iniciará con colección vacía."
                    )
                    return []
                
                datos = json.loads(contenido)
                if isinstance(datos, list):
                    return datos
                else:
                    print(
                        f"\n  [AVISO] La estructura del JSON no es una lista válida. "
                        f"Se devolverá una colección vacía."
                    )
                    return []

        except FileNotFoundError:
            print(
                f"\n  [INFO] No se encontró el archivo '{self._ruta_archivo}'. "
                f"Iniciando con colección vacía."
            )
            return []
        except json.JSONDecodeError as err:
            print(
                f"\n  [ERROR DE LECTURA] El archivo '{os.path.basename(self._ruta_archivo)}' "
                f"contiene un formato JSON inválido o corrupto: {err}. "
                f"Se continuará con colección vacía para evitar detener el sistema."
            )
            return []
        except PermissionError:
            print(
                f"\n  [ERROR DE PERMISOS] Sin permisos suficientes para leer "
                f"el archivo '{self._ruta_archivo}'."
            )
            return []
        except OSError as err:
            print(
                f"\n  [ERROR I/O] Ocurrió un error de entrada/salida al leer "
                f"el archivo: {err}."
            )
            return []

    def guardar_productos(self, lista_dicts: List[Dict[str, Any]]) -> bool:
        """
        Guarda la lista de diccionarios de productos en el archivo JSON.

        Args:
            lista_dicts: Lista de diccionarios a serializar.

        Returns:
            bool: True si la escritura fue exitosa, False en caso de error.

        Manejo de excepciones:
        - PermissionError: Notifica si la escritura está bloqueada por permisos.
        - OSError: Captura fallos generales de I/O en disco.
        """
        try:
            with open(self._ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(lista_dicts, archivo, ensure_ascii=False, indent=4)
            return True
        except PermissionError:
            print(
                f"\n  [ERROR DE PERMISOS] No se pudo guardar. Sin permisos "
                f"de escritura en '{self._ruta_archivo}'."
            )
            return False
        except OSError as err:
            print(
                f"\n  [ERROR I/O] No se pudo guardar el archivo JSON: {err}."
            )
            return False
