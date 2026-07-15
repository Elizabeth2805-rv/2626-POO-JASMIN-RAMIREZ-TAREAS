# -*- coding: utf-8 -*-
# modelos/producto.py
# Principio SRP: Esta clase es exclusivamente responsable de representar
# la información y el comportamiento de un producto del restaurante.

class Producto:
    """
    Clase base que representa un Producto general del restaurante.

    Aplica el principio de Responsabilidad Única (SRP): su única
    responsabilidad es contener y exponer la información de un producto.

    Aplica el principio Abierto/Cerrado (OCP): está abierta para ser
    extendida mediante herencia (e.g., Bebida), pero no necesita
    modificarse cuando se añaden nuevos tipos de producto.
    """

    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float) -> None:
        """
        Constructor de la clase Producto.

        Args:
            codigo:    Identificador único del producto (e.g., 'P001').
            nombre:    Nombre descriptivo del producto.
            categoria: Categoría a la que pertenece (e.g., 'Plato Fuerte').
            precio:    Precio unitario en dólares. Debe ser mayor que cero.
        """
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio

    # ------------------------------------------------------------------ #
    #  Getter / Setter: codigo                                             #
    # ------------------------------------------------------------------ #
    @property
    def codigo(self) -> str:
        """Retorna el código identificador del producto."""
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        self._codigo = valor.strip().upper()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: nombre                                             #
    # ------------------------------------------------------------------ #
    @property
    def nombre(self) -> str:
        """Retorna el nombre del producto."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: categoria                                          #
    # ------------------------------------------------------------------ #
    @property
    def categoria(self) -> str:
        """Retorna la categoría del producto."""
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        self._categoria = valor.strip()

    # ------------------------------------------------------------------ #
    #  Getter / Setter: precio                                             #
    # ------------------------------------------------------------------ #
    @property
    def precio(self) -> float:
        """Retorna el precio del producto."""
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        try:
            valor_num = float(valor)
        except (ValueError, TypeError):
            raise ValueError("El precio debe ser un valor numérico válido.")
        if valor_num <= 0:
            raise ValueError("El precio del producto debe ser mayor que cero.")
        self._precio = valor_num

    # ------------------------------------------------------------------ #
    #  Método común: mostrar_informacion                                   #
    # ------------------------------------------------------------------ #
    def mostrar_informacion(self) -> None:
        """
        Muestra los datos del producto en consola con formato legible.

        Principio LSP: Bebida sobrescribirá este método para ampliar
        la información mostrada. El servicio Restaurante siempre
        invocará mostrar_informacion() sin preguntar qué tipo concreto
        de objeto está procesando.
        """
        print(f"  [Producto] Código   : {self.codigo}")
        print(f"             Nombre   : {self.nombre}")
        print(f"             Categoría: {self.categoria}")
        print(f"             Precio   : ${self.precio:.2f}")
        print("  " + "-" * 42)
