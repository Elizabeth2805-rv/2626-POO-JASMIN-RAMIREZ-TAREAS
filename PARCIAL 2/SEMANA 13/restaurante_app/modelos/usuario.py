# -*- coding: utf-8 -*-
# modelos/usuario.py
# Semana 13 — Transición a Interfaz Gráfica Tkinter (Base Restaurante)
#
# Principio SRP: Esta clase representa la información, validaciones y serialización
# JSON de un usuario del restaurante.

from typing import Dict, Any


class Usuario:
    """
    Clase que representa a un Usuario del sistema del restaurante.

    Almacena la información de identificación, nombre completo y correo electrónico.
    Permite métodos to_dict() y from_dict() para almacenamiento y reconstrucción
    desde el archivo usuarios.json.
    """

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
    ) -> None:
        """
        Constructor de la clase Usuario.

        Args:
            identificacion: Cédula o número de identificación único del usuario.
            nombre:         Nombre completo del usuario.
            correo:         Correo electrónico del usuario.

        Raises:
            ValueError: Si algún valor ingresado no supera las validaciones.
        """
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    # ------------------------------------------------------------------ #
    #  Getter / Setter: identificacion                                     #
    # ------------------------------------------------------------------ #
    @property
    def identificacion(self) -> str:
        """Retorna la identificación del usuario."""
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        self._identificacion = valor.strip()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: nombre                                             #
    # ------------------------------------------------------------------ #
    @property
    def nombre(self) -> str:
        """Retorna el nombre del usuario."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        self._nombre = valor.strip()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: correo                                             #
    # ------------------------------------------------------------------ #
    @property
    def correo(self) -> str:
        """Retorna el correo electrónico del usuario."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El correo del usuario no puede estar vacío.")
        if "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValueError("El correo electrónico no tiene un formato válido.")
        self._correo = valor.strip().lower()

    # ------------------------------------------------------------------ #
    #  Conversión a diccionario (Serialización JSON)                      #
    # ------------------------------------------------------------------ #
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto Usuario a un diccionario compatible con JSON.

        Returns:
            dict con la información estructurada del usuario.
        """
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
        }

    # ------------------------------------------------------------------ #
    #  Reconstrucción desde diccionario (Deserialización JSON)            #
    # ------------------------------------------------------------------ #
    @classmethod
    def from_dict(cls, datos: Dict[str, Any]) -> "Usuario":
        """
        Reconstruye una instancia de Usuario a partir de un diccionario.

        Args:
            datos: Diccionario que debe contener las claves 'identificacion',
                   'nombre' y 'correo'.

        Returns:
            Nueva instancia de Usuario.

        Raises:
            KeyError:   Si falta alguna clave obligatoria en el diccionario.
            ValueError: Si algún valor no cumple las validaciones de Usuario.
        """
        claves_requeridas = ("identificacion", "nombre", "correo")
        for clave in claves_requeridas:
            if clave not in datos:
                raise KeyError(
                    f"El diccionario no contiene la clave requerida '{clave}'."
                )

        return cls(
            identificacion=str(datos["identificacion"]),
            nombre=str(datos["nombre"]),
            correo=str(datos["correo"]),
        )

    def __str__(self) -> str:
        return (
            f"Usuario(identificacion={self.identificacion!r}, "
            f"nombre={self.nombre!r}, correo={self.correo!r})"
        )
