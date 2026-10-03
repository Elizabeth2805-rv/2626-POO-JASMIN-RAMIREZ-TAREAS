# -*- coding: utf-8 -*-
# modelos/venta.py
# Semana 15 — Conceptos fundamentales de manejo de eventos (Evolución Restaurante App)
#
# Principio SRP: Esta clase representa los datos, relaciones, fecha y validaciones
# de una Venta realizada en el restaurante.

from typing import Dict, Any


class Venta:
    """
    Clase que representa una Venta del restaurante.

    Relaciona un usuario (mediante su identificación) con un producto
    (mediante su código), registrando la fecha/hora de la transacción y el monto total.
    """

    def __init__(
        self,
        id_venta: str,
        identificacion_usuario: str,
        codigo_producto: str,
        fecha: str,
        total: float,
    ) -> None:
        """
        Constructor de la clase Venta.

        Args:
            id_venta:               Código o identificador único de la venta (e.g., 'V001').
            identificacion_usuario: Cédula / ID del usuario comprador.
            codigo_producto:        Código del producto vendido.
            fecha:                  Fecha y hora en formato legible (e.g., '2026-09-26 14:30:00').
            total:                  Monto total de la venta ($).

        Raises:
            ValueError: Si alguna validación de atributos falla.
        """
        self.id_venta = id_venta
        self.identificacion_usuario = identificacion_usuario
        self.codigo_producto = codigo_producto
        self.fecha = fecha
        self.total = total

    # ------------------------------------------------------------------ #
    #  Getter / Setter: id_venta                                         #
    # ------------------------------------------------------------------ #
    @property
    def id_venta(self) -> str:
        """Retorna el código único de la venta."""
        return self._id_venta

    @id_venta.setter
    def id_venta(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El ID de la venta no puede estar vacío.")
        self._id_venta = valor.strip().upper()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: identificacion_usuario                           #
    # ------------------------------------------------------------------ #
    @property
    def identificacion_usuario(self) -> str:
        """Retorna la identificación del usuario comprador."""
        return self._identificacion_usuario

    @identificacion_usuario.setter
    def identificacion_usuario(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        self._identificacion_usuario = valor.strip()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: codigo_producto                                  #
    # ------------------------------------------------------------------ #
    @property
    def codigo_producto(self) -> str:
        """Retorna el código del producto vendido."""
        return self._codigo_producto

    @codigo_producto.setter
    def codigo_producto(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        self._codigo_producto = valor.strip().upper()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: fecha                                            #
    # ------------------------------------------------------------------ #
    @property
    def fecha(self) -> str:
        """Retorna la fecha y hora de la transacción."""
        return self._fecha

    @fecha.setter
    def fecha(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La fecha de la venta no puede estar vacía.")
        self._fecha = valor.strip()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: total                                            #
    # ------------------------------------------------------------------ #
    @property
    def total(self) -> float:
        """Retorna el monto total de la venta."""
        return self._total

    @total.setter
    def total(self, valor: float) -> None:
        try:
            valor_num = float(valor)
        except (ValueError, TypeError):
            raise ValueError("El total de la venta debe ser un número válido.")
        if valor_num <= 0:
            raise ValueError("El total de la venta debe ser mayor que cero.")
        self._total = valor_num

    # ------------------------------------------------------------------ #
    #  Conversión a diccionario (Serialización JSON)                      #
    # ------------------------------------------------------------------ #
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la instancia Venta a un diccionario estructurado para JSON.
        """
        return {
            "id_venta": self.id_venta,
            "identificacion_usuario": self.identificacion_usuario,
            "codigo_producto": self.codigo_producto,
            "fecha": self.fecha,
            "total": self.total,
        }

    # ------------------------------------------------------------------ #
    #  Reconstrucción desde diccionario (Deserialización JSON)            #
    # ------------------------------------------------------------------ #
    @classmethod
    def from_dict(cls, datos: Dict[str, Any]) -> "Venta":
        """
        Reconstruye un objeto Venta a partir de un diccionario de datos.
        """
        claves_requeridas = (
            "id_venta",
            "identificacion_usuario",
            "codigo_producto",
            "fecha",
            "total",
        )
        for clave in claves_requeridas:
            if clave not in datos:
                raise KeyError(
                    f"El diccionario de venta carece de la clave '{clave}'."
                )

        return cls(
            id_venta=str(datos["id_venta"]),
            identificacion_usuario=str(datos["identificacion_usuario"]),
            codigo_producto=str(datos["codigo_producto"]),
            fecha=str(datos["fecha"]),
            total=datos["total"],
        )

    def __str__(self) -> str:
        return (
            f"Venta(id={self.id_venta!r}, usuario={self.identificacion_usuario!r}, "
            f"producto={self.codigo_producto!r}, fecha={self.fecha!r}, total={self.total:.2f})"
        )
