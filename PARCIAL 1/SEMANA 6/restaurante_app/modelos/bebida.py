# -*- coding: utf-8 -*-
from modelos.producto import Producto

class Bebida(Producto):
    """
    Clase hija que representa una bebida del restaurante.
    Hereda de Producto y añade el atributo volumen_ml.
    """
    def __init__(self, nombre: str, precio: float, volumen_ml: int, disponibilidad: bool = True):
        # Llamada al constructor de la clase padre (Producto)
        super().__init__(nombre, precio, disponibilidad)
        self.volumen_ml = volumen_ml # Volumen en mililitros (ml)

    def mostrar_informacion(self) -> None:
        """
        Sobrescribe el método de la clase padre para mostrar la información
        específica de la bebida, incluyendo el volumen en mililitros.
        """
        super().mostrar_informacion()
        print(f"  Volumen: {self.volumen_ml} ml")
