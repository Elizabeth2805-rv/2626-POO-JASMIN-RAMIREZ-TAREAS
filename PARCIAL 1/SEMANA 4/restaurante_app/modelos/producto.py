# Clase Producto - Representa un artículo disponible en el restaurante

class Producto:
    """
    Representa un producto disponible en el restaurante.
    Almacena información sobre platos, bebidas y otros artículos del menú.
    """
    
    def __init__(self, id_producto, nombre, descripcion, precio, categoria):
        """
        Constructor de la clase Producto
        
        Args:
            id_producto: Identificador único del producto
            nombre: Nombre del producto
            descripcion: Descripción detallada del producto
            precio: Precio en pesos
            categoria: Categoría a la que pertenece (entrada, plato principal, bebida, postre)
        """
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria
    
    def __str__(self):
        """
        Representación en texto del producto
        Facilita la visualización de la información de forma legible
        """
        return (f"[{self.id_producto}] {self.nombre} ({self.categoria}) - "
                f"${self.precio:.2f} - {self.descripcion}")
    
    def obtener_descripcion_completa(self):
        """
        Retorna una descripción detallada del producto
        """
        return f"{self.nombre}: {self.descripcion}"
    
    def aplicar_descuento(self, porcentaje):
        """
        Calcula el precio con descuento aplicado
        
        Args:
            porcentaje: Porcentaje de descuento (0-100)
            
        Returns:
            float: Precio con descuento aplicado
        """
        descuento = self.precio * (porcentaje / 100)
        precio_con_descuento = self.precio - descuento
        return precio_con_descuento
