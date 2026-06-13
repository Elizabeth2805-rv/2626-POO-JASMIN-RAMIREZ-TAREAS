def registrar_mascota():
    """Registra la información de una mascota solicitando datos por teclado"""
    print("\n" + "="*50)
    print("REGISTRO DE MASCOTA")
    print("="*50)
    
    nombre = input("Ingrese nombre de su mascota: ").strip()
    especie = input("Ingrese especie de su mascota: ").strip()
    edad = input("Ingrese edad de su mascota: ").strip()
    color = input("Ingrese color de su mascota: ").strip()
    peso = input("Ingrese peso de su mascota (en kg): ").strip()
    
    mascota = {
        "nombre": nombre,
        "especie": especie,
        "edad": edad,
        "color": color,
        "peso": peso
    }
    
    return mascota


def mostrar_mascota(mascota):
    """Muestra la información de la mascota de forma organizada"""
    print("\n" + "="*50)
    print("INFORMACIÓN DE LA MASCOTA REGISTRADA")
    print("="*50)
    print(f"Nombre:  {mascota['nombre']}")
    print(f"Especie: {mascota['especie']}")
    print(f"Edad:    {mascota['edad']}")
    print(f"Color:   {mascota['color']}")
    print(f"Peso:    {mascota['peso']} kg")
    print("="*50 + "\n")


def main():
    """Función principal que controla el flujo del programa"""
    print("\n¡BIENVENIDO AL SISTEMA DE REGISTRO DE MASCOTAS!")
    
    mascotas = []
    
    while True:
        print("\nOPCIONES:")
        print("1. Registrar una nueva mascota")
        print("2. Ver mascotas registradas")
        print("3. Salir")
        
        opcion = input("Seleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            mascota = registrar_mascota()
            mascotas.append(mascota)
            print("\n✓ ¡Mascota registrada exitosamente!")
            
        elif opcion == "2":
            if len(mascotas) == 0:
                print("\nNo hay mascotas registradas aún.")
            else:
                print(f"\n--- Se encontraron {len(mascotas)} mascota(s) registrada(s) ---")
                for i, mascota in enumerate(mascotas, 1):
                    print(f"\nMascota #{i}")
                    mostrar_mascota(mascota)
                    
        elif opcion == "3":
            print("\n¡Gracias por usar el sistema! ¡Adiós!")
            break
        else:
            print("\n✗ Opción inválida. Por favor, seleccione una opción válida (1-3).")


if __name__ == "__main__":
    main()
