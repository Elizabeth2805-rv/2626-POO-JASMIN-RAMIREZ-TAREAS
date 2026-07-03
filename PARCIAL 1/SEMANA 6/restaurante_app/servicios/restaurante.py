# -*- coding: utf-8 -*-
from modelos.producto import Producto
from modelos.platillo import Platillo
from modelos.bebida import Bebida

class Restaurante:
    """
    Clase de servicio encargada de administrar una lista de productos
    registrados en el restaurante, presentar el menú categorizado
    y generar informes y estadísticas detalladas.
    """
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.productos = [] # Lista de productos registrados (Platillos y Bebidas)

    def agregar_producto(self, producto: Producto) -> None:
        """
        Agrega un producto a la lista administrada por el restaurante.
        """
        if not isinstance(producto, Producto):
            raise TypeError("Solo se pueden agregar objetos que hereden de la clase Producto.")
        self.productos.append(producto)
        print(f"[Sistema] Se ha registrado el producto: '{producto.nombre}' con éxito.")

    def mostrar_menu(self) -> None:
        """
        Muestra la información de todos los productos de forma categorizada
        (Platillos y Bebidas por separado), demostrando polimorfismo.
        """
        print("\n" + "=" * 55)
        print(f" MENÚ DETALLADO - {self.nombre.upper()} ".center(55, "="))
        print("=" * 55)

        platillos = [p for p in self.productos if isinstance(p, Platillo)]
        bebidas = [p for p in self.productos if isinstance(p, Bebida)]
        otros = [p for p in self.productos if not isinstance(p, (Platillo, Bebida))]

        if not self.productos:
            print("El restaurante no cuenta con productos registrados en este momento.")
            print("=" * 55)
            return

        if platillos:
            print(f"\n--- SECCIÓN DE PLATILLOS ({len(platillos)}) ---")
            for p in platillos:
                p.mostrar_informacion()
                print("-" * 35)

        if bebidas:
            print(f"\n--- SECCIÓN DE BEBIDAS ({len(bebidas)}) ---")
            for p in bebidas:
                p.mostrar_informacion()
                print("-" * 35)

        if otros:
            print(f"\n--- OTROS PRODUCTOS ({len(otros)}) ---")
            for p in otros:
                p.mostrar_informacion()
                print("-" * 35)

        print("\n" + "=" * 55)

    def mostrar_reporte_estadisticas(self) -> None:
        """
        Calcula y muestra un reporte completo de estadísticas del inventario del restaurante.
        """
        print("\n" + "=" * 55)
        print(f" REPORTE GENERAL DE INVENTARIO Y ESTADÍSTICAS ".center(55, "*"))
        print("=" * 55)

        total_productos = len(self.productos)
        if total_productos == 0:
            print("No hay productos registrados para generar estadísticas.")
            print("=" * 55)
            return

        platillos = [p for p in self.productos if isinstance(p, Platillo)]
        bebidas = [p for p in self.productos if isinstance(p, Bebida)]
        
        # Calcular precios
        precios = [p.obtener_precio() for p in self.productos]
        precio_promedio = sum(precios) / total_productos
        
        # Identificar el producto más caro
        producto_mas_caro = max(self.productos, key=lambda p: p.obtener_precio())
        
        # Identificar productos agotados (no disponibles)
        productos_no_disponibles = [p for p in self.productos if not p.disponibilidad]

        print(f"Resumen de Cantidades:")
        print(f"  • Total de Productos Registrados: {total_productos}")
        print(f"  • Total de Platillos: {len(platillos)}")
        print(f"  • Total de Bebidas: {len(bebidas)}")
        
        print(f"\nAnálisis de Precios:")
        print(f"  • Precio Promedio General: ${precio_promedio:.2f}")
        print(f"  • Producto Más Caro: {producto_mas_caro.nombre} (${producto_mas_caro.obtener_precio():.2f})")
        
        print(f"\nDisponibilidad de Stock:")
        print(f"  • Productos en Servicio: {total_productos - len(productos_no_disponibles)}")
        print(f"  • Productos Agotados/Inactivos: {len(productos_no_disponibles)}")
        
        if productos_no_disponibles:
            print("    Lista de Agotados:")
            for p in productos_no_disponibles:
                tipo = "Platillo" if isinstance(p, Platillo) else "Bebida" if isinstance(p, Bebida) else "Producto"
                print(f"      - {p.nombre} ({tipo})")
        
        print("=" * 55)

