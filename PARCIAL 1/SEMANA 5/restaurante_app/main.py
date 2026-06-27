from servicios.restaurante import Restaurante
from modelos.producto import Producto
from modelos.cliente import Cliente

def ejecutar_sistema() -> None:
    # 1. Crear el objeto del servicio principal
    mi_restaurante = Restaurante("El Buen Sabor")

    # 2. Crear al menos dos objetos del modelo Producto (Tipos: str, float, int, bool)
    platillo_principal = Producto("Asado de Tira Familiar", 18.50, 15, True)
    bebida_refrescante = Producto("Jugo Natural de Limón", 2.25, 40, True)
    producto_agotado = Producto("Postre Tres Leches", 3.50, 0, False)

    # 3. Crear al menos dos objetos del modelo Cliente (Tipos: str, str, int, bool)
    cliente_uno = Cliente("1726543210", "Jasmin Ramirez", 21, True)
    cliente_dos = Cliente("1709876543", "Carlos Andrade", 34, False)

    # 4. Agregar los objetos creados a las listas administradas por el servicio principal
    mi_restaurante.registrar_producto(platillo_principal)
    mi_restaurante.registrar_producto(bebida_refrescante)
    mi_restaurante.registrar_producto(producto_agotado)

    mi_restaurante.registrar_cliente(cliente_uno)
    mi_restaurante.registrar_cliente(cliente_dos)

    # 5. Mostrar la información registrada de forma organizada en la consola
    mi_restaurante.mostrar_reporte_general()

if __name__ == "__main__":
    ejecutar_sistema()

















