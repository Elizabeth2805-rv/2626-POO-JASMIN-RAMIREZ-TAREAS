# GUÍA DE USO - EJEMPLOS PRÁCTICOS

## Cómo Usar las Clases del Sistema

### 1. Crear un Producto

```python
from modelos.producto import Producto

# Crear un producto
producto = Producto(
    id_producto="P007",
    nombre="Pizza Margarita",
    descripcion="Pizza tradicional italiana",
    precio=35000,
    categoria="plato principal"
)

# Ver información del producto
print(producto)
# Salida: [P007] Pizza Margarita (plato principal) - $35000.00 - Pizza tradicional italiana

# Obtener descripción completa
print(producto.obtener_descripcion_completa())
# Salida: Pizza Margarita: Pizza tradicional italiana

# Calcular descuento
print(producto.aplicar_descuento(15))  # 15% de descuento
# Salida: 29750.0
```

### 2. Crear un Cliente

```python
from modelos.cliente import Cliente

# Crear un cliente
cliente = Cliente(
    id_cliente="C004",
    nombre="Ana Martínez",
    email="ana.martinez@email.com",
    telefono="3009999999"
)

# Ver información del cliente
print(cliente)
# Salida: [ID: C004] Ana Martínez - Email: ana.martinez@email.com - 
#         Teléfono: 3009999999 - Pedidos realizados: 0

# Agregar un pedido al cliente
pedido = {
    'productos': ['Pizza Margarita', 'Refresco'],
    'total': 43000
}
cliente.agregar_pedido(pedido)

# Verificar cantidad de pedidos
print(cliente.cantidad_pedidos)  # Salida: 1
```

### 3. Usar el Restaurante

```python
from servicios.restaurante import Restaurante
from modelos.producto import Producto
from modelos.cliente import Cliente

# Crear el restaurante
mi_restaurante = Restaurante(
    nombre="Restaurant Ejemplo",
    direccion="Calle 5 #123"
)

# Agregar productos
producto1 = Producto("P001", "Ensalada", "Ensalada fresca", 20000, "entrada")
mi_restaurante.agregar_producto(producto1)

# Agregar clientes
cliente1 = Cliente("C001", "Pedro", "pedro@email.com", "3001111111")
mi_restaurante.agregar_cliente(cliente1)

# Registrar un pedido
mi_restaurante.registrar_pedido("C001", [("P001", 2)])

# Mostrar información
mi_restaurante.mostrar_informacion_general()
mi_restaurante.mostrar_productos()
mi_restaurante.mostrar_clientes()
mi_restaurante.mostrar_pedidos()
```

## Validaciones Implementadas

### Validación de Duplicados

El sistema valida que no existan:
- Dos productos con el mismo ID
- Dos clientes con el mismo ID

```python
# Intento agregar un producto duplicado
restaurante.agregar_producto(producto1)  # OK
restaurante.agregar_producto(producto1)  # Error: El producto con ID P001 ya existe
```

### Validación de Búsqueda

Antes de registrar un pedido, el sistema verifica:
- Que el cliente exista en el sistema
- Que todos los productos del pedido existan en el menú

```python
# Intento hacer un pedido con un cliente inexistente
restaurante.registrar_pedido("C999", [("P001", 1)])
# Error: Cliente con ID C999 no encontrado
```

## Métodos Útiles

### Búsqueda de Productos
```python
producto = restaurante.buscar_producto("P001")
if producto:
    print(f"Encontrado: {producto.nombre}")
else:
    print("Producto no encontrado")
```

### Búsqueda de Clientes
```python
cliente = restaurante.buscar_cliente("C001")
if cliente:
    print(f"Cliente: {cliente.nombre}")
else:
    print("Cliente no encontrado")
```

### Cálculo de Totales
```python
# Total gastado por un cliente específico
cliente = restaurante.buscar_cliente("C001")
total = cliente.obtener_total_gastado()
print(f"Total gastado: ${total:.2f}")
```

## Consultas Comunes

### ¿Cuántos pedidos ha hecho un cliente?
```python
cliente = restaurante.buscar_cliente("C001")
print(f"Pedidos realizados: {cliente.cantidad_pedidos}")
```

### ¿Cuál es el ingreso total del restaurante?
```python
total_ingresos = sum(pedido['total'] for pedido in restaurante.pedidos_realizados)
print(f"Ingresos totales: ${total_ingresos:.2f}")
```

### ¿Cuántos productos hay en el menú?
```python
print(f"Productos disponibles: {len(restaurante.productos)}")
```

### ¿Cuántos clientes están registrados?
```python
print(f"Clientes registrados: {len(restaurante.clientes)}")
```

## Estructura de un Pedido

Cuando se registra un pedido, el sistema crea un diccionario con esta estructura:

```python
{
    'cliente': 'Nombre del Cliente',
    'detalle': [
        {
            'producto': 'Nombre del Producto',
            'cantidad': 2,
            'subtotal': 100000
        },
        # ... más items ...
    ],
    'total': 250000
}
```

## Tips para Extender el Sistema

1. **Agregar más categorías de productos**: Simplemente usa nuevas categorías al crear productos
2. **Agregar más atributos a Cliente**: Modifica la clase Cliente añadiendo nuevos atributos en `__init__()`
3. **Agregar más métodos a Restaurante**: Crea métodos adicionales en la clase Restaurante para nuevas funcionalidades
4. **Generar reportes**: Usa los métodos de búsqueda para crear reportes personalizados
5. **Exportar datos**: Los diccionarios de pedidos pueden ser fácilmente exportados a CSV o JSON

