**Explicación detallada del código — CuentaBancaria**

Este documento explica paso a paso el contenido del archivo [PARCIAL 1/TAREA SEMANA 2.py](PARCIAL 1/TAREA SEMANA 2.py#L1).

**Resumen breve:**
- **Objetivo:** Mostrar un ejemplo sencillo de Programación Orientada a Objetos (POO) en Python mediante una clase `CuentaBancaria` que modela una cuenta real.
- **Qué aprenderás:** componentes de una clase, atributos, métodos, validaciones, y el patrón `if __name__ == "__main__"`.

---

**1. Encabezado y docstring del módulo:**
- **Descripción:** Las primeras líneas son un comentario multilínea (docstring) que resume qué hace el archivo.
- **Por qué importa:** Ayuda a quien lee a entender el propósito del módulo sin leer todo el código.

**2. Importaciones:**
- En el código aparece `from typing import Optional`.
- **Nota para principiantes:** `typing` se usa para anotaciones de tipos. En este ejemplo `Optional` no se utiliza realmente; se incluyó por si se quisiera usar tipos opcionales. No afecta la ejecución si queda sin usar, pero podrías eliminarla para limpiar el código.

**3. Definición de la clase `CuentaBancaria`:**
- `class CuentaBancaria:`: declara la plantilla (tipo) que modela una cuenta del mundo real.
- **Concepto clave (POO):** una clase describe las propiedades (atributos) y comportamientos (métodos) que tendrán los objetos creados a partir de ella.

**4. Docstring de la clase y atributos:**
- Dentro de la clase hay un comentario explicando los atributos:
  - `titular` (str): nombre de la persona que posee la cuenta.
  - `numero` (str): identificador de la cuenta.
  - `saldo` (float): cuánto dinero tiene la cuenta.

**5. Método `__init__` (constructor):**
- Firma: `def __init__(self, titular: str, numero: str, saldo: float = 0.0) -> None:`
- **Qué hace:** se ejecuta al crear una instancia (objeto) `CuentaBancaria(...)` y asigna valores iniciales a `self.titular`, `self.numero` y `self.saldo`.
- **Parámetros:** `saldo` tiene un valor por defecto `0.0` — si no pasas saldo, la cuenta comienza en cero.

**6. Método `depositar(self, cantidad: float) -> None`:**
- **Función:** añade dinero a la cuenta.
- **Validaciones:** comprueba que `cantidad` sea mayor que 0; si no, lanza `ValueError`. Esto evita depositos inválidos como números negativos.

**7. Método `retirar(self, cantidad: float) -> None`:**
- **Función:** quita dinero del saldo.
- **Validaciones:** verifica `cantidad > 0` y que `cantidad <= self.saldo`. Si falla, lanza `ValueError` con un mensaje claro. Así evitamos que el saldo quede negativo.

**8. Método `transferir(self, destino: 'CuentaBancaria', cantidad: float) -> None`:**
- **Función:** mueve dinero de una cuenta a otra.
- **Comprobaciones:** primero valida que `destino` sea una instancia de `CuentaBancaria` (si no, lanza `TypeError`). Luego reutiliza `self.retirar(cantidad)` y `destino.depositar(cantidad)`, aprovechando las validaciones ya implementadas.

**9. Método `ver_saldo(self) -> float`:**
- Devuelve el saldo actual. Es un método de lectura simple que puede usarse para obtener el valor desde fuera de la clase.

**10. Método especial `__str__(self) -> str`:**
- Define cómo se muestra el objeto cuando se convierte a cadena (por ejemplo, al usar `print(cuenta)`).
- En este caso devuelve una línea con el número, titular y saldo formateado con dos decimales.

**11. Función `ejemplo_uso()`:**
- Aquí se crea código de demostración independiente de la clase para mostrar su uso:
  - Se crean dos cuentas: `cuenta_a` y `cuenta_b`.
  - Se imprimen sus estados iniciales.
  - Se hacen operaciones: depósito, retiro y transferencia.
  - Se imprime el resultado después de cada operación.

**12. Guardia `if __name__ == "__main__":`**
- **Qué hace:** garantiza que `ejemplo_uso()` solo se ejecute cuando el archivo se ejecute directamente (`python TAREA SEMANA 2.py`) y no cuando el archivo se importe desde otro módulo.

---

**Cuestiones prácticas y buenas prácticas (para seguir mejorando):**
- Manejo de errores: lanzar excepciones (`ValueError`, `TypeError`) es útil; en programas más grandes podrías capturarlas para mostrar mensajes al usuario.
- Tipado: las anotaciones (`str`, `float`, `-> None`) ayudan a documentar y a que herramientas como linters y editores detecten errores.
- Tests: más adelante puedes añadir funciones de prueba para verificar que `depositar`, `retirar` y `transferir` funcionan en casos límites.
- Limpieza: si no vas a usar `Optional`, elimina la importación.

---

**Cómo ejecutar el ejemplo en tu máquina:**
1. Abre una terminal en la carpeta `PARCIAL 1`.
2. Ejecuta:

```bash
python "TAREA SEMANA 2.py"
```

Deberías ver salida que muestra el estado inicial de las cuentas y los cambios después de cada operación.

**Ejercicios sugeridos para practicar (opcional):**
- Añadir un método `historico(self)` que guarde y muestre las operaciones realizadas.
- Implementar intereses: método `aplicar_interes(self, porcentaje)` que aumente el saldo.
- Crear una clase `Cliente` separada y asociarla a la `CuentaBancaria`.

---

Si quieres, puedo:
- Modificar el código para registrar un historial de operaciones.
- Simplificarlo aún más para explicar cada línea en detalle.
