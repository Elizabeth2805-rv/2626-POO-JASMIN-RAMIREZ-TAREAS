# 🍽️ Restaurante App — Semana 15: Manejo de Eventos (GUI Tkinter)

**Asignatura:** Programación Orientada a Objetos (POO)  
**Semestre:** 2do Semestre  
**Estudiante:** Jasmin Ramirez  
**Tema:** Conceptos fundamentales de manejo de eventos  

---

## 📌 Descripción del Proyecto y Propósito

El proyecto **Restaurante App (Semana 15)** evoluciona la aplicación gráfica desarrollada en semanas anteriores conservando su arquitectura modular por capas, la persistencia en archivos JSON y la organización visual.

En esta semana 15, el propósito central es comprender y demostrar los **fundamentos básicos del manejo de eventos** utilizando las operaciones del dominio del restaurante (relacionando **Usuarios**, **Productos** y **Ventas**).

Se demuestra cómo una acción del usuario (clic en un botón) desencadena una respuesta coordinada a través del parámetro `command=` y un método *callback*, delegando toda la lógica de negocio al servicio correspondiente (`RestauranteServicio`) y actualizando la interfaz y la persistencia física en tiempo real.

---

## 🔄 Evolución del Sistema (Semana 14 ➔ Semana 15)

1. **Módulo de Ventas Funcional**: Se reemplaza el panel temporal/pendiente por una sección de ventas interactiva.
2. **Modelo `Venta` (`modelos/venta.py`)**: Nueva entidad encargada de representar la relación entre un usuario (comprador), un producto, la fecha/hora de la transacción y el monto total.
3. **Persistencia en `ventas.json`**: Se incorpora `datos/ventas.json` para almacenar el historial de ventas mediante `ArchivoServicio`.
4. **Manejo de Eventos con `command=`**: El botón **"Registrar venta"** utiliza `command=self._on_registrar_venta` para enlazar el callback de la vista.
5. **Recursos Visuales Obligatorios (`assets/`)**: Integración de íconos y logo del sistema (`logo.png`, `app_icon.png`, `icon_producto.png`, `icon_usuario.png`, `icon_venta.png`) en el encabezado, menú de navegación, ventana principal y pantallas.
6. **Actualización Reactiva de la UI**: Al registrar una venta, la vista refresca inmediatamente la tabla `Treeview`, las tarjetas de métricas recaudadas y descuenta automáticamente el stock del producto en `productos.json`.

---

## ⚡ Fundamento de Eventos (Flujo de Ejecución)

La arquitectura respeta estrictamente el principio de separación de responsabilidades y el flujo de control por eventos:

```
[ USUARIO ] 
     │  (Realiza un clic en el botón "Registrar venta")
     ▼
[ BOTÓN / COMPONENTE ]
     │  (Configurado con command=self._on_registrar_venta)
     ▼
[ CALLBACK EN LA VISTA ]
     │  (Obtiene selecciones de los Comboboxes en MainView)
     ▼
[ RESTAURANTE SERVICIO ]
     │  (Valida existencia de usuario, producto y stock disponible)
     ▼
[ PERSISTENCIA ]
     │  (Guarda en ventas.json y actualiza stock en productos.json)
     ▼
[ RESPUESTA EN LA INTERFAZ ]
        (Actualiza Treeview de ventas, métricas y muestra feedback visual)
```

> **Importante:** El callback no manipula directamente los archivos JSON ni contiene la lógica del restaurante; únicamente recopila la selección de la interfaz, coordina la solicitud con `RestauranteServicio` y actualiza la vista.

---

## 🏗️ Estructura del Proyecto

```
PARCIAL 2/SEMANA 15/restaurante_app/
├── datos/
│   ├── productos.json       # Persistencia física de productos e inventario
│   ├── usuarios.json        # Persistencia física de usuarios y credenciales
│   └── ventas.json          # Persistencia física del historial de ventas
├── modelos/
│   ├── __init__.py          # Exportación de paquetes del módulo de modelos
│   ├── producto.py          # Clase Producto (SRP, encapsulamiento, JSON to/from dict)
│   ├── usuario.py           # Clase Usuario (SRP, encapsulamiento, JSON to/from dict)
│   └── venta.py             # Clase Venta (SRP, relación usuario-producto, validaciones)
├── servicios/
│   ├── __init__.py          # Exportación de paquetes del módulo de servicios
│   ├── archivo_servicio.py  # Persistencia I/O y captura de excepciones JSON
│   └── restaurante_servicio.py # Lógica de negocio (validaciones, CRUD y ventas)
├── ui/
│   ├── __init__.py          # Exportación de componentes de la interfaz
│   ├── login_view.py        # Pantalla de Login estilizada con logo de assets/
│   └── main_view.py         # Dashboard con pestañas de Ventas, Productos y Usuarios
├── assets/                  # Recursos visuales obligatorios (Logo e Íconos PNG)
│   ├── logo.png
│   ├── app_icon.png
│   ├── icon_producto.png
│   ├── icon_usuario.png
│   └── icon_venta.png
├── main.py                  # Punto de entrada principal y control de ventana Tkinter
└── README.md                # Documentación detallada del proyecto
```

---

## 🚀 Instrucciones para Ejecutar la Aplicación

### Requisitos Previos
- Python 3.8 o superior instalado.
- Soporte para Tkinter (incluido por defecto en la instalación estándar de Python).

### Pasos de Ejecución

1. Abra una terminal o línea de comandos.
2. Navegue al directorio del proyecto:
   ```bash
   cd "PARCIAL 2/SEMANA 15/restaurante_app"
   ```
3. Ejecute el archivo principal:
   ```bash
   python main.py
   ```

### 🔐 Credenciales de Inicio de Sesión de Prueba
- **Usuario / Cédula:** `0102030405`
- **Contraseña:** `1234` *(o cualquier texto no vacío)*
- *(También puede probar con el usuario `0987654321` o `admin`)*

---

## 🧪 Comprobación de Funcionamiento

1. **Inicio y Login**: Al ejecutar `main.py`, se abre la interfaz con el logo del restaurante y el ícono de ventana desde `assets/`.
2. **Navegación**: Puede alternar entre las secciones de **Ventas**, **Productos** y **Usuarios** mediante el menú lateral.
3. **Módulo de Ventas**:
   - Seleccione un usuario registrado del desplegable (ej. `0102030405 — Jasmin Ramirez`).
   - Seleccione un producto registrado del desplegable (ej. `P001 — Hamburguesa Especial ($8.50)`).
   - Haga clic en **"Registrar Venta"** (asociado a `command=`).
   - Se muestra una alerta informativa y un mensaje visual verde confirmando el registro.
   - La tabla de historial de ventas muestra inmediatamente la nueva transacción con su código secuencial (ej. `V003`), fecha actual y total.
   - En la sección **Productos**, el stock del producto seleccionado se reduce automáticamente en 1 unidad.
4. **Persistencia**: Al cerrar y volver a abrir la aplicación, todas las ventas registradas permanecen almacenadas en `datos/ventas.json`.

---

## ⚖️ Licencia y Responsabilidad
Desarrollado para la asignatura **Programación Orientada a Objetos**. Respetando las normas académicas, no se incluyeron términos ajenos al dominio del restaurante (sin referencias a bibliotecas o libros).
