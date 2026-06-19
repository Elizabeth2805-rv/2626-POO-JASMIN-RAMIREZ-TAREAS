# SISTEMA DE GESTIÓN DE RESTAURANTE - DOCUMENTACIÓN

## Descripción del Proyecto

Este es un sistema básico de gestión de restaurante desarrollado en Python usando Programación Orientada a Objetos (OOP). El objetivo es demostrar la organización de un proyecto en módulos, la separación de responsabilidades y la correcta comunicación entre archivos mediante importaciones.

## Estructura del Proyecto

```
restaurante_app/
├── modelos/
│   ├── __init__.py
│   ├── producto.py          # Clase que representa un producto del menú
│   └── cliente.py           # Clase que representa un cliente
├── servicios/
│   ├── __init__.py
│   └── restaurante.py       # Clase que gestiona el restaurante
└── main.py                  # Punto de entrada del programa
```

## Clases Implementadas

### 1. Clase Producto (modelos/producto.py)

**Responsabilidad:** Representar un artículo disponible en el restaurante (platos, bebidas, postres).

**Atributos:**
- `id_producto`: Identificador único (ej: "P001")
- `nombre`: Nombre del producto (ej: "Carne a la parrilla")
- `descripcion`: Descripción detallada
- `precio`: Precio en pesos
- `categoria`: Categoría (entrada, plato principal, bebida, postre)

**Métodos:**
- `__init__()`: Constructor
- `__str__()`: Representación en texto del producto
- `obtener_descripcion_completa()`: Retorna descripción detallada
- `aplicar_descuento(porcentaje)`: Calcula precio con descuento

### 2. Clase Cliente (modelos/cliente.py)

**Responsabilidad:** Representar a un cliente del restaurante y gestionar sus pedidos.

**Atributos:**
- `id_cliente`: Identificador único
- `nombre`: Nombre completo del cliente
- `email`: Correo electrónico
- `telefono`: Número de teléfono
- `pedidos`: Lista de pedidos realizados
- `cantidad_pedidos`: Contador de pedidos

**Métodos:**
- `__init__()`: Constructor
- `__str__()`: Representación en texto del cliente
- `agregar_pedido()`: Registra un nuevo pedido
- `obtener_historial_pedidos()`: Retorna lista de pedidos
- `obtener_total_gastado()`: Calcula gasto total acumulado

### 3. Clase Restaurante (servicios/restaurante.py)

**Responsabilidad:** Gestionar todas las operaciones del restaurante: productos, clientes y pedidos.

**Atributos:**
- `nombre`: Nombre del restaurante
- `direccion`: Dirección física
- `productos`: Lista de productos disponibles
- `clientes`: Lista de clientes registrados
- `pedidos_realizados`: Registro de todos los pedidos

**Métodos principales:**
- `__init__()`: Constructor
- `agregar_producto()`: Añade un producto al menú (valida duplicados)
- `agregar_cliente()`: Registra un cliente (valida duplicados)
- `buscar_producto()`: Busca un producto por ID
- `buscar_cliente()`: Busca un cliente por ID
- `registrar_pedido()`: Procesa un pedido de un cliente
- `mostrar_productos()`: Muestra menú organizado por categorías
- `mostrar_clientes()`: Muestra lista de clientes registrados
- `mostrar_pedidos()`: Muestra historial de pedidos
- `mostrar_informacion_general()`: Muestra resumen del restaurante

## Conceptos OOP Implementados

### 1. Encapsulación
- Cada clase tiene responsabilidades bien definidas
- Los atributos se agrupan lógicamente dentro de cada clase
- Los métodos pertenecen a la clase que maneja los datos

### 2. Abstracción
- Las clases del modelo (Producto, Cliente) representan conceptos reales del negocio
- Los detalles de implementación están ocultos en los métodos
- La lógica de negocio está centralizada en la clase Restaurante

### 3. Modularización
- **modelos/**: Contiene clases de datos (entidades del negocio)
- **servicios/**: Contiene clases que manejan la lógica de negocio
- **main.py**: Punto de entrada que demuestra el uso del sistema

### 4. Reutilización de Código
- Las clases se importan en los archivos que las necesitan
- Los objetos se reutilizan múltiples veces (ej: un cliente se agrega una sola vez)

## Características Destacadas

✓ **Método __init__()**: Todas las clases principales implementan constructor
✓ **Método __str__()**: Implementado para representar objetos como texto legible
✓ **Importaciones correctas**: Uso de from...import para importar clases entre módulos
✓ **Validación de datos**: Previene duplicados de productos y clientes
✓ **Gestión de listas**: Uso de listas para almacenar colecciones de objetos
✓ **Búsqueda y filtrado**: Métodos para encontrar objetos específicos
✓ **Cálculos**: Funcionalidad para calcular totales y descuentos
✓ **Presentación**: Métodos que muestran información de forma organizada

## Cómo Ejecutar el Programa

```bash
# Navegar a la carpeta del proyecto
cd restaurante_app

# Ejecutar el programa
python main.py
```

## Flujo de Ejecución

1. Se crea una instancia del Restaurante
2. Se crean productos y se agregan al menú
3. Se crean clientes y se registran en el sistema
4. Se muestra información del restaurante, menú y clientes
5. Se procesan pedidos que generan facturas
6. Se muestran resúmenes y estadísticas

## Diferencias con el Ejemplo de Biblioteca

A diferencia del ejemplo docente de una biblioteca, este sistema:
- Usa contexto de restaurante (productos, clientes, pedidos)
- Implementa categorización de productos
- Gestiona precios y cálculos de totales
- Incluye validación de cantidades
- Proporciona historial de pedidos por cliente
- Demuestra aplicación de descuentos

## Extensiones Posibles

El sistema puede extenderse con:
- Persistencia en base de datos
- Clase Pedido como entidad independiente
- Sistema de reservas
- Gestión de horarios
- Reporte de ventas por período
- Sistema de autenticación
