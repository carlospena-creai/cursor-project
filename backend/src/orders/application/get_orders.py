"""
Get Orders Use Cases

✅ Separación de responsabilidades: Un use case por operación
✅ Query objects para filtros complejos
"""

from typing import List, Optional
from ..domain.interfaces.repositories import IOrderRepository
from ..domain.models.order import Order, OrderStatus


class GetOrdersUseCase:
    """
    Use Case: Get all orders with filters

    ✅ Maneja lógica de paginación y filtros
    ✅ Depende de abstracción (repository interface)
    """

    def __init__(self, repository: IOrderRepository):
        """
        Initialize use case with repository

        Args:
            repository: Order repository implementation
        """
        self.repository = repository

    async def execute(
        self,
        user_id: Optional[int] = None,
        status: Optional[OrderStatus] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Order]:
        """
        Execute the use case

        Args:
            user_id: Filter by user ID
            status: Filter by order status
            skip: Number of orders to skip (pagination)
            limit: Maximum number of orders to return

        Returns:
            List of orders matching filters

        Business Rules:
        - Default limit is 100 (prevent overload)
        - Pagination for performance
        - Can filter by user or status
        """
        # ✅ Validación de parámetros
        if skip < 0:
            skip = 0

        if limit < 1:
            limit = 1
        elif limit > 100:
            limit = 100

        if user_id is not None and user_id <= 0:
            raise ValueError("user_id must be positive")

        # ✅ Delegar a repository
        orders = await self.repository.get_all(
            user_id=user_id,
            status=status,
            skip=skip,
            limit=limit,
        )

        return orders


class GetOrderByIdUseCase:
    """
    Use Case: Get a single order by ID

    ✅ Single Responsibility: Solo obtener una orden
    ✅ Maneja lógica de negocio específica
    """

    def __init__(self, repository: IOrderRepository):
        """
        Initialize use case with repository

        Args:
            repository: Order repository implementation
        """
        self.repository = repository

    async def execute(self, order_id: int) -> Optional[Order]:
        """
        Execute the use case

        Args:
            order_id: Order identifier

        Returns:
            Order if found, None otherwise

        Raises:
            ValueError: If order_id is invalid
        """
        # ✅ Validación de parámetros
        if order_id <= 0:
            raise ValueError("Order ID must be positive")

        # ✅ Delegar a repository
        order = await self.repository.get_by_id(order_id)

        # ✅ Aquí podríamos aplicar business rules adicionales
        # Por ejemplo, verificar permisos de acceso

        return order
