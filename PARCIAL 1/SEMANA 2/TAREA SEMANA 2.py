"""
Ejemplo básico de programación orientada a objetos.
Clase: CuentaBancaria

Incluye métodos para depositar, retirar, transferir y mostrar saldo.
Ejemplo de uso en la sección `if __name__ == "__main__"`.
"""

from typing import Optional


class CuentaBancaria:
	"""Representa una cuenta bancaria simple.

	Atributos:
		titular (str): Nombre del titular de la cuenta.
		numero (str): Número identificador de la cuenta.
		saldo (float): Saldo actual de la cuenta.
	"""

	def __init__(self, titular: str, numero: str, saldo: float = 0.0) -> None:
		self.titular = titular
		self.numero = numero
		self.saldo = float(saldo)

	def depositar(self, cantidad: float) -> None:
		"""Deposita una cantidad positiva en la cuenta."""
		if cantidad <= 0:
			raise ValueError("La cantidad a depositar debe ser mayor que cero.")
		self.saldo += cantidad

	def retirar(self, cantidad: float) -> None:
		"""Retira una cantidad si hay saldo suficiente."""
		if cantidad <= 0:
			raise ValueError("La cantidad a retirar debe ser mayor que cero.")
		if cantidad > self.saldo:
			raise ValueError("Saldo insuficiente para realizar el retiro.")
		self.saldo -= cantidad

	def transferir(self, destino: 'CuentaBancaria', cantidad: float) -> None:
		"""Transfiere una cantidad a otra cuenta si es posible."""
		if not isinstance(destino, CuentaBancaria):
			raise TypeError("El destino debe ser una CuentaBancaria.")
		self.retirar(cantidad)
		destino.depositar(cantidad)

	def ver_saldo(self) -> float:
		"""Devuelve el saldo actual."""
		return self.saldo

	def __str__(self) -> str:
		return f"Cuenta {self.numero} - Titular: {self.titular} - Saldo: ${self.saldo:.2f}"


def ejemplo_uso() -> None:
	"""Función demostrativa que crea cuentas y realiza operaciones."""
	cuenta_a = CuentaBancaria("Ana Pérez", "ES001", 1000.0)
	cuenta_b = CuentaBancaria("Luis Gómez", "ES002", 250.0)

	print("Estado inicial:")
	print(cuenta_a)
	print(cuenta_b)

	print("\nAna deposita $200 y retira $150:")
	cuenta_a.depositar(200)
	cuenta_a.retirar(150)
	print(cuenta_a)

	print("\nTransferencia de Ana a Luis: $300")
	cuenta_a.transferir(cuenta_b, 300)
	print(cuenta_a)
	print(cuenta_b)


if __name__ == "__main__":
	ejemplo_uso()

