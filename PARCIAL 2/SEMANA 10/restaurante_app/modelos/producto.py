# -*- coding: utf-8 -*-
# modelos/producto.py
# Semana 10 — Persistencia JSON, excepciones y modularidad.
#
# Principio SRP: esta clase es exclusivamente responsable de representar
# la información, validación y serialización de un producto del restaurante.
# No administra colecciones ni realiza operaciones de I/O de archivos.

from typing import Dict, Any


class Producto:
    """
    Clase que representa un Producto del restaurante.

    Aplica SRP: su responsabilidad se limita a gestionar los datos y
    validaciones de un producto, además de permitir la conversión entre
    instancia de objeto y diccionario compatible con formato JSON.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
    ) -> None:
        """
        Constructor de la clase Producto.

        Args:
            codigo:    Identificador único del producto (e.g., 'P001').
            nombre:    Nombre descriptivo del producto.
            categoria: Categoría del producto (e.g., 'Plato Fuerte').
            precio:    Precio unitario. Debe ser mayor que cero.

        Raises:
            ValueError: Si alguna validación de los atributos falla.
        """
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio

    # ------------------------------------------------------------------ #
    #  Getter / Setter: codigo                                             #
    # ------------------------------------------------------------------ #
    @property
    def codigo(self) -> str:
        """Retorna el código único del producto."""
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        self._codigo = valor.strip().upper()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: nombre                                             #
    # ------------------------------------------------------------------ #
    @property
    def nombre(self) -> str:
        """Retorna el nombre del producto."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: categoria                                          #
    # ------------------------------------------------------------------ #
    @property
    def categoria(self) -> str:
        """Retorna la categoría del producto."""
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        self._categoria = valor.strip()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: precio                                             #
    # ------------------------------------------------------------------ #
    @property
    def precio(self) -> float:
        """Retorna el precio del producto."""
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        try:
            valor_num = float(valor)
        except (ValueError, TypeError):
            raise ValueError("El precio debe ser un número válido.")
        if valor_num <= 0:
            raise ValueError("El precio del producto debe ser mayor que cero.")
        self._precio = valor_num

    # ------------------------------------------------------------------ #
    #  Conversión a diccionario (Serialización JSON)                      #
    # ------------------------------------------------------------------ #
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto Producto a un diccionario compatible con JSON.

        Returns:
            dict con la información estructurada del producto.
        """
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
        }

    # ------------------------------------------------------------------ #
    #  Reconstrucción desde diccionario (Deserialización JSON)            #
    # ------------------------------------------------------------------ #
    @classmethod
    def from_dict(cls, datos: Dict[str, Any]) -> "Producto":
        """
        Reconstruye una instancia de Producto a partir de un diccionario.

        Args:
            datos: Diccionario que debe contener las claves 'codigo',
                   'nombre', 'categoria' y 'precio'.

        Returns:
            Nueva instancia de Producto.

        Raises:
            KeyError:   Si falta alguna clave obligatoria en el diccionario.
            ValueError: Si algún valor no cumple las validaciones de Producto.
        """
        claves_requeridas = ("codigo", "nombre", "categoria", "precio")
        for clave in claves_requeridas:
            if clave not in datos:
                raise KeyError(
                    f"El diccionario no contiene la clave requerida '{clave}'."
                )

        return cls(
            codigo=str(datos["codigo"]),
            nombre=str(datos["nombre"]),
            categoria=str(datos["categoria"]),
            precio=datos["precio"],
        )

    # ------------------------------------------------------------------ #
    #  Representación en consola                                          #
    # ------------------------------------------------------------------ #
    def mostrar_informacion(self) -> None:
        """Muestra la información del producto formateada en consola."""
        print(f"  [Producto] Código   : {self.codigo}")
        print(f"             Nombre   : {self.nombre}")
        print(f"             Categoría: {self.categoria}")
        print(f"             Precio   : ${self.precio:.2f}")
        print("  " + "-" * 44)

    def __str__(self) -> str:
        return (
            f"Producto(codigo={self.codigo!r}, nombre={self.nombre!r}, "
            f"categoria={self.categoria!r}, precio={self.precio:.2f})"
        )
