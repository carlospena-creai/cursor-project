"""
Contenedor de Inyección de Dependencias - Clean Architecture

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
from .domain.interfaces.repositories import IProductRepository

# Application
from .application.create_product import CreateProductUseCase
from .application.get_products import GetProductsUseCase, GetProductByIdUseCase
from .application.update_product import UpdateProductUseCase
from .application.delete_product import DeleteProductUseCase

# Infrastructure
from .infrastructure.db.repositories.product_repository import SQLiteProductRepository


# ============================================================================
# INSTANCIAS DE REPOSITORIO (Singletons)
# ============================================================================

_product_repository: Optional[IProductRepository] = None


def get_product_repository() -> IProductRepository:
    """
    Obtiene la instancia singleton del repositorio de productos

    Retorna la abstracción IProductRepository.
    Implementación actual: SQLiteProductRepository.
    Fácil cambiar a PostgreSQL, MongoDB, etc. modificando solo esta función.

    Returns:
        Implementación de IProductRepository
    """
    global _product_repository
    if _product_repository is None:
        _product_repository = SQLiteProductRepository()
    return _product_repository


# ============================================================================
# FACTORY FUNCTIONS PARA USE CASES
# ============================================================================


def get_create_product_use_case() -> CreateProductUseCase:
    """
    Crea y retorna una instancia de CreateProductUseCase

    Inyecta el repositorio automáticamente.
    El Use Case no conoce la implementación concreta del repositorio.

    Returns:
        Instancia de CreateProductUseCase
    """
    repository = get_product_repository()
    return CreateProductUseCase(repository)


def get_get_products_use_case() -> GetProductsUseCase:
    """
    Crea y retorna una instancia de GetProductsUseCase

    Returns:
        Instancia de GetProductsUseCase
    """
    repository = get_product_repository()
    return GetProductsUseCase(repository)


def get_get_product_by_id_use_case() -> GetProductByIdUseCase:
    """
    Crea y retorna una instancia de GetProductByIdUseCase

    Returns:
        Instancia de GetProductByIdUseCase
    """
    repository = get_product_repository()
    return GetProductByIdUseCase(repository)


def get_update_product_use_case() -> UpdateProductUseCase:
    """
    Crea y retorna una instancia de UpdateProductUseCase

    Returns:
        Instancia de UpdateProductUseCase
    """
    repository = get_product_repository()
    return UpdateProductUseCase(repository)


def get_delete_product_use_case() -> DeleteProductUseCase:
    """
    Crea y retorna una instancia de DeleteProductUseCase

    Returns:
        Instancia de DeleteProductUseCase
    """
    repository = get_product_repository()
    return DeleteProductUseCase(repository)


# ============================================================================
# CONFIGURACIÓN E INICIALIZACIÓN
# ============================================================================


def init_products_module():
    """
    Inicializa el módulo de productos

    Configura la base de datos y realiza el setup inicial del módulo.
    """
    from .infrastructure.db.connection import init_database

    print("🔧 Inicializando módulo de Products...")
    init_database()
    print("✅ Módulo de Products inicializado correctamente")
