"""
Domain Layer - Clean Architecture

Esta capa contiene:
- Models de dominio puros (sin dependencias externas)
- Interfaces (abstracciones para repositorios)
- Value Objects
- Business rules y lógica de negocio

Principios:
- Sin dependencias externas (no FastAPI, no SQLite, etc.)
- Independiente del framework
- Pure Python con Pydantic para validación
"""
