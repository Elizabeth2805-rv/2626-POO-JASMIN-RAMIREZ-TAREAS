# -*- coding: utf-8 -*-
# modelos/producto.py
# Clonado desde PARCIAL 1 / SEMANA 8 — Semana 9 agrega persistencia JSON.
#
# Principio SRP: esta clase es exclusivamente responsable de representar
# la información y el comportamiento de un producto del restaurante.
# No administra colecciones ni interactúa con archivos o consola.


class Producto:
    """
    Clase base que representa un Producto general del restaurante.

    Aplica SRP: su única responsabilidad es contener y exponer la
    información de un producto (código, nombre, categoría, precio).

    Aplica OCP: está abierta para extenderse mediante herencia (e.g., Bebida)
    sin necesidad de modificarla cuando se añaden nuevos tipos de producto.

    Incorpora el método to_dict() para serializar el objeto como diccionario
    compatible con JSON, y el método de clase from_dict() para reconstruirlo.
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
            categoria: Categoría a la que pertenece (e.g., 'Plato Fuerte').
            precio:    Precio unitario. Debe ser mayor que cero.
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
        """Retorna el código identificador del producto."""
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
        """Retorna el precio unitario del producto."""
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        try:
            valor_num = float(valor)
        except (ValueError, TypeError):
            raise ValueError("El precio debe ser un valor numérico válido.")
        if valor_num <= 0:
            raise ValueError("El precio del producto debe ser mayor que cero.")
        self._precio = valor_num

    # ------------------------------------------------------------------ #
    #  Serialización / Deserialización JSON (estructura diccionario)       #
    # ------------------------------------------------------------------ #
    def to_dict(self) -> dict:
        """
        Convierte el objeto Producto a un diccionario serializable en JSON.

        La clave 'tipo' permite identificar la clase concreta al momento
        de deserializar, distinguiendo entre Producto y Bebida.

        Returns:
            dict con todos los atributos del producto.
        """
        return {
            "tipo": "Producto",
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Producto":
        """
        Crea una instancia de Producto a partir de un diccionario.

        Args:
            datos: Diccionario con las claves 'codigo', 'nombre',
                   'categoria' y 'precio'.

        Returns:
            Nueva instancia de Producto reconstruida desde el diccionario.

        Raises:
            KeyError: Si falta alguna clave obligatoria en el diccionario.
            ValueError: Si algún valor no supera las validaciones.
        """
        return cls(
            codigo=datos["codigo"],
            nombre=datos["nombre"],
            categoria=datos["categoria"],
            precio=datos["precio"],
        )

    # ------------------------------------------------------------------ #
    #  Método: mostrar_informacion                                         #
    # ------------------------------------------------------------------ #
    def mostrar_informacion(self) -> None:
        """Muestra los datos del producto con formato legible en consola."""
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
