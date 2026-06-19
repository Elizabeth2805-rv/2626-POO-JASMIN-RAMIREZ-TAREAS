# Clase Cliente - Representa a una persona que consume en el restaurante

class Cliente:
    """
    Representa un cliente del restaurante.
    Almacena información personal del cliente y el registro de sus pedidos.
    """
    
    def __init__(self, id_cliente, nombre, email, telefono):
        """
        Constructor de la clase Cliente
        
        Args:
            id_cliente: Identificador único del cliente
            nombre: Nombre completo del cliente
            email: Correo electrónico del cliente
            telefono: Número de teléfono del cliente
        """
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.pedidos = []  # Lista para almacenar los pedidos del cliente
        self.cantidad_pedidos = 0  # Contador de pedidos realizados
    
    def __str__(self):
        """
        Representación en texto del cliente
        """
        return (f"[ID: {self.id_cliente}] {self.nombre} - Email: {self.email} - "
                f"Teléfono: {self.telefono} - Pedidos realizados: {self.cantidad_pedidos}")
    
    def agregar_pedido(self, pedido):
        """
        Registra un nuevo pedido del cliente
        
        Args:
            pedido: Diccionario o objeto con información del pedido
        """
        self.pedidos.append(pedido)
        self.cantidad_pedidos += 1
    
    def obtener_historial_pedidos(self):
        """
        Retorna el historial completo de pedidos del cliente
        
        Returns:
            list: Lista de todos los pedidos realizados
        """
        if len(self.pedidos) == 0:
            return "El cliente no tiene pedidos registrados"
        return self.pedidos
    
    def obtener_total_gastado(self):
        """
        Calcula el monto total gastado por el cliente en todos sus pedidos
        
        Returns:
            float: Monto total acumulado
        """
        total = 0
        for pedido in self.pedidos:
            if isinstance(pedido, dict) and 'total' in pedido:
                total += pedido['total']
        return total
