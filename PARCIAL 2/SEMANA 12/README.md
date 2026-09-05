# restaurante_app — Semana 12: Optimización de Rendimiento mediante Colecciones (Índices dict y set)

**Estudiante:** Jasmin Ramirez  
**Asignatura:** Programación Orientada a Objetos (POO) — 2do. Semestre  
**Parcial:** 2 | **Semana:** 12  

---

## 📋 Descripción General del Sistema

El sistema `restaurante_app` evoluciona en la **Semana 12** para incorporar **estructuras auxiliares en memoria (`dict` y `set`)** orientadas a la optimización del rendimiento en operaciones frecuentes de búsqueda, consulta y validación.

A partir de la versión funcional desarrollada en la Semana 11 (la cual incluye usuarios, productos, ventas, stock y persistencia en archivos JSON), se analizaron los recorridos secuenciales sobre listas completas y se aplicaron índices en tiempo constante $O(1)$ sin trasladar responsabilidades a `main.py` ni reemplazar las colecciones principales.

En esta versión:
1. **Colecciones Principales (`List`)**: Se conservan para almacenar, listar, recorrer secuencialmente y persistir los objetos en los archivos JSON (`productos.json`, `usuarios.json`, `ventas.json`).
2. **Índices de Búsqueda Frecuente (`Dict`)**:
   - `_idx_productos`: Mapea cada `codigo` a su objeto `Producto` para búsquedas inmediatas en $O(1)$.
   - `_idx_usuarios`: Mapea cada `identificacion` (cédula/ID) a su objeto `Usuario` para búsquedas inmediatas en $O(1)$.
   - `_idx_ventas_por_usuario`: Mapea cada `usuario_id` a la lista de objetos `Venta` correspondientes a dicho usuario, reduciendo el filtrado de ventas de $O(V)$ a $O(1)$.
3. **Conjuntos de Validación de Pertenencia (`Set`)**:
   - `_codigos_productos`: Mantiene los códigos registrados para verificar unicidad de productos en $O(1)$.
   - `_ids_usuarios`: Mantiene las cédulas registradas para verificar unicidad de usuarios en $O(1)$.
4. **Reconstrucción y Sincronización Automática**:
   - Al iniciar el programa, los objetos recuperados desde los archivos JSON reconstruyen los índices en memoria mediante `reconstruir_indices()`.
   - Ante cada registro, modificación o eliminación de datos, el servicio `Restaurante` actualiza simultáneamente la lista principal y las estructuras auxiliares en tiempo real.

---

## 📁 Estructura del Proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json          # Catálogo de productos y stock persistido
│   ├── usuarios.json           # Usuarios registrados persistidos
│   └── ventas.json             # Historial de ventas persistido
├── modelos/
│   ├── __init__.py             # Exposición del paquete modelos
│   ├── producto.py             # Clase Producto (datos, validación, stock, to_dict, from_dict)
│   ├── usuario.py              # Clase Usuario (datos, validaciones, to_dict, from_dict)
│   └── venta.py                # Clase Venta (relación usuario_id, producto_codigo, cantidad)
├── servicios/
│   ├── __init__.py             # Exposición del paquete servicios
│   ├── archivo_servicio.py     # Servicio I/O para lectura/escritura JSON y manejo de excepciones
│   └── restaurante.py          # Servicio de negocio con listas e índices auxiliares (dict/set)
├── main.py                     # Interfaz de consola e integración con reporte de índices
└── README.md                   # Documentación técnica completa de la Semana 12
```

---

## ⚡ Colecciones Utilizadas y Análisis de Rendimiento

| Operación / Consulta | Colección Previa (Semana 11) | Complejidad Previa | Colección Semana 12 | Complejidad Optimizada | Justificación Técnica |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **Buscar producto por código** | Iteración sobre `List[Producto]` | $O(N)$ | `Dict[str, Producto]` (`_idx_productos`) | **$O(1)$** | Acceso directo por clave hash del código único del producto. |
| **Validar existencia de código** | Iteración con `any()` sobre lista | $O(N)$ | `Set[str]` (`_codigos_productos`) | **$O(1)$** | Validación de pertenencia rápida sin recorrer la colección. |
| **Buscar usuario por cédula/ID** | Iteración sobre `List[Usuario]` | $O(M)$ | `Dict[str, Usuario]` (`_idx_usuarios`) | **$O(1)$** | Acceso directo por clave hash del número de cédula/ID. |
| **Validar existencia de usuario** | Iteración con `any()` sobre lista | $O(M)$ | `Set[str]` (`_ids_usuarios`) | **$O(1)$** | Validación de pertenencia en conjunto en tiempo constante. |
| **Consultar ventas por usuario** | Filtrado iterativo de `List[Venta]` | $O(V)$ | `Dict[str, List[Venta]]` (`_idx_ventas_por_usuario`) | **$O(1)$** | Acceso directo a la sublista de ventas indexada por usuario. |
| **Listar, ordenar y persistir** | `List` principal | $O(N)$ | `List` principal (se conserva) | $O(N)$ | Las listas mantienen el orden de inserción y facilitan la serialización JSON. |

---

## 🛠️ Arquitectura y Sincronización de Índices

Todas las operaciones de mutación en `servicios/restaurante.py` mantienen **estricta sincronización** entre la lista principal y las estructuras auxiliares:

```
                          ┌───────────────────────────┐
                          │   OBJETOS EN MEMORIA      │
                          └─────────────┬─────────────┘
                                        │
             ┌──────────────────────────┼──────────────────────────┐
             ▼                          ▼                          ▼
  ┌───────────────────┐      ┌────────────────────┐     ┌───────────────────┐
  │ Listas Principales│      │ Diccionarios Index │     │  Conjuntos Set    │
  │ - _productos      │      │ - _idx_productos   │     │ - _codigos_prods  │
  │ - _usuarios       │      │ - _idx_usuarios    │     │ - _ids_usuarios   │
  │ - _ventas         │      │ - _idx_ventas_usr  │     └───────────────────┘
  └─────────┬─────────┘      └────────────────────┘
            │
            ▼ (to_dict / json.dump)
  ┌───────────────────┐
  │  Archivos JSON    │
  └───────────────────┘
```

1. **Al Cargar Datos (`JSON -> Objetos`)**: `reconstruir_indices()` recorre las listas recién deserializadas e indexa las claves en `_idx_productos`, `_idx_usuarios`, `_idx_ventas_por_usuario`, `_codigos_productos` y `_ids_usuarios`.
2. **Al Registrar Producto**: Se añade el objeto a `_productos` (lista), se asigna `_idx_productos[codigo] = producto` (dict) y `_codigos_productos.add(codigo)` (set).
3. **Al Eliminar Producto**: Se remueve de `_productos` (lista), se ejecuta `_idx_productos.pop(codigo)` (dict) y `_codigos_productos.discard(codigo)` (set).
4. **Al Registrar Usuario**: Se añade a `_usuarios` (lista), `_idx_usuarios[id] = usuario` (dict), `_ids_usuarios.add(id)` (set) y se inicializa la lista `_idx_ventas_por_usuario[id] = []`.
5. **Al Realizar una Venta**: Se añade a `_ventas` (lista) y se anexa inmediatamente a `_idx_ventas_por_usuario[usuario_id]` (dict de sublistas).

---

## 🚀 Forma de Ejecución

1. Abrir la terminal en la carpeta del proyecto:
   ```bash
   cd "PARCIAL 2/SEMANA 12/restaurante_app"
   ```

2. Ejecutar la aplicación principal:
   ```bash
   python main.py
   ```

---

## 🧪 Comprobación de Funcionamiento y Pruebas Realizadas

Se llevaron a cabo las siguientes pruebas de verificación en `main.py`:

1. **Reconstrucción al Iniciar**:
   - Al ejecutar `python main.py`, el sistema cargó los registros JSON y construyó automáticamente los índices en memoria, mostrando en consola los objetos e índices sincronizados.

2. **Búsqueda Frecuente de Productos por Código**:
   - Se ejecutó la Opción 2 (`Buscar producto por código`) consultando `P001`. El sistema retornó el producto al instante utilizando el diccionario `_idx_productos`.

3. **Búsqueda de Usuario por Identificación**:
   - Se ejecutó la Opción 7 (`Buscar usuario por cédula/ID`) consultando `0102030405`. El sistema retornó al usuario inmediatamente mediante `_idx_usuarios`.

4. **Consulta Optimizada de Ventas por Usuario**:
   - Se ejecutó la Opción 10 (`Consultar ventas por usuario`) para el usuario `0102030405`. Las ventas se obtuvieron de la sublista indexada `_idx_ventas_por_usuario` sin recorrer la lista general de ventas.

5. **Venta y Sincronización de Stock/Índices**:
   - Se vendieron 2 unidades del producto `P003` al usuario `0102030405`. El stock se actualizó y la nueva venta se indexó al instante en `_idx_ventas_por_usuario`.

6. **Diagnóstico de Coherencia de Índices**:
   - Se seleccionó la Opción 12 (`Ver estado de índices en memoria`). Se verificó la paridad total de elementos entre listas principales (`List`), diccionarios (`Dict`) y conjuntos (`Set`).

7. **Persistencia y Reconstrucción tras Reinicio**:
   - Se cerró el programa (Opción 13) y se volvió a ejecutar `python main.py`. Todos los datos persistidos en los archivos `.json` se reconstruyeron exitosamente en memoria con sus índices auxiliares.
