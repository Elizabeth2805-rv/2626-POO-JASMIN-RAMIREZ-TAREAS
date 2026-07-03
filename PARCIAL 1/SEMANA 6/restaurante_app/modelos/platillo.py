# -*- coding: utf-8 -*-
from modelos.producto import Producto

class Platillo(Producto):
    """
    Clase hija que representa un platillo o comida del restaurante.
    Hereda de Producto y añade el atributo tiempo_preparacion.
    """
    def __init__(self, nombre: str, precio: float, tiempo_preparacion: int, disponibilidad: bool = True):
        # Llamada al constructor de la clase padre (Producto)
        super().__init__(nombre, precio, disponibilidad)
        self.tiempo_preparacion = tiempo_preparacion # Tiempo en minutos

    def mostrar_informacion(self) -> None:
        """
        Sobrescribe el método de la clase padre para mostrar la información
        específica del platillo, incluyendo el tiempo de preparación.
        """
        super().mostrar_informacion()
        print(f"  Tiempo de Prep.: {self.tiempo_preparacion} min")
