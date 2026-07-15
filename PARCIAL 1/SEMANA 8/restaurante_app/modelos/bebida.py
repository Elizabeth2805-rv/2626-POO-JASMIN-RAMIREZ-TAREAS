# -*- coding: utf-8 -*-
# modelos/bebida.py
# Principio OCP: Bebida extiende el sistema sin modificar la clase Producto
#               ni la lógica general del servicio Restaurante.
# Principio LSP: Bebida puede sustituir a Producto en cualquier contexto
#               donde se espere un Producto, sin romper el comportamiento.

from modelos.producto import Producto


class Bebida(Producto):
    """
    Clase que representa una Bebida del restaurante.

    Hereda de Producto porque una bebida ES un tipo de producto.
    Amplía la información disponible con atributos específicos:
    tamaño y tipo de envase.

    Principio OCP aplicado: el sistema acepta Bebida en la misma
    colección de productos sin que la clase Restaurante ni la clase
    Producto necesiten ser modificadas.

    Principio LSP aplicado: cualquier método que reciba un Producto
    funciona correctamente con una instancia de Bebida.
    """

    TAMANOS_VALIDOS: tuple = ("pequeño", "mediano", "grande", "xl")
    ENVASES_VALIDOS: tuple = ("vaso", "botella", "lata", "jarra", "tetra")

    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        tamano: str,
        tipo_envase: str,
    ) -> None:
        """
        Constructor de la clase Bebida.

        Invoca el constructor padre (Producto) para reutilizar la lógica
        de validación ya establecida, y agrega sus propios atributos.

        Args:
            codigo:      Código único de la bebida (e.g., 'B001').
            nombre:      Nombre de la bebida (e.g., 'Limonada Imperial').
            categoria:   Categoría (e.g., 'Bebidas').
            precio:      Precio unitario. Debe ser mayor que cero.
            tamano:      Tamaño de la porción: pequeño, mediano, grande, xl.
            tipo_envase: Tipo de envase: vaso, botella, lata, jarra, tetra.
        """
        # Llamada al constructor de la clase padre para inicializar
        # los atributos comunes con sus validaciones
        super().__init__(codigo=codigo, nombre=nombre, categoria=categoria, precio=precio)

        # Atributos específicos de Bebida
        self.tamano = tamano
        self.tipo_envase = tipo_envase

    # ------------------------------------------------------------------ #
    #  Getter / Setter: tamano                                             #
    # ------------------------------------------------------------------ #
    @property
    def tamano(self) -> str:
        """Retorna el tamaño de la bebida."""
        return self._tamano

    @tamano.setter
    def tamano(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El tamaño de la bebida no puede estar vacío.")
        valor_normalizado = valor.strip().lower()
        if valor_normalizado not in self.TAMANOS_VALIDOS:
            validos = ", ".join(self.TAMANOS_VALIDOS)
            raise ValueError(
                f"Tamaño '{valor}' no válido. Opciones permitidas: {validos}."
            )
        self._tamano = valor_normalizado

    # ------------------------------------------------------------------ #
    #  Getter / Setter: tipo_envase                                        #
    # ------------------------------------------------------------------ #
    @property
    def tipo_envase(self) -> str:
        """Retorna el tipo de envase de la bebida."""
        return self._tipo_envase

    @tipo_envase.setter
    def tipo_envase(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El tipo de envase no puede estar vacío.")
        valor_normalizado = valor.strip().lower()
        if valor_normalizado not in self.ENVASES_VALIDOS:
            validos = ", ".join(self.ENVASES_VALIDOS)
            raise ValueError(
                f"Envase '{valor}' no válido. Opciones permitidas: {validos}."
            )
        self._tipo_envase = valor_normalizado

    # ------------------------------------------------------------------ #
    #  Sobrescritura: mostrar_informacion                                  #
    # ------------------------------------------------------------------ #
    def mostrar_informacion(self) -> None:
        """
        Muestra los datos de la bebida en consola, extendiendo el formato
        base de Producto con los atributos específicos de la bebida.

        Principio LSP: Este método sustituye al de Producto de forma
        coherente. El servicio Restaurante llama a mostrar_informacion()
        sobre cualquier objeto de la lista de productos y cada uno
        responde según su propia implementación, sin condicionales
        del tipo 'if isinstance(obj, Bebida)'.
        """
        print(f"  [Bebida]   Código   : {self.codigo}")
        print(f"             Nombre   : {self.nombre}")
        print(f"             Categoría: {self.categoria}")
        print(f"             Precio   : ${self.precio:.2f}")
        print(f"             Tamaño   : {self.tamano.capitalize()}")
        print(f"             Envase   : {self.tipo_envase.capitalize()}")
        print("  " + "-" * 42)
