# -*- coding: utf-8 -*-
import os
import sys

# Añadir el directorio actual al sys.path para garantizar que las importaciones
# relativas de los paquetes 'modelos' y 'servicios' funcionen desde cualquier entorno.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modelos.platillo import Platillo
from modelos.bebida import Bebida
from servicios.restaurante import Restaurante

def ejecutar_sistema() -> None:
    print("=" * 65)
    print(" SISTEMA DE ADMINISTRACIÓN DE RESTAURANTE - INICIALIZANDO ".center(65, "#"))
    print("=" * 65)

    # 1. Crear el objeto del servicio principal
    mi_restaurante = Restaurante("El Rincón Gourmet")

    # 2. Crear tres objetos del modelo Platillo (comidas)
    platillo1 = Platillo(nombre="Lomo Saltado", precio=15.50, tiempo_preparacion=20, disponibilidad=True)
    platillo2 = Platillo(nombre="Fetuccini a la Huancaina", precio=13.00, tiempo_preparacion=15, disponibilidad=True)
    platillo3 = Platillo(nombre="Ceviche Clásico de Pescado", precio=18.00, tiempo_preparacion=12, disponibilidad=True)
    
    # 3. Crear tres objetos del modelo Bebida (bebidas)
    bebida1 = Bebida(nombre="Chicha Morada (Jarra)", precio=6.00, volumen_ml=1000, disponibilidad=True)
    bebida2 = Bebida(nombre="Inca Kola Personal", precio=2.50, volumen_ml=500, disponibilidad=True)
    bebida3 = Bebida(nombre="Limonada Frozen", precio=3.50, volumen_ml=400, disponibilidad=False) # Agotado para pruebas de stock

    print("\n" + "-" * 20 + " [Prueba de Encapsulación y Validación de Precios] " + "-" * 20)
    
    # Caso A: Intentar modificar el precio de un Platillo con valores inválidos (Negativo / Cero)
    for precio_invalido in [-5.0, 0]:
        try:
            print(f"Intentando cambiar precio de '{platillo1.nombre}' a ${precio_invalido}...")
            platillo1.cambiar_precio(precio_invalido)
        except ValueError as error_val:
            print(f"  [RESULTADO EXPECTADO] Validación exitosa: {error_val}")
        except Exception as e:
            print(f"  Error inesperado: {e}")

    # Caso B: Modificar con precio válido
    print(f"\nPrecio original de '{platillo1.nombre}': ${platillo1.obtener_precio():.2f}")
    nuevo_precio_platillo = 16.50
    print(f"Modificando precio de '{platillo1.nombre}' a ${nuevo_precio_platillo:.2f}...")
    platillo1.cambiar_precio(nuevo_precio_platillo)
    print(f"Precio final de '{platillo1.nombre}': ${platillo1.obtener_precio():.2f}")

    # Caso C: Intentar modificar el precio de una Bebida con valores inválidos (No numéricos / Negativos)
    for valor_invalido in ["Gratis", -1.50]:
        try:
            print(f"\nIntentando cambiar precio de '{bebida1.nombre}' a '{valor_invalido}'...")
            bebida1.cambiar_precio(valor_invalido)
        except (ValueError, TypeError) as error_val:
            print(f"  [RESULTADO EXPECTADO] Validación exitosa: {error_val}")

    # Caso D: Modificar bebida con precio válido
    print(f"\nPrecio original de '{bebida1.nombre}': ${bebida1.obtener_precio():.2f}")
    nuevo_precio_bebida = 7.00
    print(f"Modificando precio de '{bebida1.nombre}' a ${nuevo_precio_bebida:.2f}...")
    bebida1.cambiar_precio(nuevo_precio_bebida)
    print(f"Precio final de '{bebida1.nombre}': ${bebida1.obtener_precio():.2f}")
    
    print("\n" + "-" * 20 + " [Registro de Productos en el Servicio] " + "-" * 20)
    # 4. Agregar los objetos creados a la lista administrada por Restaurante
    mi_restaurante.agregar_producto(platillo1)
    mi_restaurante.agregar_producto(platillo2)
    mi_restaurante.agregar_producto(platillo3)
    mi_restaurante.agregar_producto(bebida1)
    mi_restaurante.agregar_producto(bebida2)
    mi_restaurante.agregar_producto(bebida3)

    # 5. Mostrar la información registrada de forma organizada en consola (Polimorfismo)
    mi_restaurante.mostrar_menu()

    # 6. Mostrar las estadísticas detalladas del restaurante
    mi_restaurante.mostrar_reporte_estadisticas()

if __name__ == "__main__":
    ejecutar_sistema()
