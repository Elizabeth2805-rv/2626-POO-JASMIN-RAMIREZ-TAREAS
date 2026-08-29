# -*- coding: utf-8 -*-
# modelos/producto.py
# Semana 11 — Colecciones, relaciones, ventas y persistencia JSON.
#
# Principio SRP: esta clase es exclusivamente responsable de representar
# la información, validación, control de stock y serialización de un producto del restaurante.

from typing import Dict, Any


class Producto:
    """
    Clase que representa un Producto del restaurante.

    Aplica SRP: su responsabilidad se limita a gestionar los datos, validaciones,
    el stock disponible del producto y permitir la conversión entre la instancia
    de objeto y un diccionario compatible con formato JSON.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int = 0,
    ) -> None:
        """
        Constructor de la clase Producto.

        Args:
            codigo:    Identificador único del producto (e.g., 'P001').
            nombre:    Nombre descriptivo del producto.
            categoria: Categoría del producto (e.g., 'Plato Fuerte').
            precio:    Precio unitario (debe ser mayor que cero).
            stock:     Cantidad disponible en inventario (debe ser >= 0).

        Raises:
            ValueError: Si alguna validación de los atributos falla.
        """
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

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
    #  Getter / Setter: stock                                              #
    # ------------------------------------------------------------------ #
    @property
    def stock(self) -> int:
        """Retorna la cantidad disponible en stock."""
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        try:
            valor_int = int(valor)
        except (ValueError, TypeError):
            raise ValueError("El stock debe ser un número entero válido.")
        if valor_int < 0:
            raise ValueError("El stock del producto no puede ser negativo.")
        self._stock = valor_int

    # ------------------------------------------------------------------ #
    #  Operación de venta de stock                                        #
    # ------------------------------------------------------------------ #
    def vender(self, cantidad: int) -> None:
        """
        Disminuye la cantidad solicitada del stock disponible.

        Args:
            cantidad: Cantidad a descontar del stock (debe ser > 0 y <= stock actual).

        Raises:
            ValueError: Si la cantidad no es válida o supera el stock disponible.
        """
        try:
            cant_int = int(cantidad)
        except (ValueError, TypeError):
            raise ValueError("La cantidad a vender debe ser un número entero.")

        if cant_int <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero.")

        if cant_int > self._stock:
            raise ValueError(
                f"Stock insuficiente para '{self.nombre}'. "
                f"Disponible: {self._stock}, Solicitado: {cant_int}."
            )

        self._stock -= cant_int

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
            "stock": self.stock,
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
                   'nombre', 'categoria', 'precio' y 'stock'.

        Returns:
            Nueva instancia de Producto.

        Raises:
            KeyError:   Si falta alguna clave obligatoria en el diccionario.
            ValueError: Si algún valor no cumple las validaciones de Producto.
        """
        claves_requeridas = ("codigo", "nombre", "categoria", "precio", "stock")
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
            stock=datos["stock"],
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
        print(f"             Stock    : {self.stock} unidad(es)")
        print("  " + "-" * 44)

    def __str__(self) -> str:
        return (
            f"Producto(codigo={self.codigo!r}, nombre={self.nombre!r}, "
            f"categoria={self.categoria!r}, precio={self.precio:.2f}, "
            f"stock={self.stock})"
        )
