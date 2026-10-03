# 🍽️ Restaurante App — Semana 16: Manejo de Eventos en Tkinter (Gestión de Usuarios)

**Asignatura:** Programación Orientada a Objetos (POO)  
**Semestre:** 2do Semestre  
**Estudiante:** Jasmin Ramirez  
**Proyecto:** `restaurante_app`  
**Semana:** 16 — Manejo de eventos en Tkinter  

---

## 📋 1. Propósito de la Semana 16

La actividad de la **Semana 16** aborda el **Manejo de Eventos en Tkinter** mediante la evolución del sistema interactivo `restaurante_app`. El objetivo principal es aplicar mecanismos de respuesta a interacciones del usuario (como selecciones en tablas, atajos de teclado y opciones de listas desplegables) utilizando el patrón **interacción → evento → bind() → callback → servicio → persistencia → respuesta visual**.

En esta entrega, la sección de **Gestión de Usuarios** fue expandida para incorporar la administración completa de usuarios (registro, consulta, actualización y eliminación), soporte para el atributo **`rol`** (`Administrador`, `Empleado`, `Cliente`), control de acceso diferenciado y la asociación de eventos específicos en Tkinter (`<<TreeviewSelect>>`, `<Return>`, `<Escape>`, `<<ComboboxSelected>>`).

---

## 🚀 2. Evolución del Proyecto (Continuidad desde Semana 15)

El proyecto mantiene intactas la arquitectura modular y las funcionalidades previamente implementadas:

1. **Continuidad Operativa**:
   - Inicio de Sesión (`LoginView`) con recursos visuales de `assets/`.
   - Menú de navegación lateral dinámico (`Sidebar`).
   - Módulo de **Gestión de Productos** con inventario y stock en tiempo real.
   - Módulo de **Registro de Ventas** vinculando usuarios y productos con descuento automático de stock.

2. **Novedades de la Semana 16**:
   - **Atributo `rol` en `Usuario`**: Permite clasificar cada cuenta en `Administrador`, `Empleado` o `Cliente`.
   - **Formulario y Tabla de Usuarios**: Visualización ordenada en un `ttk.Treeview` con columnas (ID, Nombre, Correo, Rol).
   - **Carga Automática mediante `<<TreeviewSelect>>`**: Al hacer clic en una fila de la tabla, los datos se recuperan desde `RestauranteServicio` y se cargan automáticamente en el formulario.
   - **Atajos de Teclado**:
     - `<Return>`: Confirma el registro del usuario desde el formulario.
     - `<Escape>`: Limpia todos los campos del formulario, deselecciona las filas en el Treeview y restablece el estado inicial.
   - **Evento Virtual `<<ComboboxSelected>>`**: Reacciona inmediatamente cuando se cambia el rol en la lista desplegable.
   - **Control de Acceso**: Únicamente los usuarios con rol `Administrador` tienen habilitados los botones de modificación (Registrar, Actualizar, Eliminar). Para roles `Empleado` y `Cliente`, las acciones de escritura permanecen deshabilitadas con avisos descriptivos.
   - **Protección contra Auto-eliminación**: El sistema impide que un Administrador elimine accidentalmente su propia cuenta mientras se encuentra autenticado en la sesión activa.

---

## 📂 3. Estructura Modular del Proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json        # Datos persistentes de productos
│   ├── usuarios.json         # Datos persistentes de usuarios con el atributo 'rol'
│   └── ventas.json           # Datos persistentes de ventas registradas
├── modelos/
│   ├── __init__.py
│   ├── producto.py           # Entidad Producto (código, nombre, categoría, precio, stock)
│   ├── usuario.py            # Entidad Usuario (identificación, nombre, correo, rol)
│   └── venta.py              # Entidad Venta (relación usuario - producto)
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py   # Persistencia física I/O en formato JSON
│   └── restaurante_servicio.py # Reglas de negocio y operaciones CRUD
├── ui/
│   ├── __init__.py
│   ├── login_view.py         # Pantalla de Login con autenticación y logo de assets/
│   └── main_view.py          # Dashboard principal con gestión de eventos en Usuarios, Productos y Ventas
├── assets/                   # Recursos visuales obligatorios
│   ├── app_icon.png          # Ícono principal de la ventana Tkinter
│   ├── icon_producto.png     # Ícono para el menú de Productos
│   ├── icon_usuario.png      # Ícono para el menú de Usuarios
│   ├── icon_venta.png        # Ícono para el menú de Ventas
│   └── logo.png              # Logo del restaurante
├── main.py                   # Punto de entrada de la aplicación
└── README.md                 # Documentación del proyecto
```

---

## 👥 4. Gestión de Usuarios y Roles

La entidad `Usuario` integra el atributo `rol`, que regula la interacción en la interfaz:

- **Administrador**: Posee acceso completo a la gestión administrativa de usuarios (Registrar, Consultar, Actualizar y Eliminar).
- **Empleado**: Puede acceder al sistema, realizar consultas y operar la registrar ventas y productos, pero tiene restringida la modificación administrativa de usuarios.
- **Cliente**: Usuario final registrado en el sistema que puede ser seleccionado como comprador en el módulo de ventas.

### Modelo de Datos JSON (`usuarios.json`)
```json
[
    {
        "identificacion": "0102030405",
        "nombre": "Jasmin Ramirez",
        "correo": "jasmin.ramirez@estudiante.edu.ec",
        "rol": "Administrador"
    },
    {
        "identificacion": "0987654321",
        "nombre": "Carlos Mendoza",
        "correo": "carlos.mendoza@email.com",
        "rol": "Empleado"
    },
    {
        "identificacion": "0995891298",
        "nombre": "Junior Loyola",
        "correo": "junior23@gmail.com",
        "rol": "Cliente"
    }
]
```

---

## ⚡ 5. Eventos Implementados: `bind()` vs `command=`

Tkinter ofrece dos mecanismos principales para gestionar la interacción del usuario:

| Mecanismo | Descripción | Uso en `restaurante_app` |
| :--- | :--- | :--- |
| **`command=`** | Parámetro nativo de widgets como `Button`. Asocia un *callback* directo al evento de clic. | Botones principales del formulario: `Registrar`, `Consultar`, `Actualizar`, `Eliminar` y `Limpiar`. |
| **`bind()`** | Método flexible de Tkinter para vincular eventos de teclado (`<Return>`, `<Escape>`) o eventos virtuales de `ttk` (`<<TreeviewSelect>>`, `<<ComboboxSelected>>`). | Atajos de teclado, selección en la tabla Treeview y cambio de opción en el Combobox de rol. |

### Eventos Específicos Evidenciados:

1. **`<<TreeviewSelect>>`**:
   ```python
   self.tree_usuarios.bind("<<TreeviewSelect>>", self._on_tree_select_usuario)
   ```
   *Flujo:* El usuario selecciona una fila ➔ `_on_tree_select_usuario` obtiene la cédula/ID ➔ Consulta la entidad completa mediante `RestauranteServicio.buscar_usuario(identificacion)` ➔ Carga los datos en el formulario sin exponer contraseñas en la tabla.

2. **`<Return>`**:
   ```python
   widget.bind("<Return>", lambda e: self._on_registrar_usuario())
   ```
   *Flujo:* El usuario presiona Enter dentro de los campos ➔ Reutiliza directamente el método de registro `_on_registrar_usuario()` sin duplicar lógica de negocio.

3. **`<Escape>`**:
   ```python
   widget.bind("<Escape>", lambda e: self._limpiar_formulario_usuario())
   ```
   *Flujo:* El usuario presiona la tecla Escape ➔ Se limpian los campos de entrada, se restablece el Combobox al rol `Cliente` y se remueve la selección activa del Treeview.

4. **`<<ComboboxSelected>>`**:
   ```python
   self.cmb_usr_rol.bind("<<ComboboxSelected>>", self._on_combobox_rol_selected)
   ```
   *Flujo:* El usuario cambia la selección del rol ➔ Se activa la respuesta visual en la barra de estado e información del formulario.

---

## 🔒 6. Separación de Responsabilidades y Persistencia

- **Vistas (`ui/`)**: Solamente capturan eventos, muestran componentes gráficos y comunican retroalimentación al usuario. No leen ni escriben archivos JSON directamente.
- **Servicios (`servicios/`)**: Contienen las validaciones de negocio (comprobar duplicados, existencia de objetos, persistencia física).
- **Modelos (`modelos/`)**: Representan las entidades puras con sus getter/setters y conversión `to_dict()` / `from_dict()`.

---

## 🛠️ 7. Instrucciones de Ejecución

1. Abrir la terminal e ingresar a la carpeta de la Semana 16:
   ```bash
   cd "PARCIAL 2/SEMANA 16/restaurante_app"
   ```

2. Ejecutar el punto de entrada principal:
   ```bash
   python main.py
   ```

3. **Credenciales de prueba**:
   - **Administrador**: `0102030405` | Clave: `1234`
   - **Empleado**: `0987654321` | Clave: `1234`
   - **Cliente**: `0995891298` | Clave: `1234`
