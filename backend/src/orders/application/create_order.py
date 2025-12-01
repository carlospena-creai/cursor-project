"""
Use Case: Crear Orden

Principio de Responsabilidad Única: Solo se encarga de crear órdenes.
Dependency Injection: Los repositorios son inyectados.
Clean Architecture: Depende de abstracciones (interfaces).
"""

from ..domain.interfaces.repositories import IOrderRepository
from ..domain.models.order import Order, OrderCreate
from ...products.domain.models.product import ProductUpdate
from ...products.domain.interfaces.repositories import IProductRepository
from ...users.domain.interfaces.repositories import IUserRepository


class CreateOrderUseCase:
    """
    Use Case: Crear una nueva orden

    Recibe los repositorios por inyección de dependencias.
    Implementa la lógica de aplicación para la creación de órdenes.
    Incluye validaciones de negocio:
    - Verificar que el usuario existe
    - Verificar que los productos existen y tienen stock suficiente
    - Calcular totales
    - Reducir stock de productos
    """

    def __init__(
        self,
        order_repository: IOrderRepository,
        product_repository: IProductRepository,
        user_repository: IUserRepository,
    ):
        """
        Inicializa el use case con los repositorios

        Args:
            order_repository: Implementación del repositorio de órdenes
            product_repository: Implementación del repositorio de productos
            user_repository: Implementación del repositorio de usuarios
        """
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.user_repository = user_repository

    async def execute(self, order_data: OrderCreate) -> Order:
        """
        Ejecuta el use case

        Args:
            order_data: Datos para crear la orden

        Returns:
            Orden creada

        Raises:
            ValueError: Si la validación falla o no hay stock suficiente
            RuntimeError: Si el usuario no existe

        Reglas de Negocio Aplicadas:
        - El usuario debe existir y estar activo
        - Los productos deben existir y estar activos
        - Debe haber stock suficiente para cada producto
        - Se toma snapshot del precio al momento de la compra
        - Se reduce el stock de los productos
        - Se calcula el total automáticamente
        """
        # 1. Verificar que el usuario existe
        user = await self.user_repository.get_by_id(order_data.user_id)
        if not user:
            raise ValueError(f"User with id {order_data.user_id} not found")
        if not user.is_active:
            raise ValueError(f"User with id {order_data.user_id} is not active")

        # 2. Validar items y reducir stock
        # Verificamos que todos los productos existan, estén activos y tengan stock
        for item in order_data.items:
            product_id = item.product_id
            quantity = item.quantity

            # Obtener producto
            product = await self.product_repository.get_by_id(product_id)
            if not product:
                raise ValueError(f"Product with id {product_id} not found")

            # Verificar que el producto está activo
            if not product.is_active:
                raise ValueError(f"Product with id {product_id} is not active")

            # Verificar stock suficiente
            if not product.can_fulfill_quantity(quantity):
                raise ValueError(
                    f"Insufficient stock for product {product_id}. "
                    f"Requested: {quantity}, Available: {product.stock}"
                )

            # Reducir stock del producto
            product.reduce_stock(quantity)

            # Actualizar stock en el repositorio
            product_update = ProductUpdate(stock=product.stock)
            await self.product_repository.update(product_id, product_update)

        # 3. Persistir la orden
        # El repositorio se encargará de:
        # - Obtener los productos para construir OrderItems completos con precios actuales
        # - Calcular totales
        # - Persistir orden e items
        created_order = await self.order_repository.create(order_data)

        # Aquí podríamos disparar eventos de dominio
        # await event_bus.publish(OrderCreatedEvent(created_order))

        return created_order
