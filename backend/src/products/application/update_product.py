"""
Update Product Use Case

✅ Maneja lógica de actualización compleja
✅ Validaciones de negocio
✅ Actualización parcial (PATCH)
"""

from typing import Optional
from ..domain.interfaces.repositories import IProductRepository
from ..domain.models.product import Product, ProductUpdate


class UpdateProductUseCase:
    """
    Use Case: Update an existing product

    ✅ Implementa lógica de actualización parcial
    ✅ Validaciones de negocio
    ✅ Manejo de casos edge
    """

    def __init__(self, repository: IProductRepository):
        """
        Initialize use case with repository

        Args:
            repository: Product repository implementation
        """
        self.repository = repository

    async def execute(
        self, product_id: int, product_data: ProductUpdate
    ) -> Optional[Product]:
        """
        Execute the use case

        Args:
            product_id: Product identifier
            product_data: Data for updating the product

        Returns:
            Updated Product if found, None otherwise

        Raises:
            ValueError: If validation fails or product_id invalid

        Business Rules:
        - Product must exist
        - Cannot update to invalid state
        - Only provided fields are updated (partial update)
        - Cannot deactivate if has pending orders (future)
        """
        # ✅ Validación de parámetros
        if product_id <= 0:
            raise ValueError("Product ID must be positive")

        # ✅ Verificar que el producto existe
        existing_product = await self.repository.get_by_id(product_id)
        if not existing_product:
            return None

        # ✅ Business rules adicionales
        # Por ejemplo, no permitir desactivar si hay órdenes pendientes
        if product_data.is_active is False:
            # Aquí verificaríamos órdenes pendientes
            # has_pending_orders = await order_service.has_pending_orders(product_id)
            # if has_pending_orders:
            #     raise ValueError("Cannot deactivate product with pending orders")
            pass

        # ✅ Validar que al menos un campo está siendo actualizado
        update_dict = product_data.dict(exclude_unset=True)
        if not update_dict:
            raise ValueError("No fields to update")

        # ✅ Delegar actualización al repository
        updated_product = await self.repository.update(product_id, product_data)

        # ✅ Aquí podríamos disparar eventos de dominio
        # await event_bus.publish(ProductUpdatedEvent(updated_product))

        return updated_product
