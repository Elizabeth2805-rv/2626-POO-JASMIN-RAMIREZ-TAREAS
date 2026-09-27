# 🍽️ Semana 15 — Conceptos Fundamentales de Manejo de Eventos

**Asignatura:** Programación Orientada a Objetos (POO)  
**Semestre:** 2do Semestre  
**Estudiante:** Jasmin Ramirez  
**Proyecto:** `restaurante_app`  

---

## 📋 Resumen de la Actividad

Esta carpeta contiene la solución completa a la tarea de la **Semana 15**, enfocada en los **Conceptos fundamentales de manejo de eventos**. A partir del proyecto `restaurante_app` desarrollado en semanas anteriores, se incorporó el módulo de **Ventas** para demostrar de forma práctica cómo una acción del usuario en la interfaz activa una respuesta en el sistema mediante el uso de `command=` y *callbacks*, manteniendo la arquitectura en capas y la persistencia física en formato JSON.

---

## 📂 Estructura General del Entregable

```
PARCIAL 2/SEMANA 15/
├── README.md                      # Documentación del entregable de la Semana 15
└── restaurante_app/               # Aplicación completa evolucionada
    ├── datos/
    │   ├── productos.json         # Datos persistentes de productos
    │   ├── usuarios.json          # Datos persistentes de usuarios
    │   └── ventas.json            # Persistencia física de ventas registradas
    ├── modelos/
    │   ├── __init__.py
    │   ├── producto.py            # Entidad Producto
    │   ├── usuario.py             # Entidad Usuario
    │   └── venta.py               # Entidad Venta (Relación Usuario-Producto)
    ├── servicios/
    │   ├── __init__.py
    │   ├── archivo_servicio.py    # Persistencia I/O y lectura/escritura de JSON
    │   └── restaurante_servicio.py # Servicio de negocio (Validaciones y CRUD)
    ├── ui/
    │   ├── __init__.py
    │   ├── login_view.py          # Vista de Login con logo e imágenes de assets/
    │   └── main_view.py           # Dashboard interactivo (Ventas, Productos, Usuarios)
    ├── assets/                    # Recursos visuales obligatorios
    │   ├── logo.png               # Logo del sistema
    │   ├── app_icon.png           # Ícono de la ventana principal
    │   ├── icon_producto.png     # Ícono para el menú de productos
    │   ├── icon_usuario.png      # Ícono para el menú de usuarios
    │   └── icon_venta.png        # Ícono para el menú de ventas
    ├── main.py                    # Punto de entrada de la aplicación
    └── README.md                  # Manual y documentación técnica interna
```

---

## 🎯 Elementos Clave Implementados

1. **Flujo Evento-Servicio**:
   - `Usuario` ➔ Clic en botón "Registrar venta" ➔ `command=self._on_registrar_venta` ➔ `Callback` ➔ `RestauranteServicio` ➔ `ventas.json` ➔ `Actualización visual en UI`.
2. **Modelo Venta**:
   - Incorporado en `modelos/venta.py` para vincular `identificacion_usuario`, `codigo_producto`, fecha/hora y total.
3. **Persistencia en `ventas.json`**:
   - Administrada mediante `ArchivoServicio` y coordinada por `RestauranteServicio`.
4. **Descuento de Stock**:
   - Al registrar una venta exitosa, el stock del producto disminuye en 1 unidad y se actualiza en `productos.json`.
5. **Uso de Assets**:
   - Integración de íconos y logo desde la carpeta `assets/` en los contenedores de la UI.

---

## 🚀 Instrucciones de Ejecución

1. Abrir la terminal e ingresar a la carpeta del proyecto:
   ```bash
   cd "PARCIAL 2/SEMANA 15/restaurante_app"
   ```
2. Ejecutar la aplicación:
   ```bash
   python main.py
   ```
