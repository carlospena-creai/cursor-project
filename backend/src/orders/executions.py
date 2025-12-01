"""
Contenedor de Inyección de Dependencias - Orders Module

Inyección de dependencias manual (sin framework).
Factory functions para Use Cases.
Principio de Inversión de Dependencias (SOLID-D).

Este archivo conecta todas las capas:
- Domain (interfaces)
- Application (use cases)
- Infrastructure (implementaciones)
"""

from typing import Optional

# Domain
from .domain.interfaces.repositories import IOrderRepository

# Application
from .application.create_order import CreateOrderUseCase
from .application.get_orders import GetOrdersUseCase, GetOrderByIdUseCase
from .application.update_status import UpdateOrderStatusUseCase

# Infrastructure
from .infrastructure.db.repositories.order_repository import SQLiteOrderRepository

# Dependencias de otros módulos
from ..products.executions import get_product_repository
from ..users.executions import get_user_repository


# ============================================================================
# INSTANCIAS DE REPOSITORIO (Singletons)
# ============================================================================

_order_repository: Optional[IOrderRepository] = None


def get_order_repository() -> IOrderRepository:
    """
    Obtiene la instancia singleton del repositorio de órdenes

    Retorna la abstracción IOrderRepository.
    Implementación actual: SQLiteOrderRepository.
    Fácil cambiar a PostgreSQL, MongoDB, etc. modificando solo esta función.

    Returns:
        Implementación de IOrderRepository
    """
    global _order_repository
    if _order_repository is None:
        _order_repository = SQLiteOrderRepository()
    return _order_repository


# ============================================================================
# FACTORY FUNCTIONS PARA USE CASES
# ============================================================================


def get_create_order_use_case() -> CreateOrderUseCase:
    """
    Crea y retorna una instancia de CreateOrderUseCase

    Inyecta los repositorios automáticamente.
    El Use Case no conoce las implementaciones concretas.

    Returns:
        Instancia de CreateOrderUseCase
    """
    order_repository = get_order_repository()
    product_repository = get_product_repository()
    user_repository = get_user_repository()
    return CreateOrderUseCase(order_repository, product_repository, user_repository)


def get_get_orders_use_case() -> GetOrdersUseCase:
    """
    Crea y retorna una instancia de GetOrdersUseCase

    Returns:
        Instancia de GetOrdersUseCase
    """
    repository = get_order_repository()
    return GetOrdersUseCase(repository)


def get_get_order_by_id_use_case() -> GetOrderByIdUseCase:
    """
    Crea y retorna una instancia de GetOrderByIdUseCase

    Returns:
        Instancia de GetOrderByIdUseCase
    """
    repository = get_order_repository()
    return GetOrderByIdUseCase(repository)


def get_update_order_status_use_case() -> UpdateOrderStatusUseCase:
    """
    Crea y retorna una instancia de UpdateOrderStatusUseCase

    Returns:
        Instancia de UpdateOrderStatusUseCase
    """
    repository = get_order_repository()
    return UpdateOrderStatusUseCase(repository)


# ============================================================================
# CONFIGURACIÓN E INICIALIZACIÓN
# ============================================================================


def init_orders_module():
    """
    Inicializa el módulo de órdenes

    Configura la base de datos y realiza el setup inicial del módulo.
    """
    from .infrastructure.db.connection import init_order_database

    print("🔧 Inicializando módulo de Orders...")
    init_order_database()
    print("✅ Módulo de Orders inicializado correctamente")
