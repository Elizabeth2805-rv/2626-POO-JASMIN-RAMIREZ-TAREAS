# -*- coding: utf-8 -*-
# main.py
# Semana 9 — Persistencia de datos en archivos JSON.
# Clonado y extendido desde PARCIAL 1 / SEMANA 8.
#
# Principio SRP aplicado a main.py:
#   Su única responsabilidad es coordinar la interacción por consola:
#   mostrar el menú, solicitar datos mediante input(), construir los
#   objetos y delegar toda lógica al servicio Restaurante.
#   main.py NO manipula archivos JSON ni las listas internas del servicio.
#
# Los datos de productos y clientes se persisten automáticamente en:
#   restaurante_app/datos/productos.json
#   restaurante_app/datos/clientes.json

import os
import sys

# Agrega el directorio raíz del proyecto al PATH para importaciones relativas
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modelos.producto import Producto
from modelos.bebida import Bebida
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante


# ====================================================================== #
#  Ruta al directorio de datos JSON                                        #
# ====================================================================== #

# La carpeta 'datos/' se ubica dentro de restaurante_app/
DIRECTORIO_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")


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
    """Imprime un encabezado visual uniforme para cada sección."""
    print("\n" + "=" * 50)
    print(f"  {titulo}")
    print("=" * 50)


# ====================================================================== #
#  Funciones de interacción — Productos                                    #
# ====================================================================== #

def registrar_producto_ui(servicio: Restaurante) -> None:
    """
    Solicita los datos de un Producto general al usuario,
    construye el objeto y lo registra en el servicio.
    El servicio persiste el cambio automáticamente en productos.json.
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
            raise ValueError(
                "El precio debe ser un número decimal válido (e.g. 8.50)."
            )

        nuevo_producto = Producto(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio=precio,
        )
        servicio.registrar_producto(nuevo_producto)
        print(f"\n  ✔ Producto '{nuevo_producto.nombre}' registrado y guardado en JSON.")

    except (ValueError, TypeError) as error:
        print(f"\n  ✘ Error al registrar: {error}")

    pausar()


def registrar_bebida_ui(servicio: Restaurante) -> None:
    """
    Solicita los datos de una Bebida al usuario, construye el objeto
    y lo registra en el servicio.
    El servicio persiste el cambio automáticamente en productos.json.

    Principio LSP: la bebida se almacena en la misma colección que los
    productos generales.
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
            raise ValueError(
                "El precio debe ser un número decimal válido (e.g. 2.75)."
            )

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
        servicio.registrar_producto(nueva_bebida)
        print(f"\n  ✔ Bebida '{nueva_bebida.nombre}' registrada y guardada en JSON.")

    except (ValueError, TypeError) as error:
        print(f"\n  ✘ Error al registrar: {error}")

    pausar()


def buscar_producto_ui(servicio: Restaurante) -> None:
    """
    Solicita un código al usuario y muestra el producto encontrado,
    o informa si no existe ninguno con ese código.
    """
    imprimir_encabezado("BUSCAR PRODUCTO")
    try:
        codigo = input("  Código del producto a buscar: ").strip()
        if not codigo:
            raise ValueError("El código no puede estar vacío.")

        producto = servicio.buscar_producto_por_codigo(codigo)
        if producto:
            print("\n  Producto encontrado:")
            producto.mostrar_informacion()
        else:
            print(
                f"\n  ✘ No se encontró ningún producto con el código "
                f"'{codigo.upper()}'."
            )
    except ValueError as error:
        print(f"\n  ✘ Error: {error}")

    pausar()


def actualizar_producto_ui(servicio: Restaurante) -> None:
    """
    Solicita el código de un producto y los nuevos valores de sus
    atributos. Los campos dejados en blanco no se modifican.
    El servicio persiste el cambio automáticamente en productos.json.
    """
    imprimir_encabezado("ACTUALIZAR PRODUCTO")
    try:
        codigo = input("  Código del producto a actualizar: ").strip()
        if not codigo:
            raise ValueError("El código no puede estar vacío.")

        producto_existente = servicio.buscar_producto_por_codigo(codigo)
        if not producto_existente:
            print(
                f"\n  ✘ No se encontró ningún producto con el código "
                f"'{codigo.upper()}'."
            )
            pausar()
            return

        print(f"\n  Producto encontrado: {producto_existente.nombre}")
        print("  (Deje en blanco los campos que no desea modificar)\n")

        entrada_nombre = input(
            f"  Nuevo nombre [{producto_existente.nombre}]: "
        ).strip()
        entrada_categoria = input(
            f"  Nueva categoría [{producto_existente.categoria}]: "
        ).strip()
        entrada_precio = input(
            f"  Nuevo precio [${producto_existente.precio:.2f}]: "
        ).strip()

        nuevo_nombre: str | None = entrada_nombre if entrada_nombre else None
        nueva_categoria: str | None = (
            entrada_categoria if entrada_categoria else None
        )
        nuevo_precio: float | None = None
        if entrada_precio:
            try:
                nuevo_precio = float(entrada_precio)
            except ValueError:
                raise ValueError(
                    "El precio debe ser un número decimal válido (e.g. 9.00)."
                )

        actualizado = servicio.actualizar_producto(
            codigo=codigo,
            nuevo_nombre=nuevo_nombre,
            nueva_categoria=nueva_categoria,
            nuevo_precio=nuevo_precio,
        )

        if actualizado:
            print(
                f"\n  ✔ Producto '{codigo.upper()}' actualizado y guardado en JSON."
            )
        else:
            print(f"\n  ✘ No se pudo actualizar el producto.")

    except (ValueError, TypeError) as error:
        print(f"\n  ✘ Error al actualizar: {error}")

    pausar()


def eliminar_producto_ui(servicio: Restaurante) -> None:
    """
    Solicita el código de un producto, confirma la operación y lo elimina.
    El servicio persiste el cambio automáticamente en productos.json.
    """
    imprimir_encabezado("ELIMINAR PRODUCTO")
    try:
        codigo = input("  Código del producto a eliminar: ").strip()
        if not codigo:
            raise ValueError("El código no puede estar vacío.")

        producto_existente = servicio.buscar_producto_por_codigo(codigo)
        if not producto_existente:
            print(
                f"\n  ✘ No se encontró ningún producto con el código "
                f"'{codigo.upper()}'."
            )
            pausar()
            return

        print(f"\n  Producto encontrado: {producto_existente.nombre}")
        confirmacion = input(
            "  ¿Está seguro de que desea eliminarlo? (s/n): "
        ).strip().lower()

        if confirmacion == "s":
            eliminado = servicio.eliminar_producto(codigo)
            if eliminado:
                print(
                    f"\n  ✔ Producto '{codigo.upper()}' eliminado y JSON actualizado."
                )
            else:
                print("\n  ✘ No se pudo eliminar el producto.")
        else:
            print("\n  Operación cancelada.")

    except ValueError as error:
        print(f"\n  ✘ Error: {error}")

    pausar()


def listar_productos_ui(servicio: Restaurante) -> None:
    """
    Muestra todos los productos y bebidas registrados en el sistema.
    LSP en acción: se llama a mostrar_informacion() sobre cada objeto;
    cada uno responde según su propia implementación.
    """
    imprimir_encabezado("LISTADO DE PRODUCTOS Y BEBIDAS")
    productos = servicio.listar_productos()

    if not productos:
        print("  No hay productos registrados en el sistema.")
    else:
        print(f"  Total registrados: {len(productos)}\n")
        for indice, producto in enumerate(productos, start=1):
            print(f"  [{indice}]")
            producto.mostrar_informacion()

    pausar()


# ====================================================================== #
#  Funciones de interacción — Clientes                                     #
# ====================================================================== #

def registrar_cliente_ui(servicio: Restaurante) -> None:
    """
    Solicita los datos de un Cliente al usuario, construye el objeto
    y lo registra en el servicio.
    El servicio persiste el cambio automáticamente en clientes.json.
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
        print(
            f"\n  ✔ Cliente '{nuevo_cliente.nombre}' registrado y guardado en JSON."
        )

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
    print("\n" + "=" * 50)
    print("         SISTEMA DE RESTAURANTE")
    print("         (Con persistencia JSON)")
    print("=" * 50)
    print("  1. Registrar producto")
    print("  2. Registrar bebida")
    print("  3. Buscar producto")
    print("  4. Actualizar producto")
    print("  5. Eliminar producto")
    print("  " + "-" * 44)
    print("  6. Listar productos")
    print("  " + "-" * 44)
    print("  7. Registrar cliente")
    print("  8. Listar clientes")
    print("  " + "-" * 44)
    print("  9. Salir")
    print("=" * 50)


def main() -> None:
    """
    Función principal del sistema restaurante_app — Semana 9.

    Crea la instancia del servicio Restaurante indicando la ruta al
    directorio de datos JSON. El servicio carga automáticamente los
    datos persistidos de sesiones anteriores.

    El bucle principal se mantiene activo hasta que el usuario elige salir.
    """
    print("\n  Iniciando sistema... cargando datos desde archivos JSON.")
    mi_restaurante = Restaurante(directorio_datos=DIRECTORIO_DATOS)

    total_productos = len(mi_restaurante.listar_productos())
    total_clientes = len(mi_restaurante.listar_clientes())
    print(
        f"  Datos cargados: {total_productos} producto(s), "
        f"{total_clientes} cliente(s)."
    )

    opciones_validas = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}

    while True:
        limpiar_pantalla()
        mostrar_menu()

        opcion = input("\n  Seleccione una opción (1-9): ").strip()

        if opcion not in opciones_validas:
            print("\n  ✘ Opción no válida. Ingrese un número del 1 al 9.")
            pausar()
            continue

        limpiar_pantalla()

        if opcion == "1":
            registrar_producto_ui(mi_restaurante)
        elif opcion == "2":
            registrar_bebida_ui(mi_restaurante)
        elif opcion == "3":
            buscar_producto_ui(mi_restaurante)
        elif opcion == "4":
            actualizar_producto_ui(mi_restaurante)
        elif opcion == "5":
            eliminar_producto_ui(mi_restaurante)
        elif opcion == "6":
            listar_productos_ui(mi_restaurante)
        elif opcion == "7":
            registrar_cliente_ui(mi_restaurante)
        elif opcion == "8":
            listar_clientes_ui(mi_restaurante)
        elif opcion == "9":
            print(
                "\n  Datos guardados. "
                "Gracias por utilizar el Sistema de Restaurante. ¡Hasta pronto!\n"
            )
            break


if __name__ == "__main__":
    main()
