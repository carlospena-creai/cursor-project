"""
Products Module - Clean Architecture

Este módulo implementa Clean Architecture con:
- Domain Layer: Models e Interfaces puros
- Application Layer: Use Cases
- Infrastructure Layer: Repositories y API
- DI Container: Dependency Injection

Estructura:
    products/
    ├── domain/              # ✅ Capa de dominio pura
    │   ├── interfaces/      # Abstracciones (IProductRepository)
    │   └── models/          # Domain models (Product)
    ├── application/         # ✅ Casos de uso
    │   ├── create_product.py
    │   ├── get_products.py
    │   ├── update_product.py
    │   └── delete_product.py
    ├── infrastructure/      # ✅ Implementaciones concretas
    │   ├── api/            # FastAPI endpoints
    │   └── db/             # SQLite repository
    └── executions.py       # ✅ DI Container

Principios aplicados:
- SOLID (todos los principios)
- Dependency Inversion
- Clean Architecture
- Domain-Driven Design
- Repository Pattern
"""

__version__ = "1.0.0"
__author__ = "Clean Architecture Refactoring"

# Exportar el router principal para uso externo
from .infrastructure.api import router

__all__ = ["router"]
