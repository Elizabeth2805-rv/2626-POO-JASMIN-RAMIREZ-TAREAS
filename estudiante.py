class Estudiante:

    def __init__(self, nombre, carrera, semestre):
        self.nombre = nombre
        self.carrera = carrera
        self.semestre = semestre
    def mostrar_datos(self):
        print("Nombre:", self.nombre)
        print("Carrera:", self.carrera)
        print("Semestre:", self.semestre)

    def estudiar(self):
        print(self.nombre, "está estudiando Programación en Python.")

estudiante1 = Estudiante("Elizabeth Ramirez", "Tecnologías de la Información", 2)
estudiante2 = Estudiante("Carlos Mendoza", "Ingeniería en Sistemas", 3)

print("===== ESTUDIANTE 1 =====")
estudiante1.mostrar_datos()
estudiante1.estudiar()

print("\n===== ESTUDIANTE 2 =====")
estudiante2.mostrar_datos()
estudiante2.estudiar()
