# -*- coding: utf-8 -*-
# modelos/__init__.py
# Paquete de modelos del sistema restaurante_app.
# Facilita la importación de las clases del dominio desde un único punto.

from modelos.producto import Producto
from modelos.bebida import Bebida
from modelos.cliente import Cliente

__all__ = ["Producto", "Bebida", "Cliente"]
