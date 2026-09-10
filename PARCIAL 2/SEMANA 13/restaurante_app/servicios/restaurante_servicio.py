# -*- coding: utf-8 -*-
# servicios/restaurante_servicio.py
# Semana 13 — Transición a Interfaz Gráfica Tkinter (Base Restaurante)
#
# Principio SRP: Esta clase encapsula la lógica de negocio del restaurante,
# coordinando el modelo de datos (Producto, Usuario) y la persistencia (ArchivoServicio).

import os
from typing import List, Optional
from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """
    Servicio principal que gestiona las operaciones de negocio del restaurante.

    Mantiene colecciones en memoria de objetos Producto y Usuario, proporcionando
    métodos para validar acceso de usuarios, consultar productos, usuarios y métricas.
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

        Regla de simulación pedagógica:
        - El campo `usuario_o_id` se busca contra la `identificacion` (cédula), `correo` o `nombre`
          de los usuarios registrados.
        - La contraseña no puede estar vacía. Para propósitos del parcial, la simulación
          acepta credenciales si el usuario existe en el archivo usuarios.json y la clave no es vacía.

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
