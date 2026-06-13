def registrar_mascota():
    """
    Función para registrar los datos de una mascota.
    Solicita los datos mediante el teclado y los retorna.
    """
    print("=" * 50)
    print("SISTEMA DE REGISTRO DE MASCOTAS")
    print("=" * 50)

    nombre = input("\nIngrese nombre de su mascota: ")
    especie = input("Ingrese especie de la mascota: ")
    edad = input("Ingrese edad de la mascota: ")

    return nombre, especie, edad


def mostrar_mascota(nombre, especie, edad):
    """
    Función para mostrar la información registrada de la mascota
    de forma organizada.
    """
    print("\n" + "=" * 50)
    print("INFORMACIÓN DE LA MASCOTA REGISTRADA")
    print("=" * 50)
    print(f"Nombre:  {nombre}")
    print(f"Especie: {especie}")
    print(f"Edad:    {edad}")
    print("=" * 50)


def main():
    """
    Función principal del programa.
    """
    # Registrar los datos de la mascota
    nombre_mascota, especie_mascota, edad_mascota = registrar_mascota()

    # Mostrar la información registrada
    mostrar_mascota(nombre_mascota, especie_mascota, edad_mascota)

    print("\n¡Mascota registrada exitosamente!")


# Ejecutar el programa
if __name__ == "__main__":
    main()





