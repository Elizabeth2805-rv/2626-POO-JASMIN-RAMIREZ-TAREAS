# -*- coding: utf-8 -*-
# main.py

import os
import sys

# Asegurar que el directorio actual esté en el PATH de Python para evitar problemas de importación
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modelos.producto import Producto
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante


def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_explicacion_didactica(titulo: str, explicacion: str):
    """Muestra un panel didáctico en consola para explicar conceptos de POO."""
    print("\n" + "=" * 60)
    print(f"💡 [EXPLICACIÓN POO] - {titulo}")
    print("-" * 60)
    print(explicacion)
    print("=" * 60 + "\n")
    input("Presione [Enter] para continuar...")



def precargar_datos_ejemplo(servicio: Restaurante):
    """
    Precarga datos iniciales en el sistema para que sea inmediatamente interactivo,
    demostrando cómo los objetos se instancian y se registran en el servicio.
    """
    # Productos de ejemplo
    p1 = Producto(nombre="Hamburguesa con Queso", categoria="Plato Fuerte", precio=8.50, disponible=True)
    p2 = Producto(nombre="Limonada Imperial", categoria="Bebidas", precio=2.75, disponible=True)
    p3 = Producto(nombre="Pastel de Chocolate", categoria="Postres", precio=4.00, disponible=False)
    
    servicio.registrar_producto(p1)
    servicio.registrar_producto(p2)
    servicio.registrar_producto(p3)

    # Clientes de ejemplo usando la Dataclass
    c1 = Cliente(nombre="Jasmin Ramirez", correo="jasmin.ramirez@correo.com", id_cliente="0987654321")
    c2 = Cliente(nombre="Carlos Mendoza", correo="carlos.mendoza@correo.com", id_cliente="1234567890")
    
    servicio.registrar_cliente(c1)
    servicio.registrar_cliente(c2)


def registrar_producto_ui(servicio: Restaurante):
    print("\n--- REGISTRAR NUEVO PRODUCTO ---")
    try:
        nombre = input("Ingrese el nombre del producto: ")
        categoria = input("Ingrese la categoría del producto: ")
        
        precio_raw = input("Ingrese el precio del producto: $")
        try:
            precio = float(precio_raw)
        except ValueError:
            raise ValueError("Error de Entrada: El precio debe ser un número decimal válido.")

        disponible_raw = input("¿Está disponible actualmente? (S/N) [Por defecto: S]: ").strip().lower()
        disponible = disponible_raw in ('', 's', 'si', 'sí', 'y', 'yes')

        # Creación del objeto Producto
        nuevo_producto = Producto(nombre=nombre, categoria=categoria, precio=precio, disponible=disponible)
        
        # Registro en el servicio
        servicio.registrar_producto(nuevo_producto)
        
        print("\n✔ Producto registrado con éxito.")
        
        # Sección didáctica explicativa
        explicacion = (
            "1. Entrada de datos (input) -> Se capturaron las variables desde consola.\n"
            "2. Llamada al constructor -> Se ejecutó Producto(nombre, categoria, precio, disponible).\n"
            "3. Encapsulación y Setters -> Internamente, el constructor ejecutó los setters (@setter).\n"
            "   Por ejemplo, se validó que el precio fuera mayor a 0 y que el nombre no estuviera vacío.\n"
            "4. Almacenamiento en el Servicio -> El objeto se añadió a la lista interna en Restaurante."
        )
        mostrar_explicacion_didactica("Instanciación y Validación con Constructor Tradicional", explicacion)

    except ValueError as e:
        print(f"\n❌ Error al registrar producto: {e}")
        print("El objeto no pudo ser creado debido a fallas en la validación.")
        input("\nPresione [Enter] para regresar al menú...")


def listar_productos_ui(servicio: Restaurante):
    print("\n=== LISTADO DE PRODUCTOS EN EL SISTEMA ===")
    productos = servicio.listar_productos()
    
    if not productos:
        print("No hay productos registrados en el sistema.")
    else:
        for index, prod in enumerate(productos, 1):
            print(f"[{index}] ", end="")
            prod.mostrar_informacion()
    
    explicacion = (
        "1. Desacoplamiento (Capas) -> La vista solicita la lista al servicio 'Restaurante'.\n"
        "2. Propiedades (@property) -> El método 'mostrar_informacion()' accede a los atributos privados\n"
        "   '_nombre', '_precio', etc., de forma controlada a través de sus getters públicos.\n"
        "3. Estructura de Datos -> Se itera una lista de objetos instanciados en memoria dinámica."
    )
    mostrar_explicacion_didactica("Lectura de Datos y Uso de Getters (@property)", explicacion)


def buscar_producto_ui(servicio: Restaurante):
    print("\n--- BUSCAR PRODUCTO ---")
    query = input("Ingrese el nombre del producto que desea buscar: ")
    coincidencias = servicio.buscar_producto(query)

    if not coincidencias:
        print(f"\nNo se encontraron productos que coincidan con '{query}'.")
    else:
        print(f"\nSe encontraron {len(coincidencias)} coincidencias:")
        print("-" * 35)
        for prod in coincidencias:
            prod.mostrar_informacion()

    explicacion = (
        "1. Búsqueda en Capa de Servicio -> main.py delega la búsqueda a 'Restaurante.buscar_producto()'.\n"
        "2. Encapsulación -> La lógica de filtrado se mantiene aislada en el servicio, no en la interfaz.\n"
        "3. Acceso a Atributos -> El filtrado evalúa la propiedad 'nombre.lower()' usando el getter."
    )
    mostrar_explicacion_didactica("Métodos de Búsqueda y Encapsulación", explicacion)


def registrar_cliente_ui(servicio: Restaurante):
    print("\n--- REGISTRAR NUEVO CLIENTE ---")
    nombre = input("Ingrese el nombre del cliente: ").strip()
    correo = input("Ingrese el correo electrónico: ").strip()
    id_cliente = input("Ingrese el identificador (Cédula/RUC): ").strip()

    if not nombre or not correo or not id_cliente:
        print("\n❌ Error: Ninguno de los campos del cliente puede estar vacío.")
        input("\nPresione [Enter] para regresar...")
        return

    try:
        # Creación del objeto Cliente usando el constructor autogenerado por @dataclass
        nuevo_cliente = Cliente(nombre=nombre, correo=correo, id_cliente=id_cliente)
        
        # Registro en el servicio
        servicio.registrar_cliente(nuevo_cliente)
        print("\n✔ Cliente registrado con éxito.")

        explicacion = (
            "1. Decorador @dataclass -> La clase Cliente no tiene definido un constructor __init__ manual.\n"
            "   Python generó automáticamente el constructor en base a los atributos anotados.\n"
            "2. Representación y Estructura -> Al usar dataclass se optimiza la creación de clases\n"
            "   cuya única responsabilidad es contener y estructurar datos del negocio."
        )
        mostrar_explicacion_didactica("Uso del Decorador @dataclass", explicacion)

    except ValueError as e:
        print(f"\n❌ Error al registrar cliente: {e}")
        input("\nPresione [Enter] para regresar...")


def listar_clientes_ui(servicio: Restaurante):
    print("\n=== LISTADO DE CLIENTES REGISTRADOS ===")
    clientes = servicio.listar_clientes()
    
    if not clientes:
        print("No hay clientes registrados en el sistema.")
    else:
        for index, cliente in enumerate(clientes, 1):
            print(f"[{index}] ", end="")
            cliente.mostrar_informacion()

    explicacion = (
        "1. Transmisión de Objetos -> Se obtienen y muestran los objetos Cliente de la capa de servicio.\n"
        "2. Representación Limpia -> Las dataclasses proveen métodos predeterminados de visualización,\n"
        "   pero aquí utilizamos un método personalizado para mantener un formato visual homogéneo."
    )
    mostrar_explicacion_didactica("Listado de Estructuras de Datos de tipo Cliente", explicacion)


def buscar_cliente_ui(servicio: Restaurante):
    print("\n--- BUSCAR CLIENTE ---")
    id_cliente = input("Ingrese el identificador (Cédula/RUC) del cliente: ").strip()
    cliente = servicio.buscar_cliente(id_cliente)

    if cliente is None:
        print(f"\nNo se encontró ningún cliente con identificador '{id_cliente}'.")
    else:
        print(f"\nCliente encontrado:")
        print("-" * 35)
        cliente.mostrar_informacion()

    explicacion = (
        "1. Búsqueda por Llave Única -> El servicio busca la coincidencia exacta de 'id_cliente'.\n"
        "2. Retorno de Referencias -> Se retorna la referencia directa del objeto encontrado en la lista\n"
        "   o None en caso de no existir, permitiendo al frontend tomar la decisión de qué mostrar."
    )
    mostrar_explicacion_didactica("Búsqueda en Capa de Servicio por Identificador Único", explicacion)


def main():
    # Instanciamos el servicio principal (Restaurante)
    mi_restaurante = Restaurante()
    
    # Precargamos los datos para fines didácticos
    precargar_datos_ejemplo(mi_restaurante)

    while True:
        limpiar_pantalla()
        print("========================================")
        print("        SISTEMA DE RESTAURANTE")
        print("========================================")
        print("1. Registrar producto")
        print("2. Listar productos")
        print("3. Buscar producto")
        print("----------------------------------------")
        print("4. Registrar cliente")
        print("5. Listar clientes")
        print("6. Buscar cliente")
        print("----------------------------------------")
        print("7. Salir")
        print("========================================")
        
        opcion = input("Seleccione una opción (1-7): ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            registrar_producto_ui(mi_restaurante)
        elif opcion == "2":
            limpiar_pantalla()
            listar_productos_ui(mi_restaurante)
        elif opcion == "3":
            limpiar_pantalla()
            buscar_producto_ui(mi_restaurante)
        elif opcion == "4":
            limpiar_pantalla()
            registrar_cliente_ui(mi_restaurante)
        elif opcion == "5":
            limpiar_pantalla()
            listar_clientes_ui(mi_restaurante)
        elif opcion == "6":
            limpiar_pantalla()
            buscar_cliente_ui(mi_restaurante)
        elif opcion == "7":
            print("\nGracias por utilizar el Sistema de Restaurante. ¡Hasta pronto!\n")
            break
        else:
            print("\n❌ Opción no válida. Intente nuevamente.")
            input("Presione [Enter] para continuar...")


if __name__ == "__main__":
    main()
