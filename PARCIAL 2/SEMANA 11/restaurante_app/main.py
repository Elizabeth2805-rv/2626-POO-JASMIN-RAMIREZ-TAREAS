# -*- coding: utf-8 -*-
# main.py
# Semana 11 — Colecciones, relaciones, ventas y persistencia JSON en restaurante_app.
#
# Principio SRP:
# main.py es el punto de entrada y arranque del sistema. Su responsabilidad se limita
# a coordinar la interfaz por consola, cargar las tres colecciones (productos, usuarios,
# ventas) desde los archivos JSON al iniciar y solicitar el guardado correspondiente
# cuando las colecciones sufren modificaciones.

import os
import sys
from typing import List, Optional

# Garantizar que los paquetes locales se encuentren en el PATH de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante


# Rutas absolutas a los archivos de datos JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_PRODUCTOS_JSON = os.path.join(BASE_DIR, "datos", "productos.json")
RUTA_USUARIOS_JSON = os.path.join(BASE_DIR, "datos", "usuarios.json")
RUTA_VENTAS_JSON = os.path.join(BASE_DIR, "datos", "ventas.json")


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
#  Funciones Auxiliares de Carga Inicial                                   #
# ====================================================================== #

def cargar_productos_al_iniciar(
    archivo_serv: ArchivoServicio, ruta: str
) -> List[Producto]:
    """Carga los diccionarios de productos.json y reconstruye objetos Producto."""
    lista_dicts = archivo_serv.cargar_productos(ruta)
    productos_reconstruidos: List[Producto] = []
    registros_omitidos = 0

    for indice, datos in enumerate(lista_dicts, start=1):
        try:
            if not isinstance(datos, dict):
                print(f"  [AVISO] Producto #{indice} omitido (no es un objeto válido).")
                registros_omitidos += 1
                continue
            producto_obj = Producto.from_dict(datos)
            productos_reconstruidos.append(producto_obj)
        except KeyError as err_key:
            print(f"  [AVISO] Producto #{indice} omitido por falta de clave: {err_key}")
            registros_omitidos += 1
        except ValueError as err_val:
            print(f"  [AVISO] Producto #{indice} omitido por datos inválidos: {err_val}")
            registros_omitidos += 1

    if registros_omitidos > 0:
        print(f"  [INFO] Se omitieron {registros_omitidos} registro(s) de productos corruptos.")

    return productos_reconstruidos


def cargar_usuarios_al_iniciar(
    archivo_serv: ArchivoServicio, ruta: str
) -> List[Usuario]:
    """Carga los diccionarios de usuarios.json y reconstruye objetos Usuario."""
    lista_dicts = archivo_serv.cargar_usuarios(ruta)
    usuarios_reconstruidos: List[Usuario] = []
    registros_omitidos = 0

    for indice, datos in enumerate(lista_dicts, start=1):
        try:
            if not isinstance(datos, dict):
                print(f"  [AVISO] Usuario #{indice} omitido (no es un objeto válido).")
                registros_omitidos += 1
                continue
            usuario_obj = Usuario.from_dict(datos)
            usuarios_reconstruidos.append(usuario_obj)
        except KeyError as err_key:
            print(f"  [AVISO] Usuario #{indice} omitido por falta de clave: {err_key}")
            registros_omitidos += 1
        except ValueError as err_val:
            print(f"  [AVISO] Usuario #{indice} omitido por datos inválidos: {err_val}")
            registros_omitidos += 1

    if registros_omitidos > 0:
        print(f"  [INFO] Se omitieron {registros_omitidos} registro(s) de usuarios corruptos.")

    return usuarios_reconstruidos


def cargar_ventas_al_iniciar(
    archivo_serv: ArchivoServicio, ruta: str
) -> List[Venta]:
    """Carga los diccionarios de ventas.json y reconstruye objetos Venta."""
    lista_dicts = archivo_serv.cargar_ventas(ruta)
    ventas_reconstruidas: List[Venta] = []
    registros_omitidos = 0

    for indice, datos in enumerate(lista_dicts, start=1):
        try:
            if not isinstance(datos, dict):
                print(f"  [AVISO] Venta #{indice} omitida (no es un objeto válido).")
                registros_omitidos += 1
                continue
            venta_obj = Venta.from_dict(datos)
            ventas_reconstruidas.append(venta_obj)
        except KeyError as err_key:
            print(f"  [AVISO] Venta #{indice} omitida por falta de clave: {err_key}")
            registros_omitidos += 1
        except ValueError as err_val:
            print(f"  [AVISO] Venta #{indice} omitida por datos inválidos: {err_val}")
            registros_omitidos += 1

    if registros_omitidos > 0:
        print(f"  [INFO] Se omitieron {registros_omitidos} registro(s) de ventas corruptos.")

    return ventas_reconstruidas


# ====================================================================== #
#  Funciones Auxiliares de Persistencia                                   #
# ====================================================================== #

def persistir_productos(restaurante_serv: Restaurante, archivo_serv: ArchivoServicio) -> None:
    """Solicita la escritura física de la colección de productos en productos.json."""
    lista_dicts = restaurante_serv.obtener_productos_como_dict()
    if archivo_serv.guardar_productos(RUTA_PRODUCTOS_JSON, lista_dicts):
        print("  [PERSISTENCIA] Archivo 'productos.json' actualizado.")
    else:
        print("  [PERSISTENCIA] No se pudo guardar 'productos.json'.")


def persistir_usuarios(restaurante_serv: Restaurante, archivo_serv: ArchivoServicio) -> None:
    """Solicita la escritura física de la colección de usuarios en usuarios.json."""
    lista_dicts = restaurante_serv.obtener_usuarios_como_dict()
    if archivo_serv.guardar_usuarios(RUTA_USUARIOS_JSON, lista_dicts):
        print("  [PERSISTENCIA] Archivo 'usuarios.json' actualizado.")
    else:
        print("  [PERSISTENCIA] No se pudo guardar 'usuarios.json'.")


def persistir_ventas(restaurante_serv: Restaurante, archivo_serv: ArchivoServicio) -> None:
    """Solicita la escritura física de la colección de ventas en ventas.json."""
    lista_dicts = restaurante_serv.obtener_ventas_como_dict()
    if archivo_serv.guardar_ventas(RUTA_VENTAS_JSON, lista_dicts):
        print("  [PERSISTENCIA] Archivo 'ventas.json' actualizado.")
    else:
        print("  [PERSISTENCIA] No se pudo guardar 'ventas.json'.")


# ====================================================================== #
#  UI: Sección Productos                                                 #
# ====================================================================== #

def registrar_producto_ui(restaurante_serv: Restaurante, archivo_serv: ArchivoServicio) -> None:
    """Solicita los datos de un nuevo producto (incluyendo stock) y persiste el cambio."""
    imprimir_encabezado("REGISTRAR NUEVO PRODUCTO")
    try:
        codigo = input("  Código del producto (e.g. P001): ").strip()
        nombre = input("  Nombre del producto             : ").strip()
        categoria = input("  Categoría (e.g. Plato Fuerte)  : ").strip()
        precio_str = input("  Precio ($)                      : ").strip()
        stock_str = input("  Stock disponible (e.g. 10)      : ").strip()

        try:
            precio = float(precio_str)
        except ValueError:
            raise ValueError("El precio debe ser un número válido (e.g. 8.50).")

        try:
            stock = int(stock_str)
        except ValueError:
            raise ValueError("El stock debe ser un número entero válido (e.g. 10).")

        nuevo_producto = Producto(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock,
        )

        restaurante_serv.registrar_producto(nuevo_producto)
        print(f"\n  [OK] Producto '{nuevo_producto.nombre}' registrado correctamente.")
        persistir_productos(restaurante_serv, archivo_serv)

    except (ValueError, TypeError) as error:
        print(f"\n  [ERROR] No se pudo registrar el producto: {error}")

    pausar()


def buscar_producto_ui(restaurante_serv: Restaurante) -> None:
    """Busca y muestra la información de un producto por código."""
    imprimir_encabezado("BUSCAR PRODUCTO POR CÓDIGO")
    try:
        codigo = input("  Ingrese el código a buscar: ").strip()
        if not codigo:
            raise ValueError("El código ingresado no puede estar vacío.")

        producto = restaurante_serv.buscar_producto_por_codigo(codigo)
        if producto:
            print("\n  [OK] Producto encontrado:")
            producto.mostrar_informacion()
        else:
            print(f"\n  [ERROR] No existe ningún producto con el código '{codigo.upper()}'.")

    except ValueError as error:
        print(f"\n  [ERROR] {error}")

    pausar()


def actualizar_producto_ui(restaurante_serv: Restaurante, archivo_serv: ArchivoServicio) -> None:
    """Permite modificar atributos de un producto (incluido el stock)."""
    imprimir_encabezado("ACTUALIZAR PRODUCTO")
    try:
        codigo = input("  Código del producto a actualizar: ").strip()
        if not codigo:
            raise ValueError("El código no puede estar vacío.")

        producto = restaurante_serv.buscar_producto_por_codigo(codigo)
        if not producto:
            print(f"\n  [ERROR] No existe ningún producto con el código '{codigo.upper()}'.")
            pausar()
            return

        print(f"\n  Producto encontrado: {producto.nombre}")
        print("  (Presione [Enter] sin escribir nada para conservar el valor actual)\n")

        nom_in = input(f"  Nuevo nombre [{producto.nombre}]: ").strip()
        cat_in = input(f"  Nueva categoría [{producto.categoria}]: ").strip()
        pre_in = input(f"  Nuevo precio [${producto.precio:.2f}]: ").strip()
        stk_in = input(f"  Nuevo stock [{producto.stock}]: ").strip()

        nuevo_nombre = nom_in if nom_in else None
        nueva_cat = cat_in if cat_in else None
        nuevo_precio = float(pre_in) if pre_in else None
        nuevo_stock = int(stk_in) if stk_in else None

        exito = restaurante_serv.actualizar_producto(
            codigo=codigo,
            nuevo_nombre=nuevo_nombre,
            nueva_categoria=nueva_cat,
            nuevo_precio=nuevo_precio,
            nuevo_stock=nuevo_stock,
        )

        if exito:
            print(f"\n  [OK] Producto '{codigo.upper()}' actualizado exitosamente.")
            persistir_productos(restaurante_serv, archivo_serv)
        else:
            print("\n  [ERROR] No se pudo actualizar el producto.")

    except (ValueError, TypeError) as error:
        print(f"\n  [ERROR] Error al actualizar producto: {error}")

    pausar()


def eliminar_producto_ui(restaurante_serv: Restaurante, archivo_serv: ArchivoServicio) -> None:
    """Elimina un producto de la colección tras confirmación."""
    imprimir_encabezado("ELIMINAR PRODUCTO")
    try:
        codigo = input("  Código del producto a eliminar: ").strip()
        if not codigo:
            raise ValueError("El código no puede estar vacío.")

        producto = restaurante_serv.buscar_producto_por_codigo(codigo)
        if not producto:
            print(f"\n  [ERROR] No existe ningún producto con el código '{codigo.upper()}'.")
            pausar()
            return

        print(f"\n  Producto a eliminar: {producto.nombre}")
        confirmar = input("  ¿Está seguro de eliminarlo? (s/n): ").strip().lower()

        if confirmar == "s":
            if restaurante_serv.eliminar_producto(codigo):
                print(f"\n  [OK] Producto '{codigo.upper()}' eliminado.")
                persistir_productos(restaurante_serv, archivo_serv)
            else:
                print("\n  [ERROR] No se pudo eliminar el producto.")
        else:
            print("\n  [INFO] Operación cancelada.")

    except ValueError as error:
        print(f"\n  [ERROR] {error}")

    pausar()


def listar_productos_ui(restaurante_serv: Restaurante) -> None:
    """Muestra todos los productos registrados indicando su stock disponible."""
    imprimir_encabezado("LISTADO DE PRODUCTOS")
    productos = restaurante_serv.listar_productos()

    if not productos:
        print("  No hay productos registrados en el sistema.")
    else:
        print(f"  Total de productos en catálogo: {len(productos)}\n")
        for idx, p in enumerate(productos, start=1):
            print(f"  [{idx}]")
            p.mostrar_informacion()

    pausar()


# ====================================================================== #
#  UI: Sección Usuarios                                                  #
# ====================================================================== #

def registrar_usuario_ui(restaurante_serv: Restaurante, archivo_serv: ArchivoServicio) -> None:
    """Solicita los datos de un Usuario, lo registra en el servicio y lo guarda en JSON."""
    imprimir_encabezado("REGISTRAR USUARIO")
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
        print(f"\n  [OK] Usuario '{nuevo_usuario.nombre}' registrado correctamente.")
        persistir_usuarios(restaurante_serv, archivo_serv)

    except (ValueError, TypeError) as error:
        print(f"\n  [ERROR] No se pudo registrar el usuario: {error}")

    pausar()


def listar_usuarios_ui(restaurante_serv: Restaurante) -> None:
    """Muestra todos los usuarios registrados."""
    imprimir_encabezado("LISTADO DE USUARIOS")
    usuarios = restaurante_serv.listar_usuarios()

    if not usuarios:
        print("  No hay usuarios registrados en el sistema.")
    else:
        print(f"  Total de usuarios registrados: {len(usuarios)}\n")
        for idx, u in enumerate(usuarios, start=1):
            print(f"  [{idx}]")
            u.mostrar_informacion()

    pausar()


# ====================================================================== #
#  UI: Sección Ventas (Relación Usuario + Producto -> Venta)             #
# ====================================================================== #

def realizar_venta_ui(restaurante_serv: Restaurante, archivo_serv: ArchivoServicio) -> None:
    """
    Solicita la cédula del usuario, el código del producto y la cantidad.
    Valida la existencia del usuario, producto, cantidad y stock disponible.
    Si la venta es válida:
    - Crea y registra el objeto Venta en la colección.
    - Disminuye el stock del Producto.
    - Persiste 'ventas.json' y 'productos.json'.
    """
    imprimir_encabezado("REALIZAR OPERACIÓN DE VENTA")
    try:
        identificacion = input("  Cédula/ID del usuario comprador: ").strip()
        if not identificacion:
            raise ValueError("La identificación del usuario es obligatoria.")

        usuario = restaurante_serv.buscar_usuario_por_id(identificacion)
        if not usuario:
            print(f"\n  [ERROR] Usuario con ID '{identificacion}' no registrado.")
            pausar()
            return

        print(f"  Usuario verificado: {usuario.nombre} ({usuario.correo})")

        codigo = input("\n  Código del producto a comprar   : ").strip()
        if not codigo:
            raise ValueError("El código del producto es obligatorio.")

        producto = restaurante_serv.buscar_producto_por_codigo(codigo)
        if not producto:
            print(f"\n  [ERROR] Producto con código '{codigo.upper()}' no existe.")
            pausar()
            return

        print(
            f"  Producto seleccionado: {producto.nombre} | "
            f"Precio: ${producto.precio:.2f} | Stock actual: {producto.stock}"
        )

        cant_str = input("\n  Cantidad a comprar               : ").strip()
        try:
            cantidad = int(cant_str)
        except ValueError:
            raise ValueError("La cantidad debe ser un número entero válido.")

        # Ejecutar venta detallada desde Restaurante
        exito, mensaje = restaurante_serv.vender_producto_con_detalle(
            codigo_producto=codigo,
            identificacion_usuario=identificacion,
            cantidad=cantidad,
        )

        if exito:
            print(f"\n  [OK] {mensaje}")
            print(f"  [STOCK ACTUALIZADO] Nuevo stock de '{producto.nombre}': {producto.stock}")

            # Persistir cambios en ventas.json Y productos.json
            persistir_ventas(restaurante_serv, archivo_serv)
            persistir_productos(restaurante_serv, archivo_serv)
        else:
            print(f"\n  [VENTA RECHAZADA] {mensaje}")

    except (ValueError, TypeError) as error:
        print(f"\n  [ERROR] No se pudo procesar la venta: {error}")

    pausar()


def consultar_ventas_usuario_ui(restaurante_serv: Restaurante) -> None:
    """Solicita el ID de un usuario y lista las ventas asociadas filtrando la colección."""
    imprimir_encabezado("CONSULTAR VENTAS POR USUARIO")
    try:
        identificacion = input("  Ingrese la cédula/ID del usuario: ").strip()
        if not identificacion:
            raise ValueError("La identificación no puede estar vacía.")

        usuario = restaurante_serv.buscar_usuario_por_id(identificacion)
        if not usuario:
            print(f"\n  [ERROR] No existe ningún usuario con ID '{identificacion}'.")
            pausar()
            return

        ventas = restaurante_serv.consultar_ventas_por_usuario(identificacion)
        print(f"\n  Usuario: {usuario.nombre} (ID: {usuario.identificacion})")

        if not ventas:
            print("  El usuario no ha registrado compras hasta el momento.")
        else:
            print(f"  Total de ventas registradas para este usuario: {len(ventas)}\n")
            for idx, v in enumerate(ventas, start=1):
                prod = restaurante_serv.buscar_producto_por_codigo(v.producto_codigo)
                nom_prod = prod.nombre if prod else "Desconocido"
                precio_prod = f"${prod.precio:.2f}" if prod else "N/A"

                print(f"  [{idx}] Producto: {nom_prod} (Código: {v.producto_codigo})")
                print(f"      Cantidad  : {v.cantidad} unidad(es)")
                print(f"      Precio Un. : {precio_prod}")
                print("  " + "-" * 44)

    except ValueError as error:
        print(f"\n  [ERROR] {error}")

    pausar()


def listar_todas_las_ventas_ui(restaurante_serv: Restaurante) -> None:
    """Muestra todas las ventas registradas en el sistema."""
    imprimir_encabezado("HISTORIAL GENERAL DE VENTAS")
    ventas = restaurante_serv.listar_ventas()

    if not ventas:
        print("  No hay ventas registradas en el sistema.")
    else:
        print(f"  Total de ventas registradas: {len(ventas)}\n")
        for idx, v in enumerate(ventas, start=1):
            usr = restaurante_serv.buscar_usuario_por_id(v.usuario_id)
            prod = restaurante_serv.buscar_producto_por_codigo(v.producto_codigo)

            nom_usr = usr.nombre if usr else v.usuario_id
            nom_prod = prod.nombre if prod else v.producto_codigo

            print(f"  [{idx}] Usuario  : {nom_usr} (ID: {v.usuario_id})")
            print(f"      Producto : {nom_prod} (Código: {v.producto_codigo})")
            print(f"      Cantidad : {v.cantidad} unidad(es)")
            print("  " + "-" * 44)

    pausar()


# ====================================================================== #
#  Menú Principal y Coordinación                                          #
# ====================================================================== #

def mostrar_menu() -> None:
    """Imprime el menú de opciones interactivo."""
    print("\n" + "=" * 55)
    print("         SISTEMA DE RESTAURANTE — SEMANA 11")
    print("  (Persistencia JSON, Colecciones, Stock & Ventas)")
    print("=" * 55)
    print("  1. Registrar producto (con stock)")
    print("  2. Buscar producto por código")
    print("  3. Actualizar producto")
    print("  4. Eliminar producto")
    print("  5. Listar productos")
    print("  " + "-" * 49)
    print("  6. Registrar usuario")
    print("  7. Listar usuarios")
    print("  " + "-" * 49)
    print("  8. Realizar una venta (Venta: Usuario + Producto)")
    print("  9. Consultar ventas por usuario")
    print(" 10. Listar historial general de ventas")
    print("  " + "-" * 49)
    print(" 11. Salir del sistema")
    print("=" * 55)


def main() -> None:
    """
    Función principal de la aplicación restaurante_app (Semana 11).

    1. Instancia ArchivoServicio.
    2. Carga y reconstruye objetos Producto, Usuario y Venta desde JSON.
    3. Inicializa el servicio Restaurante con las colecciones reconstruidas.
    4. Maneja el bucle principal de interfaz interactiva por consola.
    5. Dispara el guardado JSON correspondiente tras modificaciones.
    """
    limpiar_pantalla()
    print("\n  [INICIO] Cargando aplicación restaurante_app (Semana 11)...")

    # 1. Instanciar servicio de archivo
    archivo_servicio = ArchivoServicio(directorio_datos=os.path.join(BASE_DIR, "datos"))

    # 2. Cargar objetos reconstruidos desde JSON
    print("\n  --> Cargando productos desde JSON...")
    productos_cargados = cargar_productos_al_iniciar(archivo_servicio, RUTA_PRODUCTOS_JSON)

    print("  --> Cargando usuarios desde JSON...")
    usuarios_cargados = cargar_usuarios_al_iniciar(archivo_servicio, RUTA_USUARIOS_JSON)

    print("  --> Cargando ventas desde JSON...")
    ventas_cargadas = cargar_ventas_al_iniciar(archivo_servicio, RUTA_VENTAS_JSON)

    # 3. Inicializar servicio Restaurante con objetos de dominio
    restaurante_servicio = Restaurante(
        productos_iniciales=productos_cargados,
        usuarios_iniciales=usuarios_cargados,
        ventas_iniciales=ventas_cargadas,
    )

    print(
        f"\n  [SISTEMA LISTO] Colecciones cargadas exitosamente:\n"
        f"    - Productos: {len(productos_cargados)}\n"
        f"    - Usuarios : {len(usuarios_cargados)}\n"
        f"    - Ventas   : {len(ventas_cargadas)}"
    )
    pausar()

    opciones_validas = {str(i) for i in range(1, 12)}

    while True:
        limpiar_pantalla()
        mostrar_menu()

        opcion = input("\n  Seleccione una opción (1-11): ").strip()

        if opcion not in opciones_validas:
            print("\n  [ERROR] Opción no válida. Por favor seleccione un número entre 1 y 11.")
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
            registrar_usuario_ui(restaurante_servicio, archivo_servicio)
        elif opcion == "7":
            listar_usuarios_ui(restaurante_servicio)
        elif opcion == "8":
            realizar_venta_ui(restaurante_servicio, archivo_servicio)
        elif opcion == "9":
            consultar_ventas_usuario_ui(restaurante_servicio)
        elif opcion == "10":
            listar_todas_las_ventas_ui(restaurante_servicio)
        elif opcion == "11":
            print(
                "\n  ¡Gracias por utilizar el Sistema de Restaurante! "
                "Persistencia asegurada en archivos JSON. Hasta pronto.\n"
            )
            break


if __name__ == "__main__":
    main()
