# Clase Restaurante - Gestiona todas las operaciones del restaurante
# Se importan las clases que se utilizarán en este módulo
from modelos.producto import Producto
from modelos.cliente import Cliente


class Restaurante:
    """
    Clase principal que gestiona las operaciones del restaurante.
    Administra productos disponibles, clientes registrados y pedidos realizados.
    Esta clase representa la lógica de negocio central del sistema.
    """
    
    def __init__(self, nombre, direccion):
        """
        Constructor de la clase Restaurante
        
        Args:
            nombre: Nombre del restaurante
            direccion: Dirección física del restaurante
        """
        self.nombre = nombre
        self.direccion = direccion
        self.productos = []  # Lista para almacenar productos disponibles
        self.clientes = []   # Lista para almacenar clientes registrados
        self.pedidos_realizados = []  # Registro de todos los pedidos
    
    def agregar_producto(self, producto):
        """
        Añade un nuevo producto al menú del restaurante
        
        Args:
            producto: Objeto de tipo Producto a agregar
            
        Returns:
            bool: True si se agregó exitosamente, False si ya existe
        """
        # Verificar que el producto no esté duplicado
        for prod in self.productos:
            if prod.id_producto == producto.id_producto:
                print(f"Error: El producto con ID {producto.id_producto} ya existe")
                return False
        
        self.productos.append(producto)
        print(f"Producto '{producto.nombre}' agregado al menú")
        return True
    
    def agregar_cliente(self, cliente):
        """
        Registra un nuevo cliente en el sistema
        
        Args:
            cliente: Objeto de tipo Cliente a registrar
            
        Returns:
            bool: True si se registró exitosamente, False si ya existe
        """
        # Verificar que el cliente no esté duplicado
        for clnt in self.clientes:
            if clnt.id_cliente == cliente.id_cliente:
                print(f"Error: El cliente con ID {cliente.id_cliente} ya existe")
                return False
        
        self.clientes.append(cliente)
        print(f"Cliente '{cliente.nombre}' registrado en el sistema")
        return True
    
    def buscar_producto(self, id_producto):
        """
        Busca un producto por su ID
        
        Args:
            id_producto: ID del producto a buscar
            
        Returns:
            Producto o None si no se encuentra
        """
        for producto in self.productos:
            if producto.id_producto == id_producto:
                return producto
        return None
    
    def buscar_cliente(self, id_cliente):
        """
        Busca un cliente por su ID
        
        Args:
            id_cliente: ID del cliente a buscar
            
        Returns:
            Cliente o None si no se encuentra
        """
        for cliente in self.clientes:
            if cliente.id_cliente == id_cliente:
                return cliente
        return None
    
    def registrar_pedido(self, id_cliente, lista_productos):
        """
        Registra un pedido de un cliente
        
        Args:
            id_cliente: ID del cliente que realiza el pedido
            lista_productos: Lista de tuplas (id_producto, cantidad)
            
        Returns:
            dict: Información del pedido registrado o None si hay error
        """
        cliente = self.buscar_cliente(id_cliente)
        if not cliente:
            print(f"Error: Cliente con ID {id_cliente} no encontrado")
            return None
        
        # Calcular el total del pedido
        total_pedido = 0
        detalle_pedido = []
        
        for id_prod, cantidad in lista_productos:
            producto = self.buscar_producto(id_prod)
            if not producto:
                print(f"Error: Producto con ID {id_prod} no encontrado")
                return None
            
            subtotal = producto.precio * cantidad
            total_pedido += subtotal
            detalle_pedido.append({
                'producto': producto.nombre,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
        
        # Crear el registro del pedido
        pedido = {
            'cliente': cliente.nombre,
            'detalle': detalle_pedido,
            'total': total_pedido
        }
        
        # Agregar el pedido al historial del cliente y al del restaurante
        cliente.agregar_pedido(pedido)
        self.pedidos_realizados.append(pedido)
        
        print(f"\nPedido registrado para {cliente.nombre}")
        print(f"Total: ${total_pedido:.2f}")
        return pedido
    
    def mostrar_productos(self):
        """
        Muestra todos los productos disponibles en el restaurante
        """
        print("\n" + "="*80)
        print(f"MENÚ DEL RESTAURANTE: {self.nombre}")
        print("="*80)
        
        if len(self.productos) == 0:
            print("No hay productos disponibles")
            return
        
        # Agrupar productos por categoría
        categorias = {}
        for producto in self.productos:
            if producto.categoria not in categorias:
                categorias[producto.categoria] = []
            categorias[producto.categoria].append(producto)
        
        # Mostrar productos por categoría
        for categoria, prods in categorias.items():
            print(f"\n--- {categoria.upper()} ---")
            for producto in prods:
                print(f"  {producto}")
        print("="*80)
    
    def mostrar_clientes(self):
        """
        Muestra todos los clientes registrados en el sistema
        """
        print("\n" + "="*80)
        print("CLIENTES REGISTRADOS")
        print("="*80)
        
        if len(self.clientes) == 0:
            print("No hay clientes registrados")
            return
        
        for cliente in self.clientes:
            print(f"  {cliente}")
        print("="*80)
    
    def mostrar_pedidos(self):
        """
        Muestra el resumen de todos los pedidos realizados
        """
        print("\n" + "="*80)
        print("HISTORIAL DE PEDIDOS")
        print("="*80)
        
        if len(self.pedidos_realizados) == 0:
            print("No hay pedidos registrados")
            return
        
        for i, pedido in enumerate(self.pedidos_realizados, 1):
            print(f"\nPedido #{i} - Cliente: {pedido['cliente']}")
            for item in pedido['detalle']:
                print(f"  - {item['producto']} x{item['cantidad']}: ${item['subtotal']:.2f}")
            print(f"  Total: ${pedido['total']:.2f}")
        
        print("="*80)
    
    def mostrar_informacion_general(self):
        """
        Muestra información general del restaurante
        """
        print("\n" + "="*80)
        print(f"INFORMACIÓN DEL RESTAURANTE: {self.nombre}")
        print("="*80)
        print(f"Dirección: {self.direccion}")
        print(f"Productos en el menú: {len(self.productos)}")
        print(f"Clientes registrados: {len(self.clientes)}")
        print(f"Pedidos realizados: {len(self.pedidos_realizados)}")
        
        if len(self.pedidos_realizados) > 0:
            total_ingresos = sum(pedido['total'] for pedido in self.pedidos_realizados)
            print(f"Ingresos totales: ${total_ingresos:.2f}")
        
        print("="*80)
