"""
Users Module - Clean Architecture

Módulo de autenticación y gestión de usuarios.
Implementa JWT authentication y user management.

Estructura:
    users/
    ├── domain/              # Capa de dominio pura
    │   ├── interfaces/      # Abstracciones
    │   └── models/          # Domain models
    ├── application/         # Casos de uso
    │   ├── register.py
    │   ├── login.py
    │   └── get_profile.py
    ├── infrastructure/      # Implementaciones concretas
    │   ├── api/            # FastAPI endpoints
    │   └── db/             # Repository
    └── executions.py       # DI Container

Principios aplicados:
- SOLID
- Clean Architecture
- JWT Security
- Password Hashing
"""

__version__ = "1.0.0"

from .infrastructure.api import router

__all__ = ["router"]
