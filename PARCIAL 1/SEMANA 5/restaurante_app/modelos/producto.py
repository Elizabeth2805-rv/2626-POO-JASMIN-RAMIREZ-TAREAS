class Producto:
    def __init__(self, nombre_producto: str, precio_unitario: float, cantidad_stock: int, esta_disponible: bool):
        """Constructor para inicializar las propiedades de un producto del menú."""
        self.nombre_producto: str = nombre_producto
        self.precio_unitario: float = precio_unitario
        self.cantidad_stock: int = cantidad_stock
        self.esta_disponible: bool = esta_disponible

    def __str__(self) -> str:
        """Devuelve una representación amigable del producto en formato de texto."""
        estado: str = "Disponible" if self.esta_disponible else "Agotado"
        return f"Producto: {self.nombre_producto} | Precio: ${self.precio_unitario:.2f} | Stock: {self.cantidad_stock} unidades ({estado})"

