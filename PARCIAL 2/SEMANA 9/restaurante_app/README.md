# restaurante_app — Semana 9 (Persistencia JSON)

**Estudiante:** Jasmín Elizabeth Ramírez Vaca  
**Asignatura:** Programación Orientada a Objetos (Python) — 2.º Semestre  
**Semana:** 9 — Persistencia de datos en archivos JSON  
**Docente:** Ing. Edwin Gustavo Fernández Sánchez, Mgs.

---

## Descripción del sistema

`restaurante_app` es un sistema de administración básica para un restaurante
desarrollado de forma incremental a lo largo del curso. Esta versión corresponde
a la **Semana 9** y representa una evolución directa del proyecto de la Semana 8.

La mejora principal consiste en incorporar **persistencia de datos en archivos
JSON**: los productos, bebidas y clientes registrados durante una sesión se
guardan automáticamente en archivos con estructura de diccionario, y se
recuperan al iniciar el programa en una sesión posterior.

---

## Estructura del proyecto

```
restaurante_app/
├── modelos/
│   ├── __init__.py         # Expone Producto, Bebida y Cliente como paquete
│   ├── producto.py         # Clase Producto + serialización to_dict / from_dict
│   ├── bebida.py           # Clase Bebida (hereda de Producto) + serialización
│   └── cliente.py          # Clase Cliente + serialización to_dict / from_dict
├── servicios/
│   ├── __init__.py         # Expone Restaurante como paquete
│   └── restaurante.py      # Servicio: administra colecciones + persistencia JSON
├── almacenamiento/
│   ├── __init__.py         # Expone GestorJSON como paquete
│   └── gestor_json.py      # Lectura y escritura de archivos JSON
├── datos/                  # Generado automáticamente al ejecutar el programa
│   ├── productos.json      # Lista de dicts de productos y bebidas
│   └── clientes.json       # Lista de dicts de clientes
├── main.py                 # Punto de arranque e interfaz por consola
└── README.md               # Documentación del proyecto
```

---

## Responsabilidad de cada componente

| Archivo | Responsabilidad |
|---|---|
| `modelos/producto.py` | Representa un producto (código, nombre, categoría, precio). Valida sus datos. Serializa/deserializa como diccionario (`to_dict` / `from_dict`). |
| `modelos/bebida.py` | Extiende Producto con tamaño y envase. Sobrescribe `to_dict` / `from_dict` para incluir sus atributos adicionales. |
| `modelos/cliente.py` | Representa un cliente (identificación, nombre, correo). Valida sus datos. Serializa/deserializa como diccionario. |
| `almacenamiento/gestor_json.py` | **Única responsabilidad**: leer y escribir archivos JSON. No construye objetos de dominio ni interactúa con la consola. |
| `servicios/restaurante.py` | Administra las colecciones de productos y clientes. Coordina la persistencia con `GestorJSON`. Carga datos al iniciar y guarda después de cada operación. |
| `main.py` | Muestra el menú, solicita datos por consola, construye objetos y delega toda operación al servicio. No accede directamente a archivos ni colecciones internas. |

---

## Estructura de los archivos JSON

### `datos/productos.json`

Cada producto o bebida se almacena como un **diccionario** dentro de una lista.
La clave `"tipo"` permite distinguir entre `Producto` y `Bebida` al momento de
reconstruir los objetos.

```json
[
    {
        "tipo": "Producto",
        "codigo": "P001",
        "nombre": "Bandeja Paisa",
        "categoria": "Plato Fuerte",
        "precio": 25000.0
    },
    {
        "tipo": "Bebida",
        "codigo": "B001",
        "nombre": "Limonada de Coco",
        "categoria": "Bebidas",
        "precio": 8000.0,
        "tamano": "mediano",
        "tipo_envase": "vaso"
    }
]
```

### `datos/clientes.json`

Cada cliente se almacena como un **diccionario** dentro de una lista.

```json
[
    {
        "identificacion": "1012345678",
        "nombre": "Ana Torres",
        "correo": "ana@correo.com"
    }
]
```

---

## Flujo de persistencia

```
main.py crea Restaurante(directorio_datos)
        ↓
Restaurante inicializa GestorJSON
        ↓
GestorJSON lee productos.json y clientes.json
        ↓
Restaurante reconstruye objetos desde los diccionarios (from_dict)
        ↓
── Sesión activa ──
        ↓
Usuario registra / actualiza / elimina un dato
        ↓
Restaurante modifica la colección en memoria
        ↓
Restaurante llama a GestorJSON para guardar el estado
        ↓
GestorJSON convierte objetos a dicts (to_dict) y escribe el archivo JSON
```

---

## Instrucciones para ejecutar el programa

### Requisitos

- Python 3.10 o superior instalado.
- No se requieren bibliotecas externas (solo módulos estándar: `json`, `os`).

### Pasos

1. Clonar o descargar el repositorio.
2. Abrir una terminal en la carpeta `restaurante_app/`.
3. Ejecutar:

```bash
python main.py
```

4. La carpeta `datos/` se crea automáticamente en el primer uso.
5. Los datos persisten entre sesiones; al volver a ejecutar el programa,
   los registros anteriores se cargan automáticamente.

### Menú del programa

```
==================================================
         SISTEMA DE RESTAURANTE
         (Con persistencia JSON)
==================================================
  1. Registrar producto
  2. Registrar bebida
  3. Buscar producto
  4. Actualizar producto
  5. Eliminar producto
  --------------------------------------------
  6. Listar productos
  --------------------------------------------
  7. Registrar cliente
  8. Listar clientes
  --------------------------------------------
  9. Salir
==================================================
```

---

## Evolución del proyecto

| Semana | Mejora incorporada |
|---|---|
| Semanas 2–7 | Clases básicas, encapsulamiento, propiedades |
| Semana 8 | Herencia (`Bebida` extiende `Producto`), principios SOLID |
| **Semana 9** | **Persistencia JSON con estructura tipo diccionario; paquete `almacenamiento`; métodos `to_dict` / `from_dict`; CRUD completo de productos** |
