"""
Gestor de Conexión a Base de Datos

Provee connection pooling simulado, context managers para transacciones,
y configuración apropiada de SQLite.
"""

import sqlite3
import os
from typing import Optional
from contextlib import contextmanager


class DatabaseConnection:
    """
    Gestor de Conexión a Base de Datos

    Maneja conexiones de forma segura con context managers.
    Implementa connection pooling básico.
    """

    def __init__(self, db_path: str = "ecommerce.db"):
        """
        Inicializa el gestor de conexiones

        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        """
        Obtiene una conexión a la base de datos

        Configura foreign keys y row factory para acceso por nombre de columna.

        Returns:
            Conexión SQLite configurada
        """
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def transaction(self):
        """
        Context manager para transacciones

        Auto-commit en éxito, auto-rollback en error.

        Usage:
            with db_connection.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT ...")
        """
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_schema(self):
        """
        Inicializa el schema de la base de datos con constraints apropiados

        - CHECK constraints para validaciones a nivel de BD
        - Índices para mejorar performance
        - Tipos de datos apropiados (INTEGER para centavos)
        """
        with self.transaction() as conn:
            cursor = conn.cursor()

            # Tabla products con constraints apropiados
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL CHECK(length(trim(name)) > 0),
                price INTEGER NOT NULL CHECK(price > 0),
                stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0),
                category TEXT NOT NULL CHECK(length(trim(category)) > 0),
                description TEXT,
                is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0, 1)),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Índices para performance
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_category 
            ON products(category)
            """)

            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_price 
            ON products(price)
            """)

            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_active 
            ON products(is_active)
            """)

            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_name 
            ON products(name)
            """)

            # Trigger para actualizar updated_at automáticamente
            cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_product_timestamp 
            AFTER UPDATE ON products
            BEGIN
                UPDATE products SET updated_at = CURRENT_TIMESTAMP 
                WHERE id = NEW.id;
            END
            """)

    def seed_data(self):
        """Inserta datos de ejemplo si la base de datos está vacía"""
        with self.transaction() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]

            if count == 0:
                print("📦 Insertando productos de ejemplo...")

                # Precios en centavos (89999 = $899.99)
                sample_products = [
                    (
                        "Laptop HP Pavilion",
                        89999,
                        10,
                        "Electronics",
                        "High performance laptop perfect for work and entertainment",
                    ),
                    (
                        "iPhone 15 Pro",
                        99999,
                        5,
                        "Electronics",
                        "Latest iPhone model with advanced camera system",
                    ),
                    (
                        "Coffee Maker Deluxe",
                        15999,
                        15,
                        "Home",
                        "Premium coffee maker for the perfect morning brew",
                    ),
                    (
                        "Running Shoes Pro",
                        12999,
                        20,
                        "Sports",
                        "Comfortable running shoes for professional athletes",
                    ),
                    (
                        "Wireless Headphones",
                        7999,
                        25,
                        "Electronics",
                        "Premium sound quality with noise cancellation",
                    ),
                    (
                        "Smart Watch",
                        24999,
                        12,
                        "Electronics",
                        "Track your fitness and stay connected",
                    ),
                    (
                        "Yoga Mat Premium",
                        4999,
                        30,
                        "Sports",
                        "High-quality yoga mat for your daily practice",
                    ),
                    (
                        "Ceramic Coffee Mug",
                        1599,
                        50,
                        "Home",
                        "Beautiful ceramic mug for your favorite beverage",
                    ),
                    (
                        "Bluetooth Speaker",
                        8999,
                        18,
                        "Electronics",
                        "Portable speaker with amazing sound quality",
                    ),
                    (
                        "Kitchen Knife Set",
                        19999,
                        8,
                        "Home",
                        "Professional chef knife set for cooking enthusiasts",
                    ),
                ]

                cursor.executemany(
                    """
                INSERT INTO products (name, price, stock, category, description)
                VALUES (?, ?, ?, ?, ?)
                """,
                    sample_products,
                )

                print(f"✅ Insertados {len(sample_products)} productos de ejemplo")


# Instancia singleton
_db_connection: Optional[DatabaseConnection] = None


def get_db_connection() -> DatabaseConnection:
    """
    Obtiene la instancia singleton de la conexión a base de datos

    Returns:
        Instancia de DatabaseConnection
    """
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
    return _db_connection


def init_database():
    """Inicializa el schema y datos de ejemplo de la base de datos"""
    db = get_db_connection()
    db.init_schema()
    db.seed_data()
    print("✅ Base de datos inicializada correctamente")
