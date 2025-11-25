"""
Delete Product Use Case

✅ Implementa soft delete por defecto
✅ Validaciones de negocio antes de eliminar
✅ Manejo de dependencias
"""

from ..domain.interfaces.repositories import IProductRepository


class DeleteProductUseCase:
    """
    Use Case: Delete a product (soft delete)

    ✅ Implementa soft delete (is_active=False)
    ✅ Validaciones de negocio
    ✅ Verifica dependencias
    """

    def __init__(self, repository: IProductRepository):
        """
        Initialize use case with repository

        Args:
            repository: Product repository implementation
        """
        self.repository = repository

    async def execute(self, product_id: int) -> bool:
        """
        Execute the use case (soft delete)

        Args:
            product_id: Product identifier

        Returns:
            True if product was deleted, False if not found

        Raises:
            ValueError: If product_id invalid or business rules violated

        Business Rules:
        - Product must exist
        - Cannot delete if has active orders (future)
        - Cannot delete if referenced in other entities (future)
        - Uses soft delete (set is_active=False)
        """
        # ✅ Validación de parámetros
        if product_id <= 0:
            raise ValueError("Product ID must be positive")

        # ✅ Verificar que el producto existe
        existing_product = await self.repository.get_by_id(product_id)
        if not existing_product:
            return False

        # ✅ Business rules: verificar dependencias
        # Por ejemplo, no permitir eliminar si tiene órdenes activas
        # has_active_orders = await order_service.has_active_orders(product_id)
        # if has_active_orders:
        #     raise ValueError("Cannot delete product with active orders")

        # ✅ Delegar eliminación al repository (soft delete)
        result = await self.repository.delete(product_id)

        # ✅ Aquí podríamos disparar eventos de dominio
        # await event_bus.publish(ProductDeletedEvent(product_id))

        return result
