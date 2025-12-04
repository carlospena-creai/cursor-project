"""
Interfaces de Repositorio - Clean Architecture

Define los contratos para operaciones de persistencia.
Permite múltiples implementaciones (SQLite, PostgreSQL, MongoDB, etc.)
Principio de Inversión de Dependencias (SOLID-D).
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.product import Product, ProductCreate, ProductUpdate


class IProductRepository(ABC):
    """
    Interfaz del Repositorio de Productos

    Define el contrato para operaciones de persistencia.
    Independiente de la implementación concreta.
    Permite testing con mocks y facilita el cambio de tecnología de persistencia.
    """

    @abstractmethod
    async def create(self, product_data: ProductCreate) -> Product:
        """
        Crea un nuevo producto

        Args:
            product_data: Datos para crear el producto

        Returns:
            Producto creado con ID asignado

        Raises:
            ValueError: Si la validación falla
        """
        pass

    @abstractmethod
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por ID

        Args:
            product_id: Identificador del producto

        Returns:
            Producto si existe, None si no se encuentra
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        search: Optional[str] = None,
        only_active: bool = True,
    ) -> List[Product]:
        """
        Obtiene todos los productos con filtros opcionales

        Args:
            skip: Número de productos a omitir (paginación)
            limit: Número máximo de productos a retornar
            category: Filtrar por categoría
            min_price: Precio mínimo
            max_price: Precio máximo
            search: Búsqueda en nombre del producto
            only_active: Solo retornar productos activos

        Returns:
            Lista de productos que coinciden con los filtros
        """
        pass

    @abstractmethod
    async def update(
        self, product_id: int, product_data: ProductUpdate
    ) -> Optional[Product]:
        """
        Actualiza un producto existente

        Args:
            product_id: Identificador del producto
            product_data: Datos para actualizar el producto

        Returns:
            Producto actualizado si existe, None si no se encuentra
        """
        pass

    @abstractmethod
    async def delete(self, product_id: int) -> bool:
        """
        Elimina un producto (soft delete - establece is_active=False)

        Args:
            product_id: Identificador del producto

        Returns:
            True si el producto fue eliminado, False si no se encontró
        """
        pass

    @abstractmethod
    async def exists(self, product_id: int) -> bool:
        """
        Verifica si un producto existe

        Args:
            product_id: Identificador del producto

        Returns:
            True si el producto existe, False en caso contrario
        """
        pass

    @abstractmethod
    async def count(
        self,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        search: Optional[str] = None,
        only_active: bool = True,
    ) -> int:
        """
        Cuenta productos con filtros opcionales

        Args:
            category: Filtrar por categoría
            min_price: Precio mínimo
            max_price: Precio máximo
            search: Búsqueda en nombre del producto
            only_active: Solo contar productos activos

        Returns:
            Número de productos que coinciden con los filtros
        """
        pass
