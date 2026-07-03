# Sistema de Administración de Restaurante (restaurante_app)

Este proyecto es una aplicación modular en Python diseñada bajo el paradigma de **Programación Orientada a Objetos (POO)**. Modela el catálogo de productos de un restaurante aplicando conceptos clave como **Herencia**, **Encapsulación** y **Polimorfismo**.

**Estudiante:** Jasmin Ramirez  
**Materia:** Programación Orientada a Objetos  
**Semestre:** 2do. Semestre  

---

## 1. Descripción del Sistema
El sistema `restaurante_app` administra los productos ofrecidos por un restaurante. Los productos se dividen en dos categorías principales: **Platillos** (comidas) y **Bebidas**. Un servicio centralizado (`Restaurante`) permite registrar estos productos y mostrar el menú completo al público, adaptando el formato de salida según el tipo de producto.

---

## 2. Estructura del Proyecto
El proyecto está estructurado de manera modular para separar las responsabilidades del dominio (modelos) y de la lógica de negocio (servicios):

```text
restaurante_app/
├── modelos/
│   ├── __init__.py         # Inicializador del paquete modelos
│   ├── producto.py         # Clase padre general 'Producto'
│   ├── platillo.py         # Clase hija 'Platillo' (hereda de Producto)
│   └── bebida.py           # Clase hija 'Bebida' (hereda de Producto)
├── servicios/
│   ├── __init__.py         # Inicializador del paquete servicios
│   └── restaurante.py      # Clase de servicio 'Restaurante'
└── main.py                 # Punto de entrada de la aplicación
```

---

## 3. Principios de Programación Orientada a Objetos Aplicados

### A. Herencia
Se implementó una jerarquía de clases donde la clase padre `Producto` abstrae las propiedades comunes y las clases hijas `Platillo` y `Bebida` extienden este comportamiento:
* **`Producto` (Clase Padre):** Define atributos compartidos como `nombre`, `__precio` (encapsulado) y `disponibilidad`.
* **`Platillo` (Clase Hija):** Hereda de `Producto` mediante `super().__init__()` y añade el atributo especializado `tiempo_preparacion` (en minutos).
* **`Bebida` (Clase Hija):** Hereda de `Producto` mediante `super().__init__()` y añade el atributo especializado `volumen_ml` (en mililitros).

### B. Encapsulación y Validación
El atributo de precio dentro de la clase `Producto` se declaró como privado (`__precio`) para protegerlo de manipulaciones externas indebidas.
* **Acceso (Getter):** Se accede al valor mediante el método `obtener_precio()`.
* **Modificación (Setter):** Se modifica utilizando el método `cambiar_precio(nuevo_precio)`.
* **Validación:** El método `cambiar_precio` verifica que el nuevo valor sea un número (entero o flotante) y estrictamente mayor que cero. Si se intenta asignar un valor menor o igual a cero, se genera un `ValueError`, protegiendo la integridad de los datos.

### C. Polimorfismo
El polimorfismo se demuestra mediante el método `mostrar_informacion()`.
* La clase padre `Producto` define una implementación base.
* Las clases `Platillo` y `Bebida` sobrescriben (`override`) este método para incorporar detalles específicos (tiempo de preparación y volumen, respectivamente) usando la llamada a `super().mostrar_informacion()`.
* Al recorrer la lista de productos en `Restaurante.mostrar_menu()`, se invoca `producto.mostrar_informacion()` y cada objeto ejecuta su comportamiento correspondiente de acuerdo con su clase en tiempo de ejecución.

---

## 4. Instrucciones de Ejecución
Para ejecutar el proyecto, asegúrese de estar en el directorio de la semana correspondiente y ejecute el archivo `main.py`:

```bash
cd "PARCIAL 1/SEMANA 6/restaurante_app"
python main.py
```

---

## 5. Reflexión sobre la Modularidad en POO con Python
La programación orientada a objetos combinada con una estructura de carpetas modular ofrece múltiples ventajas en proyectos de software:
1. **Mantenibilidad:** Separar clases en módulos (`modelos/` y `servicios/`) facilita la localización y corrección de errores sin afectar el resto del sistema.
2. **Reutilización de Código:** La herencia reduce la redundancia al permitir que las subclases aprovechen los atributos y métodos comunes de la clase padre.
3. **Escalabilidad:** Añadir nuevos tipos de productos (como *Postres* o *Combos*) requiere crear una nueva clase que herede de `Producto` sin necesidad de modificar el código existente en `Restaurante`.
4. **Legibilidad:** Cada archivo contiene una única responsabilidad clara, haciendo que el código sea comprensible para cualquier desarrollador.
