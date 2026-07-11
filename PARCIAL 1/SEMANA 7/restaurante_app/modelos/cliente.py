# -*- coding: utf-8 -*-
# modelos/cliente.py

from dataclasses import dataclass

@dataclass
class Cliente:
    """
    Clase que representa un Cliente del restaurante.
    Esta clase se define utilizando el decorador @dataclass de Python.
    
    ¿Qué hace @dataclass?
    Genera automáticamente el constructor especial __init__(), el método __repr__()
    (para visualización legible en consola), el método __eq__() (para comparar objetos),
    entre otros métodos especiales, sin necesidad de escribirlos manualmente.
    """
    nombre: str
    correo: str
    id_cliente: str  # Cédula, RUC o identificador único del cliente

    def mostrar_informacion(self) -> None:
        """
        Muestra la información del cliente formateada en consola.
        """
        print(f"Cliente ID: {self.id_cliente}")
        print(f"  Nombre:    {self.nombre}")
        print(f"  Correo:    {self.correo}")
        print("-" * 30)
