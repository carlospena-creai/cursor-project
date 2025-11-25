"""
Application Layer - Clean Architecture

Esta capa contiene:
- Use Cases (casos de uso de la aplicación)
- Application Services
- DTOs específicos de aplicación
- Orquestación de lógica de negocio

Principios:
- Depende solo del Domain Layer
- No depende de Infrastructure
- Coordina operaciones del dominio
- Implementa casos de uso específicos
"""

from .create_product import CreateProductUseCase
from .get_products import GetProductsUseCase, GetProductByIdUseCase
from .update_product import UpdateProductUseCase
from .delete_product import DeleteProductUseCase

__all__ = [
    "CreateProductUseCase",
    "GetProductsUseCase",
    "GetProductByIdUseCase",
    "UpdateProductUseCase",
    "DeleteProductUseCase",
]
