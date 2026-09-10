# restaurante_app — Semana 13: Conceptos fundamentales de interfaces gráficas de usuario con Tkinter

**Estudiante:** Jasmin Ramirez  
**Asignatura:** Programación Orientada a Objetos (POO) — 2do. Semestre  
**Parcial:** 2 | **Semana:** 13  

---

## 📋 Descripción General del Sistema

El sistema `restaurante_app` evoluciona en la **Semana 13** iniciando la transición desde una aplicación basada en consola hacia una **Interfaz Gráfica de Usuario (GUI)** construida con el framework estándar **Tkinter** en Python.

Siguiendo el diseño arquitectónico del proyecto docente (**Biblioteca App**), la solución se organiza en una arquitectura limpia por capas que desacopla la presentación visual, la lógica del negocio y la persistencia de datos:

1. **Capa de Modelos (`modelos/`)**: Representa las entidades `Producto` y `Usuario` con encapsulamiento, getters/setters con validación y conversión bidireccional JSON (`to_dict()` y `from_dict()`).
2. **Capa de Servicios (`servicios/`)**:
   - `ArchivoServicio`: Encargado de la persistencia I/O sobre archivos JSON (`productos.json` y `usuarios.json`), manejando excepciones de archivo y formato.
   - `RestauranteServicio`: Encapsula la lógica de negocio, la validación de acceso simulada, y la entrega de productos, usuarios y métricas generales a la interfaz visual.
3. **Capa de Interfaz Gráfica (`ui/`)**:
   - `LoginView`: Pantalla de acceso simulada con entradas de usuario/contraseña y mensajes visuales de retroalimentación en caso de campos vacíos o credenciales erróneas.
   - `MainView`: Panel principal del restaurante con navegación entre **Productos Registrados**, **Usuarios Registrados** y **Ventas (Pendiente)**, desplegando tablas interactivas mediante `ttk.Treeview`.
4. **Punto de Entrada (`main.py`)**: Prepara la única ventana `tk.Tk()`, inyecta las dependencias a las vistas y controla el ciclo de vida y la navegación suave entre Login y la Interfaz Principal sin abrir múltiples ventanas.

---

## 📁 Estructura del Proyecto

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

---

## 🔄 Flujo de Ejecución de la Aplicación

```text
       Inicio de la Aplicación (main.py)
                      │
                      ▼
     Instanciación de ArchivoServicio 
           y RestauranteServicio
                      │
                      ▼
      Despliegue de Ventana Única (Tk)
                      │
                      ▼
                 LoginView
        ┌─────────────┴─────────────┐
        │ Campones vacíos / Error   │ ➔ Muestra alerta visual (roja)
        └─────────────┬─────────────┘
                      │ Credenciales Válidas
                      ▼
        RestauranteServicio.validar_acceso()
                      │
                      ▼
                  MainView
   ├── 📦 Productos Registrados (Treeview)
   ├── 👥 Usuarios Registrados  (Treeview)
   └── 🛒 Ventas (Pendiente)
                      │
                      ▼
            Botón "Cerrar Sesión"
                      │
                      ▼
             Retorno a LoginView
```

---

## 🔑 Credenciales de Prueba (Simulación de Acceso)

Para verificar el funcionamiento del inicio de sesión en la interfaz gráfica, se pueden utilizar cualquiera de los siguientes usuarios registrados en `usuarios.json`:

| Usuario / Cédula / Correo | Contraseña | Nombre Completo | Rol / Descripción |
| :--- | :--- | :--- | :--- |
| `0102030405` | `1234` (o cualquier clave) | Jasmin Ramirez | Usuario Registrado |
| `0987654321` | `1234` (o cualquier clave) | Carlos Mendoza | Cliente Frecuente |
| `admin` | `admin` | Administrador del Restaurante | Administrador del Sistema |

---

## 🚀 Instrucciones de Ejecución

### Prerrequisitos
- Python 3.8 o superior instalado.
- Módulo `tkinter` habilitado (incluido por defecto en instalaciones de Python en Windows/macOS).

### Pasos para Ejecutar
1. Abra una terminal en la carpeta raíz del proyecto (`PARCIAL 2/SEMANA 13/restaurante_app`).
2. Ejecute la aplicación con el siguiente comando:

```bash
python main.py
```

O desde la carpeta `SEMANA 13`:

```bash
python -m restaurante_app.main
```

---

## ✅ Comprobación Mínima de Funcionamiento Realizada

- [x] **Ventana Única**: La aplicación se ejecuta dentro de un único ciclo de vida `mainloop()` y una única instancia de `tk.Tk()`.
- [x] **Login Visual**: La pantalla de login valida que los campos no estén vacíos y muestra avisos visuales en rojo si los datos son incorrectos.
- [x] **Autenticación en Servicio**: La validación de credenciales se realiza a través de `RestauranteServicio.validar_acceso(...)`.
- [x] **Dashboard MainView**: Al acceder con credenciales válidas, se despliega el panel principal con saludo personalizado al usuario.
- [x] **Consulta de Productos**: Muestra la lista de productos (`Código`, `Nombre`, `Categoría`, `Precio`, `Stock`) leída mediante `RestauranteServicio` desde `productos.json`.
- [x] **Consulta de Usuarios**: Muestra la lista de usuarios leída mediante `RestauranteServicio` desde `usuarios.json`.
- [x] **Sección Pendiente**: Muestra la opción de Ventas claramente identificada como pendiente para semanas futuras.
- [x] **Cerrar Sesión**: El botón "Cerrar Sesión" retorna a la pantalla de login dentro de la misma ventana Tkinter.
