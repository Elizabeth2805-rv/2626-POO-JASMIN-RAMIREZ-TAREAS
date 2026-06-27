class Cliente:
    def __init__(self, cedula_identidad: str, nombre_completo: str, edad_cliente: int, tiene_membresia: bool):
        """Constructor para registrar los datos informativos de un cliente."""
        self.cedula_identidad: str = cedula_identidad
        self.nombre_completo: str = nombre_completo
        self.edad_cliente: int = edad_cliente
        self.tiene_membresia: bool = tiene_membresia

    def __str__(self) -> str:
        """Devuelve la información del cliente estructurada como texto."""
        tipo_cliente: str = "Cliente VIP" if self.tiene_membresia else "Cliente Regular"
        return f"ID: {self.cedula_identidad} | Nombre: {self.nombre_completo} | Edad: {self.edad_cliente} años | Tipo: {tipo_cliente}"