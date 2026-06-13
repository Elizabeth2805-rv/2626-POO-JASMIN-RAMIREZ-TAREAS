class Mascota:
    """Clase que representa una mascota con atributos y comportamientos."""

    def __init__(self, nombre, especie, edad):
        """
        Constructor de la clase Mascota.

        Args:
            nombre (str): Nombre de la mascota
            especie (str): Especie de la mascota
            edad (int): Edad de la mascota en años
        """
        self.nombre = nombre
        self.especie = especie
        self.edad = edad

    def mostrar_informacion(self):
        """
        Método que muestra la información completa de la mascota.
        """
        print(f"--- Información de la Mascota ---")
        print(f"Nombre: {self.nombre}")
        print(f"Especie: {self.especie}")
        print(f"Edad: {self.edad} años")
        print()

    def hacer_sonido(self):
        """
        Método que hace un sonido específico según la especie de la mascota.
        """
        sonidos = {
            "Perro": "¡Guau guau!",
            "Gato": "¡Miau miau!",
            "Pajaro": "¡Pío pío!",
            "Hamster": "¡Chic chic!",
            "Conejo": "¡Squeak squeak!"
        }

        sonido = sonidos.get(self.especie, "La mascota hace un sonido desconocido")
        print(f"{self.nombre} ({self.especie}) dice: {sonido}")
        print()

