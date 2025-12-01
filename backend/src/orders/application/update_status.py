"""
Use Case: Actualizar Estado de Orden

Principio de Responsabilidad Única: Solo se encarga de actualizar estados.
Dependency Injection: El repositorio es inyectado.
Clean Architecture: Depende de abstracciones (interfaces).
"""

from typing import Optional
from ..domain.interfaces.repositories import IOrderRepository
from ..domain.models.order import Order, OrderStatus


class UpdateOrderStatusUseCase:
    """
    Use Case: Actualizar el estado de una orden

    Implementa la lógica de aplicación para actualizar estados.
    Incluye validaciones de transiciones de estado válidas.
    """

    def __init__(self, repository: IOrderRepository):
        """
        Inicializa el use case con el repositorio

        Args:
            repository: Implementación del repositorio de órdenes
        """
        self.repository = repository

    async def execute(self, order_id: int, new_status: OrderStatus) -> Optional[Order]:
        """
        Ejecuta el use case

        Args:
            order_id: Identificador de la orden
            new_status: Nuevo estado

        Returns:
            Orden actualizada si existe, None si no se encuentra

        Raises:
            ValueError: Si la validación falla o la transición no es válida

        Reglas de Negocio Aplicadas:
        - La orden debe existir
        - La transición de estado debe ser válida
        - No se puede cambiar el estado de órdenes completadas o canceladas
        """
        # ✅ Validación de parámetros
        if order_id <= 0:
            raise ValueError("Order ID must be positive")

        # ✅ Obtener la orden existente
        order = await self.repository.get_by_id(order_id)
        if not order:
            return None

        # ✅ Validar transición de estado usando la lógica del dominio
        try:
            order.update_status(new_status)
        except ValueError as e:
            raise ValueError(f"Invalid status transition: {str(e)}")

        # ✅ Actualizar en el repositorio
        updated_order = await self.repository.update_status(order_id, new_status)

        # ✅ Aquí podríamos disparar eventos de dominio
        # await event_bus.publish(OrderStatusChangedEvent(updated_order))

        return updated_order
