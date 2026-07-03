# -*- coding: utf-8 -*-

class Producto:
    """
    Clase padre que representa un producto general en el restaurante.
    """
    def __init__(self, nombre: str, precio: float, disponibilidad: bool = True):
        self.nombre = nombre
        self.disponibilidad = disponibilidad
        # Encapsulación del atributo precio
        self.__precio = 0.0
        self.cambiar_precio(precio)

    def obtener_precio(self) -> float:
        """
        Método de acceso (Getter) para obtener el precio del producto.
        """
        return self.__precio

    def cambiar_precio(self, nuevo_precio: float) -> None:
        """
        Método de modificación (Setter) para cambiar el precio con validación.
        El precio debe ser un número strictly mayor que cero.
        """
        if not isinstance(nuevo_precio, (int, float)):
            raise TypeError("El precio debe ser un número (entero o decimal).")
        
        if nuevo_precio <= 0:
            raise ValueError(f"Error: El precio ({nuevo_precio}) debe ser mayor que cero. No se puede asignar un precio negativo o igual a cero.")
        
        self.__precio = float(nuevo_precio)

    def mostrar_informacion(self) -> None:
        """
        Muestra la información general del producto en consola.
        """
        estado = "Disponible" if self.disponibilidad else "No disponible"
        print(f"Producto: {self.nombre}")
        print(f"  Precio: ${self.obtener_precio():.2f}")
        print(f"  Estado: {estado}")
