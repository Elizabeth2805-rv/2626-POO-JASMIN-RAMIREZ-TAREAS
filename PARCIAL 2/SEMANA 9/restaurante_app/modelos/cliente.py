# -*- coding: utf-8 -*-
# modelos/cliente.py
# Clonado desde PARCIAL 1 / SEMANA 8 — Semana 9 agrega persistencia JSON.
#
# Principio SRP: esta clase es exclusivamente responsable de representar
# la información de un cliente del restaurante.


class Cliente:
    """
    Clase que representa a un Cliente registrado en el restaurante.

    Aplica SRP: su única responsabilidad es contener y exponer los datos
    de un cliente. No administra colecciones ni interactúa con archivos.

    Incorpora to_dict() para serializar el objeto como diccionario compatible
    con JSON, y from_dict() para reconstruirlo a partir de un diccionario.
    """

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
    ) -> None:
        """
        Constructor de la clase Cliente.

        Args:
            identificacion: Número de cédula o RUC único del cliente.
            nombre:         Nombre completo del cliente.
            correo:         Correo electrónico de contacto.
        """
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    # ------------------------------------------------------------------ #
    #  Getter / Setter: identificacion                                     #
    # ------------------------------------------------------------------ #
    @property
    def identificacion(self) -> str:
        """Retorna la identificación única del cliente."""
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La identificación del cliente no puede estar vacía.")
        self._identificacion = valor.strip()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: nombre                                             #
    # ------------------------------------------------------------------ #
    @property
    def nombre(self) -> str:
        """Retorna el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        self._nombre = valor.strip()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: correo                                             #
    # ------------------------------------------------------------------ #
    @property
    def correo(self) -> str:
        """Retorna el correo electrónico del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El correo del cliente no puede estar vacío.")
        if "@" not in valor or "." not in valor.split("@")[-1]:
            raise ValueError(
                "El correo electrónico ingresado no tiene un formato válido."
            )
        self._correo = valor.strip().lower()

    # ------------------------------------------------------------------ #
    #  Serialización / Deserialización JSON (estructura diccionario)       #
    # ------------------------------------------------------------------ #
    def to_dict(self) -> dict:
        """
        Convierte el objeto Cliente a un diccionario serializable en JSON.

        Returns:
            dict con todos los atributos del cliente.
        """
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Cliente":
        """
        Crea una instancia de Cliente a partir de un diccionario.

        Args:
            datos: Diccionario con las claves 'identificacion',
                   'nombre' y 'correo'.

        Returns:
            Nueva instancia de Cliente reconstruida desde el diccionario.
        """
        return cls(
            identificacion=datos["identificacion"],
            nombre=datos["nombre"],
            correo=datos["correo"],
        )

    # ------------------------------------------------------------------ #
    #  Método: mostrar_informacion                                         #
    # ------------------------------------------------------------------ #
    def mostrar_informacion(self) -> None:
        """Muestra los datos del cliente formateados en consola."""
        print(f"  [Cliente]  ID       : {self.identificacion}")
        print(f"             Nombre   : {self.nombre}")
        print(f"             Correo   : {self.correo}")
        print("  " + "-" * 44)

    def __str__(self) -> str:
        return (
            f"Cliente(identificacion={self.identificacion!r}, "
            f"nombre={self.nombre!r}, correo={self.correo!r})"
        )
