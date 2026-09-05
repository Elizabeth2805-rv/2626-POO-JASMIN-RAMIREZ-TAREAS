# -*- coding: utf-8 -*-
# modelos/venta.py
# Semana 12 — Rendimiento mediante colecciones, índices y persistencia JSON.
#
# Principio SRP: esta clase es exclusivamente responsable de representar
# la transacción de una venta entre un usuario registrado y un producto.

from typing import Dict, Any


class Venta:
    """
    Clase que representa la relación y transacción de Venta entre un Usuario y un Producto.

    Almacena el ID del usuario comprador, el código del producto adquirido
    y la cantidad comprada.
    """

    def __init__(
        self,
        usuario_id: str,
        producto_codigo: str,
        cantidad: int,
    ) -> None:
        """
        Constructor de la clase Venta.

        Args:
            usuario_id:      Identificación (ID/cédula) del usuario que compra.
            producto_codigo: Código único del producto comprado.
            cantidad:        Cantidad de unidades vendidas.

        Raises:
            ValueError: Si alguno de los argumentos no cumple con las validaciones.
        """
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad

    # ------------------------------------------------------------------ #
    #  Getter / Setter: usuario_id                                         #
    # ------------------------------------------------------------------ #
    @property
    def usuario_id(self) -> str:
        """Retorna la identificación del usuario comprador."""
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        self._usuario_id = valor.strip()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: producto_codigo                                    #
    # ------------------------------------------------------------------ #
    @property
    def producto_codigo(self) -> str:
        """Retorna el código del producto vendido."""
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        self._producto_codigo = valor.strip().upper()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: cantidad                                           #
    # ------------------------------------------------------------------ #
    @property
    def cantidad(self) -> int:
        """Retorna la cantidad vendida."""
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        try:
            cant_int = int(valor)
        except (ValueError, TypeError):
            raise ValueError("La cantidad vendida debe ser un número entero.")
        if cant_int <= 0:
            raise ValueError("La cantidad vendida debe ser mayor que cero.")
        self._cantidad = cant_int

    # ------------------------------------------------------------------ #
    #  Conversión a diccionario (Serialización JSON)                      #
    # ------------------------------------------------------------------ #
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto Venta a un diccionario compatible con JSON.

        Returns:
            dict con la información estructurada de la venta.
        """
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
        }

    # ------------------------------------------------------------------ #
    #  Reconstrucción desde diccionario (Deserialización JSON)            #
    # ------------------------------------------------------------------ #
    @classmethod
    def from_dict(cls, datos: Dict[str, Any]) -> "Venta":
        """
        Reconstruye una instancia de Venta a partir de un diccionario.

        Args:
            datos: Diccionario que debe contener 'usuario_id',
                   'producto_codigo' y 'cantidad'.

        Returns:
            Nueva instancia de Venta.

        Raises:
            KeyError:   Si falta alguna clave obligatoria.
            ValueError: Si algún valor no cumple las validaciones de Venta.
        """
        claves_requeridas = ("usuario_id", "producto_codigo", "cantidad")
        for clave in claves_requeridas:
            if clave not in datos:
                raise KeyError(
                    f"El diccionario no contiene la clave requerida '{clave}'."
                )

        return cls(
            usuario_id=str(datos["usuario_id"]),
            producto_codigo=str(datos["producto_codigo"]),
            cantidad=datos["cantidad"],
        )

    # ------------------------------------------------------------------ #
    #  Representación en consola                                          #
    # ------------------------------------------------------------------ #
    def mostrar_informacion(self) -> None:
        """Muestra la información formateada de la venta en consola."""
        print(f"  [Venta] ID Usuario     : {self.usuario_id}")
        print(f"          Código Producto: {self.producto_codigo}")
        print(f"          Cantidad       : {self.cantidad} unidad(es)")
        print("  " + "-" * 44)

    def __str__(self) -> str:
        return (
            f"Venta(usuario_id={self.usuario_id!r}, "
            f"producto_codigo={self.producto_codigo!r}, "
            f"cantidad={self.cantidad})"
        )
