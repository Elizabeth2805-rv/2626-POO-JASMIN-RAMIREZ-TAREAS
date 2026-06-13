from mascota import Mascota

# Crear el primer objeto de la clase Mascota: Un perro
mascota1 = Mascota("Max", "Perro", 3)

# Crear el segundo objeto de la clase Mascota: Un gato
mascota2 = Mascota("Luna", "Gato", 2)

# Crear un tercer objeto para demostrar más la funcionalidad: Un pajaro
mascota3 = Mascota("Tweety", "Pajaro", 1)

print("=" * 40)
print("PROGRAMA DE MASCOTAS")
print("=" * 40)
print()

# Ejecutar métodos del primer objeto (perro)
print("Información de la primera mascota:")
mascota1.mostrar_informacion()
print("Sonido que hace:")
mascota1.hacer_sonido()

# Ejecutar métodos del segundo objeto (gato)
print("Información de la segunda mascota:")
mascota2.mostrar_informacion()
print("Sonido que hace:")
mascota2.hacer_sonido()

# Ejecutar métodos del tercer objeto (pajaro)
print("Información de la tercera mascota:")
mascota3.mostrar_informacion()
print("Sonido que hace:")
mascota3.hacer_sonido()

print("=" * 40)
print("Fin del programa")
print("=" * 40)

