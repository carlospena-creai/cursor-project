"""
Infrastructure Layer - Clean Architecture

Esta capa contiene:
- Implementaciones concretas de repositories
- Adaptadores para frameworks externos (FastAPI, SQLite)
- API endpoints
- Configuración de base de datos

Principios:
- Implementa las interfaces del Domain Layer
- Depende de frameworks externos
- Es la capa más externa
- Intercambiable (podemos cambiar de SQLite a PostgreSQL)
"""
