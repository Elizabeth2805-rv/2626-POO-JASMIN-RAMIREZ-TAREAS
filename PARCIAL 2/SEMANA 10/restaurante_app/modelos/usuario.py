# -*- coding: utf-8 -*-
# modelos/usuario.py
# Semana 10 — Entidad general de Usuario (almacenada en memoria).
#
# Responsabilidad única (SRP): esta clase representa la información y validaciones
# de un usuario del restaurante. Permanece en memoria durante esta semana.

class Usuario:
    """
    Clase que representa a un Usuario del sistema del restaurante.

    Almacena la información de identificación, nombre completo y correo electrónico.
    En esta semana se mantiene únicamente en memoria.
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
    #  Representación en consola                                          #
    # ------------------------------------------------------------------ #
    def mostrar_informacion(self) -> None:
        """Muestra la información del usuario en consola."""
        print(f"  [Usuario]  ID       : {self.identificacion}")
        print(f"             Nombre   : {self.nombre}")
        print(f"             Correo   : {self.correo}")
        print("  " + "-" * 44)

    def __str__(self) -> str:
        return (
            f"Usuario(identificacion={self.identificacion!r}, "
            f"nombre={self.nombre!r}, correo={self.correo!r})"
        )
