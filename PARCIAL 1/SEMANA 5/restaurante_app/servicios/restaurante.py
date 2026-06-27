from modelos.producto import Producto
from modelos.cliente import Cliente


class Restaurante:
    def __init__(self, nombre_establecimiento: str):
        """Inicializa el restaurante con su nombre y sus listas de datos compuestas."""
        self.nombre_establecimiento: str = nombre_establecimiento
        # Listas como tipo de dato compuesto para almacenar los objetos creados
        self.lista_productos: list[Producto] = []
        self.lista_clientes: list[Cliente] = []

    def registrar_producto(self, nuevo_producto: Producto) -> None:
        """Agrega un objeto Producto a la lista del establecimiento."""
        self.lista_productos.append(nuevo_producto)

    def registrar_cliente(self, nuevo_cliente: Cliente) -> None:
        """Agrega un objeto Cliente a la lista del establecimiento."""
        self.lista_clientes.append(nuevo_cliente)

    def mostrar_reporte_general(self) -> None:
        """Imprime de forma ordenada toda la información almacenada en el sistema."""
        print(f"\n=========================================")
        print(f" REPORTE DEL RESTAURANTE: {self.nombre_establecimiento.upper()} ")
        print(f"=========================================")

        print("\n--- MENÚ DE PRODUCTOS REGISTRADOS ---")
        if not self.lista_productos:
            print("No hay productos en el sistema.")
        else:
            for producto in self.lista_productos:
                print(producto)  # Llama automáticamente al método __str__() del producto

        print("\n--- CLIENTES REGISTRADOS ---")
        if not self.lista_clientes:
            print("No hay clientes en el sistema.")
        else:
            for cliente in self.lista_clientes:
                print(cliente)  # Llama automáticamente al método __str__() del cliente
        print("=========================================\n")
