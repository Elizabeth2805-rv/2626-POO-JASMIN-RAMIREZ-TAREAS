# -*- coding: utf-8 -*-
# modelos/usuario.py
# Semana 9 — Estructuras de datos en Python.
#
# Responsabilidad única (SRP): esta clase se encarga exclusivamente de
# representar la información general de una persona registrada en el sistema.
# No administra colecciones ni contiene lógica de negocio.
#
# Nota de diseño: Usuario es una entidad general. En semanas posteriores
# podrá evolucionar hacia subclases como Cliente, Empleado o Administrador
# mediante herencia, sin necesidad de modificar esta clase base.


class Usuario:
    """
    Clase que representa a un Usuario registrado en el sistema del restaurante.

    Almacena y valida la información básica de identificación de una persona:
    identificación única, nombre completo y correo electrónico.

    Esta clase es intencional mente general para que el sistema pueda
    evolucionar hacia distintos tipos de usuarios sin modificar su base.
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
            identificacion: Número de cédula o identificador único del usuario.
            nombre:         Nombre completo de la persona registrada.
            correo:         Dirección de correo electrónico de contacto.
        """
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    # ------------------------------------------------------------------ #
    #  Getter / Setter: identificacion                                     #
    # ------------------------------------------------------------------ #
    @property
    def identificacion(self) -> str:
        """Retorna la identificación única del usuario."""
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
        """Retorna el nombre completo del usuario."""
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
            raise ValueError(
                "El correo electrónico ingresado no tiene un formato válido."
            )
        self._correo = valor.strip().lower()

    # ------------------------------------------------------------------ #
    #  Método: mostrar_informacion                                         #
    # ------------------------------------------------------------------ #
    def mostrar_informacion(self) -> None:
        """Muestra los datos del usuario con formato legible en consola."""
        print(f"  [Usuario]  ID       : {self.identificacion}")
        print(f"             Nombre   : {self.nombre}")
        print(f"             Correo   : {self.correo}")
        print("  " + "-" * 44)

    def __str__(self) -> str:
        return (
            f"Usuario(identificacion={self.identificacion!r}, "
            f"nombre={self.nombre!r}, correo={self.correo!r})"
        )
