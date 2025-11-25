import sqlite3
import os
from typing import Optional

# ❌ PROBLEMA: Configuración global básica sin validación
DATABASE_PATH = "ecommerce.db"


def get_database_url() -> str:
    """
    Get database URL/path.

    ❌ PROBLEMA: Hardcoded path sin environment variables
    ❌ PROBLEMA: No support para diferentes entornos
    """
    return DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    """
    Get database connection - shared utility.

    ❌ PROBLEMA: No connection pooling
    ❌ PROBLEMA: No configuración de performance
    ❌ PROBLEMA: No timeout configuration
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)

        # ❌ PROBLEMA: Configuraciones básicas comentadas
        # conn.execute("PRAGMA foreign_keys = ON")  # Should be enabled
        # conn.execute("PRAGMA journal_mode = WAL")  # For better concurrency
        # conn.execute("PRAGMA synchronous = NORMAL")  # For performance

        return conn
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        raise


def init_db():
    """
    Initialize all database tables.

    ✅ ACTUALIZADO: Usa Clean Architecture modules
    """
    try:
        print("🔧 Initializing shared database...")

        # ✅ Initialize products table - Clean Architecture version
        from src.products.infrastructure.db.connection import (
            init_database as init_products_db,
        )

        init_products_db()

        # ❌ PROBLEMA: No inicialización de otras tablas futuras:
        # - users table
        # - orders table
        # - order_items table
        # - categories table

        print("✅ Database initialization completed")

    except Exception as e:
        print(f"❌ Error during database initialization: {e}")
        raise


def check_db_health() -> dict:
    """
    Basic database health check.

    ❌ PROBLEMA: Health check muy básico
    ❌ PROBLEMA: No métricas de performance
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if we can query
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        # Check products table
        cursor.execute("SELECT COUNT(*) FROM products")
        products_count = cursor.fetchone()[0]

        conn.close()

        return {
            "status": "healthy",
            "database_path": DATABASE_PATH,
            "products_count": products_count,
            "connection_test": "passed",
        }

    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "database_path": DATABASE_PATH}


def reset_database():
    """
    Reset database - DELETE ALL DATA.

    ❌ PROBLEMA: Función peligrosa sin confirmaciones
    ❌ PROBLEMA: No backup antes del reset
    """
    try:
        if os.path.exists(DATABASE_PATH):
            print("⚠️  WARNING: Deleting existing database...")
            os.remove(DATABASE_PATH)

        print("🔧 Recreating database...")
        init_db()
        print("✅ Database reset completed")

    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        raise


# ❌ PROBLEMA: No funciones para:
# - Connection pooling management
# - Database migrations
# - Schema versioning
# - Backup/restore utilities
# - Performance monitoring
# - Connection cleanup
# - Transaction management utilities
