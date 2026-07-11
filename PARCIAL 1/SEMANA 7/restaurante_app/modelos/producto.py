# -*- coding: utf-8 -*-
# modelos/producto.py

class Producto:
    """
    Clase que representa un Producto dentro del menú del restaurante.
    Aplica conceptos de encapsulación utilizando atributos "privados" (por convención con _)
    y controla el acceso y modificación de estos atributos usando decoradores @property y @setter.
    """

    def __init__(self, nombre: str, categoria: str, precio: float, disponible: bool = True):
        """
        Constructor tradicional de la clase Producto.
        Nota: Al usar setters para inicializar los atributos, garantizamos que las validaciones
        se ejecuten tanto en la creación del objeto como en cualquier modificación futura.
        """
        # Se llama a los setters correspondientes para que se aplique la lógica de validación
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.disponible = disponible

    # --- GETTER Y SETTER PARA 'nombre' ---
    @property
    def nombre(self) -> str:
        """Getter para obtener el nombre del producto."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """
        Setter para modificar el nombre del producto.
        Valida que el nombre no sea una cadena vacía o contenga únicamente espacios.
        """
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Error de Validación: El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    # --- GETTER Y SETTER PARA 'categoria' ---
    @property
    def categoria(self) -> str:
        """Getter para obtener la categoría del producto."""
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        """
        Setter para modificar la categoría del producto.
        Valida que la categoría no sea una cadena vacía o contenga únicamente espacios.
        """
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Error de Validación: La categoría del producto no puede estar vacía.")
        self._categoria = valor.strip()

    # --- GETTER Y SETTER PARA 'precio' ---
    @property
    def precio(self) -> float:
        """Getter para obtener el precio del producto."""
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        """
        Setter para modificar el precio del producto.
        Valida que el precio sea un número y estrictamente mayor que cero.
        """
        try:
            valor_num = float(valor)
        except (ValueError, TypeError):
            raise ValueError("Error de Validación: El precio debe ser un valor numérico válido.")
        
        if valor_num <= 0:
            raise ValueError("Error de Validación: El precio del producto debe ser mayor que cero.")
        
        self._precio = valor_num

    # --- GETTER Y SETTER PARA 'disponible' ---
    @property
    def disponible(self) -> bool:
        """Getter para obtener el estado de disponibilidad del producto."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        """Setter para modificar el estado de disponibilidad. Asegura un tipo de dato booleano."""
        if not isinstance(valor, bool):
            # En caso de que se pase un valor que no sea booleano de forma directa
            if str(valor).lower() in ('true', '1', 'si', 'sí', 'yes'):
                self._disponible = True
            elif str(valor).lower() in ('false', '0', 'no'):
                self._disponible = False
            else:
                raise ValueError("Error de Validación: La disponibilidad debe ser un valor booleano (True o False).")
        else:
            self._disponible = valor

    # --- MÉTODO PARA MOSTRAR INFORMACIÓN ---
    def mostrar_informacion(self) -> None:
        """Muestra los datos del producto formateados de una manera legible para el usuario."""
        estado = "Disponible" if self.disponible else "Agotado"
        print(f"Producto: {self.nombre}")
        print(f"  Categoría: {self.categoria}")
        print(f"  Precio:    ${self.precio:.2f}")
        print(f"  Estado:    {estado}")
        print("-" * 30)
