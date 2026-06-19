# main.py - Punto de entrada del sistema de gestión de restaurante
# Demuestra la creación de objetos y el uso de las clases implementadas

from servicios.restaurante import Restaurante
from modelos.producto import Producto
from modelos.cliente import Cliente


def main():
    """
    Función principal que ejecuta una demostración del sistema de restaurante
    """
    
    # ========== CREACIÓN DEL RESTAURANTE ==========
    print("\n" + "="*80)
    print("INICIALIZANDO SISTEMA DE GESTIÓN DE RESTAURANTE")
    print("="*80)
    
    # Crear una instancia del restaurante
    restaurante = Restaurante(
        nombre="Mi Restaurante Delicioso",
        direccion="Calle Principal 123, Ciudad"
    )
    
    # ========== CREACIÓN DE PRODUCTOS ==========
    print("\n[PRODUCTOS] Agregando productos al menú...\n")
    
    # Crear productos de diferentes categorías
    producto1 = Producto(
        id_producto="P001",
        nombre="Entrada de camarones",
        descripcion="6 camarones frescos a la mantequilla",
        precio=45000,
        categoria="entrada"
    )
    
    producto2 = Producto(
        id_producto="P002",
        nombre="Carne a la parrilla",
        descripcion="Carne de res premium a la parrilla",
        precio=85000,
        categoria="plato principal"
    )
    
    producto3 = Producto(
        id_producto="P003",
        nombre="Salmón a la mantequilla",
        descripcion="Filete de salmón fresco con salsa de mantequilla",
        precio=75000,
        categoria="plato principal"
    )
    
    producto4 = Producto(
        id_producto="P004",
        nombre="Refresco natural",
        descripcion="Jugo de frutas naturales",
        precio=8000,
        categoria="bebida"
    )
    
    producto5 = Producto(
        id_producto="P005",
        nombre="Vino tinto",
        descripcion="Vino tinto reserva",
        precio=65000,
        categoria="bebida"
    )
    
    producto6 = Producto(
        id_producto="P006",
        nombre="Tiramisú",
        descripcion="Postre italiano tradicional",
        precio=25000,
        categoria="postre"
    )
    
    # Agregar los productos al restaurante
    restaurante.agregar_producto(producto1)
    restaurante.agregar_producto(producto2)
    restaurante.agregar_producto(producto3)
    restaurante.agregar_producto(producto4)
    restaurante.agregar_producto(producto5)
    restaurante.agregar_producto(producto6)
    
    # ========== CREACIÓN DE CLIENTES ==========
    print("\n[CLIENTES] Registrando clientes en el sistema...\n")
    
    # Crear clientes
    cliente1 = Cliente(
        id_cliente="C001",
        nombre="Juan Pérez",
        email="juan.perez@email.com",
        telefono="3001234567"
    )
    
    cliente2 = Cliente(
        id_cliente="C002",
        nombre="María García",
        email="maria.garcia@email.com",
        telefono="3007654321"
    )
    
    cliente3 = Cliente(
        id_cliente="C003",
        nombre="Carlos López",
        email="carlos.lopez@email.com",
        telefono="3005555555"
    )
    
    # Registrar los clientes en el restaurante
    restaurante.agregar_cliente(cliente1)
    restaurante.agregar_cliente(cliente2)
    restaurante.agregar_cliente(cliente3)
    
    # ========== DEMOSTRACIÓN DE MÉTODOS ==========
    
    # Mostrar información general del restaurante
    restaurante.mostrar_informacion_general()
    
    # Mostrar el menú completo
    restaurante.mostrar_productos()
    
    # Mostrar clientes registrados
    restaurante.mostrar_clientes()
    
    # ========== REGISTRO DE PEDIDOS ==========
    print("\n" + "="*80)
    print("[PEDIDOS] REALIZANDO PEDIDOS")
    print("="*80)
    
    # Pedido 1: Juan Pérez pide entrada y plato principal
    print("\n[Cliente] Juan Pérez")
    restaurante.registrar_pedido("C001", [("P001", 1), ("P002", 1), ("P004", 2)])
    
    # Pedido 2: María García pide salmón y postre
    print("\n[Cliente] María García")
    restaurante.registrar_pedido("C002", [("P003", 1), ("P006", 1), ("P005", 1)])
    
    # Pedido 3: Carlos López pide plato principal y bebida
    print("\n[Cliente] Carlos López")
    restaurante.registrar_pedido("C003", [("P002", 2), ("P004", 1)])
    
    # Mostrar historial de pedidos
    restaurante.mostrar_pedidos()
    
    # ========== DEMOSTRACIÓN DE MÉTODOS ADICIONALES ==========
    print("\n" + "="*80)
    print("[INFO] INFORMACIÓN ADICIONAL DE CLIENTES")
    print("="*80)
    
    # Mostrar información detallada de cada cliente
    for cliente in restaurante.clientes:
        print(f"\n[Cliente] {cliente.nombre}:")
        print(f"   - Total gastado: ${cliente.obtener_total_gastado():.2f}")
        print(f"   - Cantidad de pedidos: {cliente.cantidad_pedidos}")
    
    # ========== DEMOSTRACIÓN DE DESCUENTOS ==========
    print("\n" + "="*80)
    print("[DESCUENTOS] DEMOSTRACIÓN DE DESCUENTOS")
    print("="*80)
    
    producto_prueba = restaurante.buscar_producto("P002")
    print(f"\nProducto: {producto_prueba.nombre}")
    print(f"Precio original: ${producto_prueba.precio:.2f}")
    print(f"Precio con 10% descuento: ${producto_prueba.aplicar_descuento(10):.2f}")
    print(f"Precio con 20% descuento: ${producto_prueba.aplicar_descuento(20):.2f}")
    
    # ========== INFORMACIÓN FINAL ==========
    print("\n" + "="*80)
    print("[COMPLETADO] DEMOSTRACIÓN COMPLETADA")
    print("="*80)
    print("\nEste sistema demuestra:")
    print("  [OK] Separacion de responsabilidades (modelos y servicios)")
    print("  [OK] Uso correcto de clases con constructores (__init__)")
    print("  [OK] Implementacion del metodo especial __str__()")
    print("  [OK] Importaciones entre modulos")
    print("  [OK] Gestion de listas de objetos")
    print("  [OK] Busqueda y filtrado de datos")
    print("  [OK] Validacion de duplicados")
    print("="*80 + "\n")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
