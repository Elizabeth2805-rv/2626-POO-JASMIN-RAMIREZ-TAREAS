# -*- coding: utf-8 -*-
# main.py
# Semana 10 — Manejo de archivos, excepciones y persistencia JSON aplicada a restaurante_app.
#
# Principio SRP:
# main.py es el punto de arranque del sistema. Su única responsabilidad es coordinar
# la interacción con el usuario mediante la consola, cargar los objetos Producto desde
# el archivo JSON al iniciar y solicitar el guardado a través de ArchivoServicio
# cada vez que la colección de productos en Restaurante sufre modificaciones.

import os
import sys
from typing import List, Optional

# Garantizar que los paquetes locales se encuentren en el PATH de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante


# Ruta al archivo de datos JSON
RUTA_PRODUCTOS_JSON = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "datos", "productos.json"
)


# ====================================================================== #
#  Utilidades de Consola                                                   #
# ====================================================================== #

def limpiar_pantalla() -> None:
    """Limpia la pantalla de la consola según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar() -> None:
    """Pausa la ejecución de la consola hasta que el usuario presione Enter."""
    input("\n  Presione [Enter] para continuar...")


def imprimir_encabezado(titulo: str) -> None:
    """Imprime un encabezado formateado y uniforme en la consola."""
    print("\n" + "=" * 55)
    print(f"  {titulo}")
    print("=" * 55)


# ====================================================================== #
#  Funciones Auxiliares de Carga y Guardado                                #
# ====================================================================== #

def cargar_productos_al_iniciar(archivo_serv: ArchivoServicio) -> List[Producto]:
    """
    Carga los diccionarios almacenados en productos.json mediante ArchivoServicio
    y reconstruye cada objeto Producto de manera controlada.

    Manejo de excepciones por registro:
    - KeyError: Si falta alguna clave requerida en un registro JSON almacenado.
    - ValueError: Si un atributo no supera las validaciones de Producto.

    Cualquier registro corrupto es ignorado individualmente con una notificación
    para no impedir la carga de los productos válidos.

    Returns:
        List[Producto]: Lista de objetos Producto válidos reconstruidos.
    """
    lista_dicts = archivo_serv.cargar_productos()
    productos_reconstruidos: List[Producto] = []

    registros_omitidos = 0
    for indice, datos in enumerate(lista_dicts, start=1):
        try:
            if not isinstance(datos, dict):
                print(f"  [AVISO] El registro #{indice} no es un objeto/diccionario. Omitido.")
                registros_omitidos += 1
                continue

            producto_obj = Producto.from_dict(datos)
            productos_reconstruidos.append(producto_obj)

        except KeyError as err_key:
            print(
                f"  [AVISO] Registro #{indice} omitido por falta de clave requerida: {err_key}"
            )
            registros_omitidos += 1
        except ValueError as err_val:
            print(
                f"  [AVISO] Registro #{indice} omitido por datos inválidos: {err_val}"
            )
            registros_omitidos += 1

    if registros_omitidos > 0:
        print(f"  [INFO] Se omitieron {registros_omitidos} registro(s) no válidos durante la carga.")

    return productos_reconstruidos


def persistir_cambios_productos(
    restaurante_serv: Restaurante, archivo_serv: ArchivoServicio
) -> None:
    """
    Obtiene la lista de diccionarios desde Restaurante y solicita
    su escritura física en productos.json a ArchivoServicio.
    """
    lista_dicts = restaurante_serv.obtener_productos_como_dict()
    exito = archivo_serv.guardar_productos(lista_dicts)
    if exito:
        print("  [PERSISTENCIA] Archivo 'productos.json' actualizado correctamente.")
    else:
        print("  [PERSISTENCIA] No se pudo actualizar el archivo 'productos.json'.")


# ====================================================================== #
#  Funciones de Interfaz — Productos                                      #
# ====================================================================== #

def registrar_producto_ui(
    restaurante_serv: Restaurante, archivo_serv: ArchivoServicio
) -> None:
    """
    Solicita por consola los datos de un nuevo producto, valida la información,
    lo registra en el servicio Restaurante y solicita la actualización del JSON.
    """
    imprimir_encabezado("REGISTRAR NUEVO PRODUCTO")
    try:
        codigo = input("  Código del producto (e.g. P001): ").strip()
        nombre = input("  Nombre del producto             : ").strip()
        categoria = input("  Categoría (e.g. Plato Fuerte)  : ").strip()
        precio_str = input("  Precio ($)                      : ").strip()

        try:
            precio = float(precio_str)
        except ValueError:
            raise ValueError("El precio ingresado debe ser un número válido (e.g. 12.50).")

        nuevo_producto = Producto(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio=precio,
        )

        restaurante_serv.registrar_producto(nuevo_producto)
        print(f"\n  [OK] Producto '{nuevo_producto.nombre}' registrado en el servicio.")

        # Persistir cambio en productos.json
        persistir_cambios_productos(restaurante_serv, archivo_serv)

    except (ValueError, TypeError) as error:
        print(f"\n  [ERROR] Error al registrar producto: {error}")

    pausar()


def buscar_producto_ui(restaurante_serv: Restaurante) -> None:
    """Solicita un código de producto y muestra la información si existe."""
    imprimir_encabezado("BUSCAR PRODUCTO POR CÓDIGO")
    try:
        codigo = input("  Ingrese el código a buscar (e.g. P001): ").strip()
        if not codigo:
            raise ValueError("El código ingresado no puede estar vacío.")

        producto = restaurante_serv.buscar_producto_por_codigo(codigo)
        if producto:
            print("\n  [OK] Producto encontrado:")
            producto.mostrar_informacion()
        else:
            print(
                f"\n  [ERROR] No se encontró ningún producto con el código '{codigo.upper()}'."
            )

    except ValueError as error:
        print(f"\n  [ERROR] Error: {error}")

    pausar()


def actualizar_producto_ui(
    restaurante_serv: Restaurante, archivo_serv: ArchivoServicio
) -> None:
    """
    Solicita el código de un producto y los nuevos valores.
    Si se actualiza con éxito en Restaurante, persiste los cambios en JSON.
    """
    imprimir_encabezado("ACTUALIZAR PRODUCTO")
    try:
        codigo = input("  Código del producto a actualizar: ").strip()
        if not codigo:
            raise ValueError("El código no puede estar vacío.")

        producto_existente = restaurante_serv.buscar_producto_por_codigo(codigo)
        if not producto_existente:
            print(
                f"\n  [ERROR] No se encontró ningún producto con el código '{codigo.upper()}'."
            )
            pausar()
            return

        print(f"\n  Producto encontrado: {producto_existente.nombre}")
        print("  (Presione [Enter] sin escribir nada para conservar el valor actual)\n")

        nom_input = input(f"  Nuevo nombre [{producto_existente.nombre}]: ").strip()
        cat_input = input(f"  Nueva categoría [{producto_existente.categoria}]: ").strip()
        pre_input = input(f"  Nuevo precio [${producto_existente.precio:.2f}]: ").strip()

        nuevo_nombre: Optional[str] = nom_input if nom_input else None
        nueva_categoria: Optional[str] = cat_input if cat_input else None
        nuevo_precio: Optional[float] = None

        if pre_input:
            try:
                nuevo_precio = float(pre_input)
            except ValueError:
                raise ValueError("El nuevo precio debe ser un número válido.")

        actualizado = restaurante_serv.actualizar_producto(
            codigo=codigo,
            nuevo_nombre=nuevo_nombre,
            nueva_categoria=nueva_categoria,
            nuevo_precio=nuevo_precio,
        )

        if actualizado:
            print(f"\n  [OK] Producto '{codigo.upper()}' actualizado exitosamente.")
            persistir_cambios_productos(restaurante_serv, archivo_serv)
        else:
            print("\n  [ERROR] No se pudo realizar la actualización.")

    except (ValueError, TypeError) as error:
        print(f"\n  [ERROR] Error al actualizar producto: {error}")

    pausar()


def eliminar_producto_ui(
    restaurante_serv: Restaurante, archivo_serv: ArchivoServicio
) -> None:
    """
    Solicita el código del producto a eliminar, solicita confirmación
    y actualiza el archivo JSON si se elimina del servicio.
    """
    imprimir_encabezado("ELIMINAR PRODUCTO")
    try:
        codigo = input("  Código del producto a eliminar: ").strip()
        if not codigo:
            raise ValueError("El código no puede estar vacío.")

        producto_existente = restaurante_serv.buscar_producto_por_codigo(codigo)
        if not producto_existente:
            print(
                f"\n  [ERROR] No se encontró ningún producto con el código '{codigo.upper()}'."
            )
            pausar()
            return

        print(f"\n  Producto a eliminar: {producto_existente.nombre}")
        confirmar = input("  ¿Está seguro de que desea eliminarlo? (s/n): ").strip().lower()

        if confirmar == "s":
            eliminado = restaurante_serv.eliminar_producto(codigo)
            if eliminado:
                print(f"\n  [OK] Producto '{codigo.upper()}' eliminado exitosamente.")
                persistir_cambios_productos(restaurante_serv, archivo_serv)
            else:
                print("\n  [ERROR] No se pudo eliminar el producto.")
        else:
            print("\n  [INFO] Operación de eliminación cancelada.")

    except ValueError as error:
        print(f"\n  [ERROR] Error: {error}")

    pausar()


def listar_productos_ui(restaurante_serv: Restaurante) -> None:
    """Muestra todos los productos registrados en el sistema."""
    imprimir_encabezado("LISTADO DE PRODUCTOS")
    productos = restaurante_serv.listar_productos()

    if not productos:
        print("  No hay productos registrados en el sistema.")
    else:
        print(f"  Total de productos registrados: {len(productos)}\n")
        for idx, producto in enumerate(productos, start=1):
            print(f"  [{idx}]")
            producto.mostrar_informacion()

    pausar()


# ====================================================================== #
#  Funciones de Interfaz — Usuarios (En Memoria)                          #
# ====================================================================== #

def registrar_usuario_ui(restaurante_serv: Restaurante) -> None:
    """Solicita los datos de un Usuario y lo registra en memoria."""
    imprimir_encabezado("REGISTRAR USUARIO (EN MEMORIA)")
    try:
        identificacion = input("  Cédula o ID del usuario  : ").strip()
        nombre = input("  Nombre completo          : ").strip()
        correo = input("  Correo electrónico       : ").strip()

        nuevo_usuario = Usuario(
            identificacion=identificacion,
            nombre=nombre,
            correo=correo,
        )

        restaurante_serv.registrar_usuario(nuevo_usuario)
        print(f"\n  [OK] Usuario '{nuevo_usuario.nombre}' registrado en memoria.")

    except (ValueError, TypeError) as error:
        print(f"\n  [ERROR] Error al registrar usuario: {error}")

    pausar()


def listar_usuarios_ui(restaurante_serv: Restaurante) -> None:
    """Muestra los usuarios almacenados en memoria."""
    imprimir_encabezado("LISTADO DE USUARIOS (EN MEMORIA)")
    usuarios = restaurante_serv.listar_usuarios()

    if not usuarios:
        print("  No hay usuarios registrados en memoria.")
    else:
        print(f"  Total de usuarios registrados: {len(usuarios)}\n")
        for idx, usuario in enumerate(usuarios, start=1):
            print(f"  [{idx}]")
            usuario.mostrar_informacion()

    pausar()


# ====================================================================== #
#  Menú Principal                                                          #
# ====================================================================== #

def mostrar_menu() -> None:
    """Imprime las opciones del menú principal en la consola."""
    print("\n" + "=" * 55)
    print("         SISTEMA DE RESTAURANTE — SEMANA 10")
    print("      (Persistencia JSON & Control de Excepciones)")
    print("=" * 55)
    print("  1. Registrar producto")
    print("  2. Buscar producto por código")
    print("  3. Actualizar producto")
    print("  4. Eliminar producto")
    print("  5. Listar productos")
    print("  " + "-" * 49)
    print("  6. Registrar usuario (En memoria)")
    print("  7. Listar usuarios (En memoria)")
    print("  " + "-" * 49)
    print("  8. Salir del sistema")
    print("=" * 55)


def main() -> None:
    """
    Función principal de la aplicación restaurante_app (Semana 10).

    1. Instancia ArchivoServicio con la ruta datos/productos.json.
    2. Carga los productos desde JSON convirtiéndolos a objetos Producto.
    3. Entrega la colección de objetos Producto a Restaurante.
    4. Mantiene el bucle interactivo de consola.
    5. Solicita el guardado JSON tras registrar, actualizar o eliminar productos.
    """
    limpiar_pantalla()
    print("\n  [INICIO] Cargando aplicación restaurante_app...")

    # 1. Crear servicio de archivo
    archivo_servicio = ArchivoServicio(ruta_archivo=RUTA_PRODUCTOS_JSON)

    # 2. Cargar y reconstruir objetos Producto desde JSON
    productos_cargados = cargar_productos_al_iniciar(archivo_servicio)

    # 3. Inicializar servicio de Restaurante con los objetos Producto
    restaurante_servicio = Restaurante(productos_iniciales=productos_cargados)

    print(
        f"  [SISTEMA LISTO] Se cargaron {len(productos_cargados)} producto(s) "
        f"desde 'datos/productos.json'."
    )
    pausar()

    opciones_validas = {"1", "2", "3", "4", "5", "6", "7", "8"}

    while True:
        limpiar_pantalla()
        mostrar_menu()

        opcion = input("\n  Seleccione una opción (1-8): ").strip()

        if opcion not in opciones_validas:
            print("\n  [ERROR] Opción no válida. Por favor seleccione un número del 1 al 8.")
            pausar()
            continue

        limpiar_pantalla()

        if opcion == "1":
            registrar_producto_ui(restaurante_servicio, archivo_servicio)
        elif opcion == "2":
            buscar_producto_ui(restaurante_servicio)
        elif opcion == "3":
            actualizar_producto_ui(restaurante_servicio, archivo_servicio)
        elif opcion == "4":
            eliminar_producto_ui(restaurante_servicio, archivo_servicio)
        elif opcion == "5":
            listar_productos_ui(restaurante_servicio)
        elif opcion == "6":
            registrar_usuario_ui(restaurante_servicio)
        elif opcion == "7":
            listar_usuarios_ui(restaurante_servicio)
        elif opcion == "8":
            print(
                "\n  ¡Gracias por utilizar el Sistema de Restaurante! "
                "Persistencia asegurada en 'datos/productos.json'. Hasta pronto.\n"
            )
            break


if __name__ == "__main__":
    main()
