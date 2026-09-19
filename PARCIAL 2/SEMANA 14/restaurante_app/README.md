# restaurante_app — Semana 14: Componentes y Contenedores en Tkinter

**Estudiante:** Jasmin Ramirez  
**Asignatura:** Programación Orientada a Objetos (POO) — 2do. Semestre  
**Parcial:** 2 | **Semana:** 14  
**Tema Central:** Componentes y contenedores en Tkinter / ttk (CRUD Completo de Productos y Usuarios)

---

## 📋 Propósito de la Semana 14

En la **Semana 14**, el proyecto `restaurante_app` evoluciona desde la base gráfica inicial construida en la Semana 13 hacia una interfaz de usuario significativamente más clara, organizada y funcional mediante el uso avanzado de **componentes y contenedores** de Tkinter y ttk.

El objetivo central es permitir la gestión completa (**Registrar, Consultar/Cargar, Actualizar y Eliminar**) tanto para los **Productos del restaurante** como para los **Usuarios del sistema**, utilizando formularios dedicados en contenedores `ttk.LabelFrame` y botones de acción (`command=`), manteniendo la arquitectura modular por capas (SRP) y la persistencia física en archivos JSON (`productos.json` y `usuarios.json`).

---

## 🏗️ Estructura del Proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

### Separación de Responsabilidades:
- **`modelos/`**: Clases `Producto` y `Usuario` con encapsulamiento, getters/setters con validación de dominio y serialización JSON (`to_dict` / `from_dict`).
- **`servicios/`**:
  - `ArchivoServicio`: Persistencia física I/O (`json.load` y `json.dump`) manejando excepciones de archivo.
  - `RestauranteServicio`: Lógica de negocio, validaciones y operaciones CRUD completas para Productos y Usuarios.
- **`ui/`**:
  - `LoginView`: Pantalla de autenticación inicial.
  - `MainView`: Dashboard del restaurante compuesto por contenedores y componentes organizados con gestores de geometría (`grid` y `pack`).
- **`main.py`**: Instancia la ventana raíz única (`tk.Tk()`), inyecta dependencias y controla la navegación entre vistas.

---

## 🎨 Componentes y Contenedores Utilizados

| Tipo | Elemento | Uso en la Aplicación |
| :--- | :--- | :--- |
| **Contenedor** | `tk.Frame` | Tarjetas de resumen, cabecera superior, barra lateral y contenedores de botones de acción. |
| **Contenedor** | `ttk.LabelFrame` | Agrupación visual del **Formulario de Producto**, **Inventario de Productos**, **Formulario de Usuario** y **Lista de Usuarios**. |
| **Componente** | `ttk.Entry` | Entradas de texto para Código, Nombre, Precio, Identificación y Correo. |
| **Componente** | `ttk.Combobox` | Selección desplegable de categorías de productos (*Plato Fuerte, Bebida, Postre, Entrada, Acompañamiento*). |
| **Componente** | `ttk.Spinbox` | Captura y control numérico de unidades en Stock. |
| **Componente** | `tk.Button` | Botones de acción (`command=`) para **Registrar**, **Consultar**, **Actualizar**, **Eliminar** y **Limpiar** en ambos módulos. |
| **Componente** | `ttk.Treeview` | Tablas de visualización interactiva para productos y usuarios con Scrollbar vertical. |
| **Componente** | `tk.Label` | Títulos, tarjetas de métricas y banners de retroalimentación de operaciones (éxito/error). |

---

## ⚡ Operaciones Implementadas (CRUD en Productos y Usuarios)

Todas las operaciones se invocan desde los botones con controladores `command=` y se procesan en `RestauranteServicio`:

### 📦 Módulo de Productos:
1. **➕ Registrar**: Inserta un nuevo producto con validación de código único y positivo.
2. **🔍 Consultar / Cargar**: Carga los datos de un producto en el formulario desde su código o clic en la tabla.
3. **✏️ Actualizar**: Modifica nombre, categoría, precio o stock conservando los cambios en `productos.json`.
4. **🗑️ Eliminar**: Elimina el producto previa confirmación y actualiza `productos.json`.
5. **🧹 Limpiar Campos**: Blanquea las entradas del formulario.

### 👥 Módulo de Usuarios:
1. **➕ Registrar**: Inserta un nuevo usuario validando identificación única y formato de correo.
2. **🔍 Consultar / Cargar**: Carga los datos del usuario según la cédula o clic en la tabla.
3. **✏️ Actualizar**: Modifica el nombre o correo del usuario conservando los cambios en `usuarios.json`.
4. **🗑️ Eliminar**: Elimina el usuario previa confirmación y actualiza `usuarios.json`.
5. **🧹 Limpiar Campos**: Blanquea las entradas del formulario de usuario.

---

## 💾 Persistencia en Archivos JSON

La persistencia de datos es **transparente y automática**:
- Toda modificación exitosa sobre productos o usuarios provoca el guardado inmediato en `datos/productos.json` y `datos/usuarios.json`.
- Al reiniciar la aplicación, los datos guardados en JSON se cargan y reconstruyen automáticamente.
- **Regla de Arquitectura:** Las vistas (`ui/`) NUNCA leen ni escriben directamente los archivos JSON; todas las peticiones se delegan a `RestauranteServicio`.

---

## 🔑 Credenciales de Prueba (Inicio de Sesión)

Para acceder al sistema desde la pantalla de `LoginView`:

| Usuario / Cédula | Contraseña | Nombre | Rol |
| :--- | :--- | :--- | :--- |
| `0102030405` | `1234` | Jasmin Ramirez | Usuario Registrado |
| `0987654321` | `1234` | Carlos Mendoza | Cliente Frecuente |
| `admin` | `admin` | Administrador | Administrador del Sistema |

---

## 🚀 Pasos para Ejecutar la Aplicación

### Prerrequisitos
- Python 3.8 o superior.
- Módulo `tkinter` habilitado (estándar en Python para Windows/macOS).

### Ejecución
1. Abra una terminal en el directorio del proyecto (`PARCIAL 2/SEMANA 14/restaurante_app`).
2. Ejecute el punto de entrada principal:

```bash
python main.py
```

---

## ✅ Comprobación Mínima de Funcionamiento Realizada

- [x] **Inicio sin Errores**: `main.py` arranca la ventana Tkinter única de forma centrada.
- [x] **Acceso por Login**: La validación de credenciales en `LoginView` se delega a `RestauranteServicio`.
- [x] **CRUD de Productos**: Formulario con componentes y contenedores, botones de acción (`command=`) y persistencia en `productos.json`.
- [x] **CRUD de Usuarios**: Formulario con componentes y contenedores, botones de acción (`command=`) y persistencia en `usuarios.json`.
- [x] **Persistencia entre Reinicios**: Los datos modificados se conservan al cerrar y reabrir la aplicación.
- [x] **Separación de Responsabilidades**: Las vistas no manipulan JSON ni contienen reglas de negocio.
