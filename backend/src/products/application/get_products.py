"""
Get Products Use Cases

✅ Separación de responsabilidades: Un use case por operación
✅ Query objects para filtros complejos
"""

import asyncio
from typing import List, Optional, Tuple
from ..domain.interfaces.repositories import IProductRepository
from ..domain.models.product import Product


class GetProductsUseCase:
    """
    Use Case: Get all products with filters

    ✅ Maneja lógica de paginación y filtros
    ✅ Depende de abstracción (repository interface)
    """

    def __init__(self, repository: IProductRepository):
        """
        Initialize use case with repository

        Args:
            repository: Product repository implementation
        """
        self.repository = repository

    async def execute(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        search: Optional[str] = None,
        only_active: bool = True,
    ) -> Tuple[List[Product], int]:
        """
        Execute the use case

        Args:
            skip: Number of products to skip (pagination)
            limit: Maximum number of products to return
            category: Filter by category
            min_price: Minimum price filter
            max_price: Maximum price filter
            search: Search in product name
            only_active: Only return active products

        Returns:
            Tuple of (List of products matching filters, total count)

        Business Rules:
        - Default limit is 100 (prevent overload)
        - By default only active products
        - Pagination for performance
        """
        # ✅ Validación de parámetros
        if skip < 0:
            skip = 0

        if limit < 1:
            limit = 1
        elif limit > 100:
            limit = 100

        # ✅ Obtener productos y total en paralelo
        products, total = await asyncio.gather(
            self.repository.get_all(
                skip=skip,
                limit=limit,
                category=category,
                min_price=min_price,
                max_price=max_price,
                search=search,
                only_active=only_active,
            ),
            self.repository.count(
                category=category,
                min_price=min_price,
                max_price=max_price,
                search=search,
                only_active=only_active,
            ),
        )

        return products, total


class GetProductByIdUseCase:
    """
    Use Case: Get a single product by ID

    ✅ Single Responsibility: Solo obtener un producto
    ✅ Maneja lógica de negocio específica
    """

    def __init__(self, repository: IProductRepository):
        """
        Initialize use case with repository

        Args:
            repository: Product repository implementation
        """
        self.repository = repository

    async def execute(self, product_id: int) -> Optional[Product]:
        """
        Execute the use case

        Args:
            product_id: Product identifier

        Returns:
            Product if found, None otherwise

        Raises:
            ValueError: If product_id is invalid
        """
        # ✅ Validación de parámetros
        if product_id <= 0:
            raise ValueError("Product ID must be positive")

        # ✅ Delegar a repository
        product = await self.repository.get_by_id(product_id)

        # ✅ Aquí podríamos aplicar business rules adicionales
        # Por ejemplo, ocultar productos inactivos o aplicar permisos

        return product
