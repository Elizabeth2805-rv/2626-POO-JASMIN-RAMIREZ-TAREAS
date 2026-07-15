# -*- coding: utf-8 -*-
# main.py
# Punto de arranque del sistema restaurante_app — Semana 8.
#
# Principio SRP aplicado a main.py:
#   Su única responsabilidad es coordinar la interacción con el usuario:
#   mostrar el menú, solicitar datos mediante input(), crear los objetos
#   y delegar toda la lógica de administración al servicio Restaurante.
#   main.py NO administra listas ni contiene lógica de negocio.

import os
import sys

# Asegura que el directorio raíz del proyecto esté en el PATH de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modelos.producto import Producto
from modelos.bebida import Bebida
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante


# ====================================================================== #
#  Utilidades de consola                                                   #
# ====================================================================== #

def limpiar_pantalla() -> None:
    """Limpia la consola según el sistema operativo en uso."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar() -> None:
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\n  Presione [Enter] para continuar...")


def imprimir_encabezado(titulo: str) -> None:
    """Imprime un encabezado visual homogéneo para cada sección."""
    print("\n" + "=" * 48)
    print(f"  {titulo}")
    print("=" * 48)


# ====================================================================== #
#  Funciones de interacción — Productos                                    #
# ====================================================================== #

def registrar_producto_ui(servicio: Restaurante) -> None:
    """
    Solicita los datos de un Producto general al usuario,
    crea el objeto y lo registra en el servicio.
    """
    imprimir_encabezado("REGISTRAR PRODUCTO GENERAL")
    try:
        codigo = input("  Código del producto (e.g. P001): ").strip()
        nombre = input("  Nombre del producto             : ").strip()
        categoria = input("  Categoría (e.g. Plato Fuerte)  : ").strip()
        precio_raw = input("  Precio ($)                      : ").strip()

        try:
            precio = float(precio_raw)
        except ValueError:
            raise ValueError("El precio debe ser un número decimal válido (e.g. 8.50).")

        nuevo_producto = Producto(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio=precio,
        )
        servicio.registrar_producto(nuevo_producto)
        print(f"\n  ✔ Producto '{nuevo_producto.nombre}' registrado con éxito.")

    except (ValueError, TypeError) as error:
        print(f"\n  ✘ Error al registrar: {error}")

    pausar()


def registrar_bebida_ui(servicio: Restaurante) -> None:
    """
    Solicita los datos de una Bebida al usuario,
    crea el objeto y lo registra en el servicio.

    Principio OCP: la nueva clase Bebida amplía el sistema sin modificar
    la lógica del servicio Restaurante.
    Principio LSP: la bebida se almacena en la misma colección de productos.
    """
    imprimir_encabezado("REGISTRAR BEBIDA")
    tamanos = ", ".join(Bebida.TAMANOS_VALIDOS)
    envases = ", ".join(Bebida.ENVASES_VALIDOS)

    try:
        codigo = input("  Código de la bebida (e.g. B001) : ").strip()
        nombre = input("  Nombre de la bebida             : ").strip()
        categoria = input("  Categoría (e.g. Bebidas)        : ").strip()
        precio_raw = input("  Precio ($)                      : ").strip()

        try:
            precio = float(precio_raw)
        except ValueError:
            raise ValueError("El precio debe ser un número decimal válido (e.g. 2.75).")

        print(f"  Tamaños disponibles: {tamanos}")
        tamano = input("  Tamaño                          : ").strip()

        print(f"  Envases disponibles: {envases}")
        tipo_envase = input("  Tipo de envase                  : ").strip()

        nueva_bebida = Bebida(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            tamano=tamano,
            tipo_envase=tipo_envase,
        )
        # La bebida se registra en la misma colección que los productos (LSP)
        servicio.registrar_producto(nueva_bebida)
        print(f"\n  ✔ Bebida '{nueva_bebida.nombre}' registrada con éxito.")

    except (ValueError, TypeError) as error:
        print(f"\n  ✘ Error al registrar: {error}")

    pausar()


def listar_productos_ui(servicio: Restaurante) -> None:
    """
    Muestra todos los productos y bebidas registrados en el sistema.

    Principio LSP en acción: se llama a mostrar_informacion() sobre
    cada objeto de la lista. Cada uno responde según su propia
    implementación (Producto o Bebida) sin condicionales de tipo.
    """
    imprimir_encabezado("LISTADO DE PRODUCTOS Y BEBIDAS")
    productos = servicio.listar_productos()

    if not productos:
        print("  No hay productos registrados en el sistema.")
    else:
        print(f"  Total registrados: {len(productos)}\n")
        for indice, producto in enumerate(productos, start=1):
            print(f"  [{indice}]")
            # Polimorfismo: cada objeto ejecuta su propia versión del método
            producto.mostrar_informacion()

    pausar()


# ====================================================================== #
#  Funciones de interacción — Clientes                                     #
# ====================================================================== #

def registrar_cliente_ui(servicio: Restaurante) -> None:
    """
    Solicita los datos de un Cliente al usuario,
    crea el objeto y lo registra en el servicio.
    """
    imprimir_encabezado("REGISTRAR CLIENTE")
    try:
        identificacion = input("  Cédula o RUC del cliente : ").strip()
        nombre = input("  Nombre completo          : ").strip()
        correo = input("  Correo electrónico       : ").strip()

        nuevo_cliente = Cliente(
            identificacion=identificacion,
            nombre=nombre,
            correo=correo,
        )
        servicio.registrar_cliente(nuevo_cliente)
        print(f"\n  ✔ Cliente '{nuevo_cliente.nombre}' registrado con éxito.")

    except (ValueError, TypeError) as error:
        print(f"\n  ✘ Error al registrar: {error}")

    pausar()


def listar_clientes_ui(servicio: Restaurante) -> None:
    """
    Muestra todos los clientes registrados en el sistema.
    """
    imprimir_encabezado("LISTADO DE CLIENTES")
    clientes = servicio.listar_clientes()

    if not clientes:
        print("  No hay clientes registrados en el sistema.")
    else:
        print(f"  Total registrados: {len(clientes)}\n")
        for indice, cliente in enumerate(clientes, start=1):
            print(f"  [{indice}]")
            cliente.mostrar_informacion()

    pausar()


# ====================================================================== #
#  Menú principal                                                          #
# ====================================================================== #

def mostrar_menu() -> None:
    """Imprime el menú interactivo del sistema."""
    print("\n" + "=" * 48)
    print("         SISTEMA DE RESTAURANTE")
    print("=" * 48)
    print("  1. Registrar producto")
    print("  2. Registrar bebida")
    print("  3. Registrar cliente")
    print("  " + "-" * 42)
    print("  4. Listar productos")
    print("  5. Listar clientes")
    print("  " + "-" * 42)
    print("  6. Salir")
    print("=" * 48)


def main() -> None:
    """
    Función principal del sistema restaurante_app.

    Crea la instancia del servicio Restaurante y mantiene el bucle
    de interacción hasta que el usuario elija salir.
    """
    mi_restaurante = Restaurante()

    opciones_validas = {"1", "2", "3", "4", "5", "6"}

    while True:
        limpiar_pantalla()
        mostrar_menu()

        opcion = input("\n  Seleccione una opción (1-6): ").strip()

        if opcion not in opciones_validas:
            print("\n  ✘ Opción no válida. Intente nuevamente.")
            pausar()
            continue

        limpiar_pantalla()

        if opcion == "1":
            registrar_producto_ui(mi_restaurante)
        elif opcion == "2":
            registrar_bebida_ui(mi_restaurante)
        elif opcion == "3":
            registrar_cliente_ui(mi_restaurante)
        elif opcion == "4":
            listar_productos_ui(mi_restaurante)
        elif opcion == "5":
            listar_clientes_ui(mi_restaurante)
        elif opcion == "6":
            print("\n  Gracias por utilizar el Sistema de Restaurante. ¡Hasta pronto!\n")
            break


if __name__ == "__main__":
    main()
