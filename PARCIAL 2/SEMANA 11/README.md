# restaurante_app — Semana 11: Colecciones, Relaciones, Ventas y Persistencia JSON

**Estudiante:** Jasmin Ramirez  
**Asignatura:** Programación Orientada a Objetos (POO) — 2do. Semestre  
**Parcial:** 2 | **Semana:** 11  

---

## 📋 Descripción General del Sistema

El sistema `restaurante_app` evoluciona en la **Semana 11** para aplicar de forma integral los conceptos de **colecciones de objetos, relaciones entre entidades, control de stock y persistencia completa en archivos JSON**.

En esta versión:
1. **Producto** gestiona la cantidad disponible en almacén (`stock`) evitando valores negativos.
2. **Usuario** amplía sus funcionalidades permitiendo persistencia física completa en `usuarios.json`.
3. **Venta** se incorpora como una nueva entidad de dominio que representa de forma explícita la relación entre un `Usuario` y un `Producto` adquirido.
4. **Restaurante** (Servicio) coordina las colecciones en memoria, controla las reglas de negocio (validación de stock, existencia de entidades) y realiza consultas filtradas de ventas por usuario.
5. **ArchivoServicio** centraliza la lectura (`json.load`) y escritura (`json.dump`) de los archivos `productos.json`, `usuarios.json` y `ventas.json`, garantizando el manejo transparente de excepciones físicas de archivos.

---

## 📁 Estructura del Proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json          # Almacena el catálogo de productos y su stock actualizado
│   ├── usuarios.json           # Almacena los usuarios registrados en el sistema
│   └── ventas.json             # Almacena las transacciones realizadas (Usuario -> Producto)
├── modelos/
│   ├── __init__.py             # Exposición del paquete modelos
│   ├── producto.py             # Clase Producto (validaciones, stock, vender(), to_dict, from_dict)
│   ├── usuario.py              # Clase Usuario (validaciones, to_dict, from_dict)
│   └── venta.py                # Clase Venta (relación usuario_id, producto_codigo, cantidad)
├── servicios/
│   ├── __init__.py             # Exposición del paquete servicios
│   ├── archivo_servicio.py     # Servicio I/O para JSON y manejo de excepciones de archivos
│   └── restaurante.py          # Servicio de gestión de colecciones y reglas de negocio
├── main.py                     # Coordinador de interfaz de consola y flujo principal
└── README.md                   # Documentación técnica completa de la Semana 11
```

---

## 🚀 Forma de Ejecución

1. Abrir la terminal en la carpeta del proyecto:
   ```bash
   cd "PARCIAL 2/SEMANA 11/restaurante_app"
   ```

2. Ejecutar el script principal:
   ```bash
   python main.py
   ```
