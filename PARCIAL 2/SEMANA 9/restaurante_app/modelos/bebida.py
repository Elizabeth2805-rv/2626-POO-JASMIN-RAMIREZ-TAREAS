# -*- coding: utf-8 -*-
# modelos/bebida.py
# Clonado desde PARCIAL 1 / SEMANA 8 — Semana 9 agrega persistencia JSON.
#
# Principio OCP: Bebida extiende el sistema sin modificar Producto ni Restaurante.
# Principio LSP: Bebida puede sustituir a Producto en cualquier contexto.

from modelos.producto import Producto


class Bebida(Producto):
    """
    Clase que representa una Bebida del restaurante.

    Hereda de Producto porque una bebida ES un tipo de producto.
    Extiende la información disponible con atributos específicos:
    tamaño y tipo de envase.

    Incorpora sobrescritura de to_dict() para incluir sus atributos
    propios en la serialización JSON, y from_dict() para reconstruirse
    correctamente desde un diccionario.
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

        Args:
            codigo:      Código único de la bebida (e.g., 'B001').
            nombre:      Nombre de la bebida (e.g., 'Limonada Imperial').
            categoria:   Categoría (e.g., 'Bebidas').
            precio:      Precio unitario. Debe ser mayor que cero.
            tamano:      Tamaño de la porción: pequeño, mediano, grande, xl.
            tipo_envase: Tipo de envase: vaso, botella, lata, jarra, tetra.
        """
        super().__init__(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio=precio,
        )
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
                f"Tamaño '{valor}' no válido. Opciones: {validos}."
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
                f"Envase '{valor}' no válido. Opciones: {validos}."
            )
        self._tipo_envase = valor_normalizado

    # ------------------------------------------------------------------ #
    #  Serialización / Deserialización JSON                                #
    # ------------------------------------------------------------------ #
    def to_dict(self) -> dict:
        """
        Convierte la Bebida a un diccionario serializable en JSON.

        Sobrescribe el método de Producto para incluir los atributos
        específicos de Bebida (tamano, tipo_envase).
        La clave 'tipo' = 'Bebida' permite que el gestor JSON la
        reconstruya como instancia de la clase correcta.

        Returns:
            dict con todos los atributos de la bebida.
        """
        datos = super().to_dict()          # Reutiliza el dict base de Producto
        datos["tipo"] = "Bebida"           # Sobreescribe el tipo para distinguirla
        datos["tamano"] = self.tamano
        datos["tipo_envase"] = self.tipo_envase
        return datos

    @classmethod
    def from_dict(cls, datos: dict) -> "Bebida":
        """
        Crea una instancia de Bebida a partir de un diccionario.

        Args:
            datos: Diccionario con las claves de Producto más
                   'tamano' y 'tipo_envase'.

        Returns:
            Nueva instancia de Bebida reconstruida desde el diccionario.
        """
        return cls(
            codigo=datos["codigo"],
            nombre=datos["nombre"],
            categoria=datos["categoria"],
            precio=datos["precio"],
            tamano=datos["tamano"],
            tipo_envase=datos["tipo_envase"],
        )

    # ------------------------------------------------------------------ #
    #  Sobrescritura: mostrar_informacion                                  #
    # ------------------------------------------------------------------ #
    def mostrar_informacion(self) -> None:
        """
        Muestra los datos de la bebida en consola, extendiendo el formato
        base de Producto con los atributos específicos de la bebida.
        """
        print(f"  [Bebida]   Código   : {self.codigo}")
        print(f"             Nombre   : {self.nombre}")
        print(f"             Categoría: {self.categoria}")
        print(f"             Precio   : ${self.precio:.2f}")
        print(f"             Tamaño   : {self.tamano.capitalize()}")
        print(f"             Envase   : {self.tipo_envase.capitalize()}")
        print("  " + "-" * 44)
