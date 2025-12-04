"""
Interfaces de Repositorio - Orders Module

Define los contratos para operaciones de persistencia de órdenes.
Principio de Inversión de Dependencias (SOLID-D).
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.order import Order, OrderCreate, OrderUpdate, OrderStatus


class IOrderRepository(ABC):
    """
    Interfaz del Repositorio de Órdenes

    Define el contrato para operaciones de persistencia.
    Independiente de la implementación concreta.
    """

    @abstractmethod
    async def create(self, order_data: OrderCreate) -> Order:
        """
        Crea una nueva orden

        Args:
            order_data: Datos para crear la orden

        Returns:
            Orden creada con ID asignado

        Raises:
            ValueError: Si la validación falla
        """
        pass

    @abstractmethod
    async def get_by_id(self, order_id: int) -> Optional[Order]:
        """
        Obtiene una orden por ID

        Args:
            order_id: Identificador de la orden

        Returns:
            Orden si existe, None si no se encuentra
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        user_id: Optional[int] = None,
        status: Optional[OrderStatus] = None,
        skip: int = 0,
        limit: int = 100,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[Order]:
        """
        Obtiene todas las órdenes con filtros opcionales y ordenamiento

        Args:
            user_id: Filtrar por usuario
            status: Filtrar por estado
            skip: Número de órdenes a omitir (paginación)
            limit: Número máximo de órdenes a retornar
            sort_by: Campo por el cual ordenar (id, user_id, status, total, created_at, updated_at)
            sort_order: Orden de clasificación (asc, desc)

        Returns:
            Lista de órdenes que coinciden con los filtros
        """
        pass

    @abstractmethod
    async def update(self, order_id: int, order_data: OrderUpdate) -> Optional[Order]:
        """
        Actualiza una orden existente

        Args:
            order_id: Identificador de la orden
            order_data: Datos para actualizar la orden

        Returns:
            Orden actualizada si existe, None si no se encuentra
        """
        pass

    @abstractmethod
    async def update_status(
        self, order_id: int, new_status: OrderStatus
    ) -> Optional[Order]:
        """
        Actualiza el estado de una orden

        Args:
            order_id: Identificador de la orden
            new_status: Nuevo estado

        Returns:
            Orden actualizada si existe, None si no se encuentra
        """
        pass

    @abstractmethod
    async def exists(self, order_id: int) -> bool:
        """
        Verifica si una orden existe

        Args:
            order_id: Identificador de la orden

        Returns:
            True si la orden existe, False en caso contrario
        """
        pass

    @abstractmethod
    async def count(
        self, user_id: Optional[int] = None, status: Optional[OrderStatus] = None
    ) -> int:
        """
        Cuenta órdenes con filtros opcionales

        Args:
            user_id: Filtrar por usuario
            status: Filtrar por estado

        Returns:
            Número de órdenes que coinciden con los filtros
        """
        pass
