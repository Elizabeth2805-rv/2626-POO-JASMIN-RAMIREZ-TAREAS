# restaurante_app — Semana 8

**Estudiante:** Jasmin Ramirez  
**Asignatura:** Programación Orientada a Objetos  
**Semana:** 8 — Principios SOLID (SRP, OCP, LSP)

---

## Descripción del sistema

`restaurante_app` es un sistema de gestión básica de productos, bebidas y clientes de un restaurante, desarrollado en Python con Programación Orientada a Objetos. Permite registrar y listar productos generales, bebidas y clientes mediante un menú interactivo ejecutado desde consola.

El proyecto evoluciona la versión de la Semana 7 incorporando la clase `Bebida` mediante herencia y aplicando de forma explícita los principios **SRP**, **OCP** y **LSP** de SOLID.

---

## Estructura del proyecto

```
restaurante_app/
├── modelos/
│   ├── __init__.py       # Expone Producto, Bebida y Cliente
│   ├── producto.py       # Clase base Producto
│   ├── bebida.py         # Clase hija Bebida (hereda de Producto)
│   └── cliente.py        # Clase Cliente (independiente de Producto)
├── servicios/
│   ├── __init__.py       # Expone Restaurante
│   └── restaurante.py    # Clase de servicio Restaurante
└── main.py               # Punto de arranque e interacción por consola
```

---

## Responsabilidad de cada clase

| Clase | Archivo | Responsabilidad |
|---|---|---|
| `Producto` | `modelos/producto.py` | Representar un producto general con código, nombre, categoría y precio. Definir `mostrar_informacion()`. |
| `Bebida` | `modelos/bebida.py` | Especializar `Producto` añadiendo tamaño y tipo de envase. Sobrescribir `mostrar_informacion()`. |
| `Cliente` | `modelos/cliente.py` | Representar un cliente con identificación, nombre y correo. |
| `Restaurante` | `servicios/restaurante.py` | Administrar las colecciones de productos (incluye bebidas) y clientes. Validar duplicados. |
| `main.py` | `main.py` | Mostrar el menú, solicitar datos con `input()`, crear objetos y llamar al servicio. |

---

## Relación entre Producto y Bebida

`Bebida` hereda de `Producto` porque **una bebida ES un tipo de producto**. La herencia es válida y semánticamente correcta.

```
Producto  (clase base)
    └── Bebida  (clase hija — especialización)
```

`Cliente` **no** hereda de `Producto` porque un cliente no es un producto. La herencia solo se aplica cuando existe una relación "es un" real.

---

## Principios SOLID aplicados

### S — Responsabilidad Única (SRP)
Cada clase cumple exactamente una responsabilidad:
- `Producto` y `Bebida` representan productos.
- `Cliente` representa un cliente.
- `Restaurante` administra las colecciones y las reglas de negocio.
- `main.py` coordina la interacción por consola.

### O — Abierto/Cerrado (OCP)
La clase `Bebida` amplía el sistema añadiendo atributos específicos (tamaño, tipo de envase) **sin modificar** la clase `Producto` ni la lógica del servicio `Restaurante`. Para agregar un nuevo tipo de producto en el futuro basta con crear una nueva subclase de `Producto`.

### L — Sustitución de Liskov (LSP)
Un objeto `Bebida` puede utilizarse en cualquier lugar donde se espere un `Producto`:
- El servicio `Restaurante` almacena `Producto` y `Bebida` en **una sola colección** (`_productos`).
- El método `registrar_producto()` acepta cualquier instancia de `Producto` o sus subclases.
- Durante el listado, se llama a `mostrar_informacion()` sobre todos los objetos de la lista **sin preguntar qué tipo concreto es cada uno**. Cada objeto responde correctamente según su propia implementación (polimorfismo).

---

## Instrucciones de ejecución

**Requisitos:** Python 3.8 o superior. No se requieren dependencias externas.

```bash
# Desde la carpeta restaurante_app/
python main.py
```

### Opciones del menú

```
================================================
         SISTEMA DE RESTAURANTE
================================================
  1. Registrar producto
  2. Registrar bebida
  3. Registrar cliente
  ------------------------------------------
  4. Listar productos
  5. Listar clientes
  ------------------------------------------
  6. Salir
================================================
```

### Ejemplo de flujo

1. Seleccionar **opción 1** → ingresar código `P001`, nombre `Hamburguesa con Queso`, categoría `Plato Fuerte`, precio `8.50`.
2. Seleccionar **opción 2** → ingresar código `B001`, nombre `Limonada Imperial`, categoría `Bebidas`, precio `2.75`, tamaño `mediano`, envase `vaso`.
3. Seleccionar **opción 3** → ingresar cédula `0987654321`, nombre `Jasmin Ramirez`, correo `jasmin@correo.com`.
4. Seleccionar **opción 4** → el sistema lista P001 y B001 usando `mostrar_informacion()` de cada objeto (polimorfismo).
5. Seleccionar **opción 5** → el sistema lista los clientes registrados.

---

## Reflexión

Diseñar proyectos aplicando los principios SOLID produce sistemas **mantenibles, escalables y comprensibles**. Cuando cada clase cumple una sola responsabilidad, encontrar y corregir errores resulta más sencillo porque el problema está acotado a un único lugar. Cuando el sistema está abierto a la extensión pero cerrado a la modificación, añadir nuevas funcionalidades (como la clase `Bebida`) no introduce riesgos en el código ya probado. Y cuando se respeta la sustitución de Liskov, el polimorfismo funciona de forma natural: el servicio `Restaurante` no necesita saber si está procesando un `Producto` o una `Bebida`; simplemente invoca el contrato común y cada objeto cumple su parte. Estos principios no son restricciones, sino herramientas que permiten que el código crezca sin convertirse en un problema.
