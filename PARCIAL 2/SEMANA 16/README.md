# 🍽️ Semana 16 — Manejo de Eventos en Tkinter (Gestión de Usuarios)

**Asignatura:** Programación Orientada a Objetos (POO)  
**Semestre:** 2do Semestre  
**Estudiante:** Jasmin Ramirez  
**Proyecto:** `restaurante_app`  

---

## 📋 Resumen de la Actividad

Esta carpeta contiene el entregable correspondiente a la **Semana 16** sobre **Manejo de Eventos en Tkinter**. La actividad evoluciona el proyecto `restaurante_app`, expandiendo la sección de **Usuarios** para aplicar de forma práctica eventos en interfaz gráfica como `<<TreeviewSelect>>`, `<Return>`, `<Escape>` y `<<ComboboxSelected>>`, vinculados mediante el método `bind()`, mientras se conservan los botones principales mediante `command=`.

---

## 📂 Estructura del Entregable

```text
PARCIAL 2/SEMANA 16/
├── README.md                      # Documentación principal del entregable de la Semana 16
└── restaurante_app/               # Proyecto evolved con arquitectura modular
    ├── datos/
    │   ├── productos.json         # Persistencia de productos
    │   ├── usuarios.json          # Persistencia de usuarios con el atributo 'rol'
    │   └── ventas.json            # Persistencia de ventas
    ├── modelos/
    │   ├── __init__.py
    │   ├── producto.py            # Modelo Producto
    │   ├── usuario.py             # Modelo Usuario con atributo rol
    │   └── venta.py               # Modelo Venta
    ├── servicios/
    │   ├── __init__.py
    │   ├── archivo_servicio.py    # Servicio I/O para JSON
    │   └── restaurante_servicio.py # Servicio de negocio (CRUD + validaciones)
    ├── ui/
    │   ├── __init__.py
    │   ├── login_view.py          # Vista de inicio de sesión
    │   └── main_view.py           # Dashboard principal (Eventos en Usuarios, Productos y Ventas)
    ├── assets/                    # Recursos visuales obligatorios (íconos y logo)
    ├── main.py                    # Punto de entrada de la aplicación
    └── README.md                  # Documentación interna del módulo restaurante_app
```

---

## 🎯 Requisitos de la Semana 16 Cumplidos

1. **Atributo `rol` en el modelo `Usuario`**:
   - Roles integrados: `Administrador`, `Empleado`, `Cliente`.
   - Persistencia automática en `usuarios.json`.

2. **Manejo de Eventos Demostrado**:
   - `<<TreeviewSelect>>`: Carga los datos de la fila seleccionada en la tabla hacia el formulario mediante `RestauranteServicio`.
   - `<Return>`: Confirma el registro del usuario como atajo de teclado reutilizando el callback `_on_registrar_usuario`.
   - `<Escape>`: Limpia el formulario, deselecciona las filas del Treeview y devuelve la interfaz a su estado inicial.
   - `<<ComboboxSelected>>`: Responde en tiempo real a la selección del rol en el formulario.
   - `command=`: Se mantiene en los botones `Registrar`, `Consultar`, `Actualizar`, `Eliminar` y `Limpiar`.

3. **Control de Acceso y Seguridad de Sesión**:
   - Únicamente los usuarios con rol `Administrador` pueden modificar la gestión de usuarios.
   - Protección contra auto-eliminación: El Administrador autenticado no puede borrar su propia cuenta en sesión activa.

4. **Reutilización y Separación de Capas**:
   - La interfaz responde a eventos y actualiza la vista.
   - Las reglas de negocio, validaciones y persistencia se delegan completamente a `RestauranteServicio`.

---

## 🚀 Instrucciones de Ejecución

1. Abrir una terminal y navegar al directorio:
   ```bash
   cd "PARCIAL 2/SEMANA 16/restaurante_app"
   ```

2. Ejecutar la aplicación:
   ```bash
   python main.py
   ```

3. Credenciales de prueba:
   - **Usuario Administrador**: `0102030405`
   - **Usuario Empleado**: `0987654321`
   - **Usuario Cliente**: `0995891298`
   - **Contraseña**: `1234`
