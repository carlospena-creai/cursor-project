"""
Get Orders Use Cases

✅ Separación de responsabilidades: Un use case por operación
✅ Query objects para filtros complejos
"""

import asyncio
from typing import List, Optional, Tuple
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
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> Tuple[List[Order], int]:
        """
        Execute the use case

        Args:
            user_id: Filter by user ID
            status: Filter by order status
            skip: Number of orders to skip (pagination)
            limit: Maximum number of orders to return
            sort_by: Field to sort by (id, user_id, status, total, created_at, updated_at)
            sort_order: Sort order (asc, desc)

        Returns:
            Tuple of (List of orders matching filters, total count)

        Business Rules:
        - Default limit is 100 (prevent overload)
        - Pagination for performance
        - Can filter by user or status
        - Validates sort_by and sort_order
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

        # ✅ Validar sort_by
        valid_sort_fields = [
            "id",
            "user_id",
            "status",
            "total",
            "created_at",
            "updated_at",
        ]
        if sort_by and sort_by not in valid_sort_fields:
            raise ValueError(
                f"Invalid sort_by field. Must be one of: {valid_sort_fields}"
            )

        # ✅ Validar sort_order
        if sort_order and sort_order not in ["asc", "desc"]:
            raise ValueError("sort_order must be 'asc' or 'desc'")

        # ✅ Obtener órdenes y total en paralelo
        orders, total = await asyncio.gather(
            self.repository.get_all(
                user_id=user_id,
                status=status,
                skip=skip,
                limit=limit,
                sort_by=sort_by,
                sort_order=sort_order,
            ),
            self.repository.count(
                user_id=user_id,
                status=status,
            ),
        )

        return orders, total


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
