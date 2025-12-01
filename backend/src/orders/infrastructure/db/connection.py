"""
Gestor de Conexión a Base de Datos para Orders

Maneja el schema y datos iniciales de las tablas de órdenes.
"""

import sqlite3
from contextlib import contextmanager
from typing import Optional


class OrderDatabaseConnection:
    """
    Gestor de Conexión para Orders

    Comparte la misma base de datos que Products y Users pero maneja su propio schema.
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
        Inicializa el schema de las tablas orders y order_items

        Crea las tablas con todos los constraints necesarios.
        Maneja relaciones con users y products.
        """
        with self.transaction() as conn:
            cursor = conn.cursor()

            # Tabla orders
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending' 
                    CHECK(status IN ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled')),
                total INTEGER NOT NULL CHECK(total > 0),
                shipping_address TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT
            )
            """)

            # Tabla order_items
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL CHECK(length(trim(product_name)) > 0),
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                unit_price INTEGER NOT NULL CHECK(unit_price > 0),
                subtotal INTEGER NOT NULL CHECK(subtotal > 0),
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
            )
            """)

            # Índices para performance
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_orders_user_id 
            ON orders(user_id)
            """)

            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_orders_status 
            ON orders(status)
            """)

            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_orders_created_at 
            ON orders(created_at)
            """)

            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_order_items_order_id 
            ON order_items(order_id)
            """)

            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_order_items_product_id 
            ON order_items(product_id)
            """)

            # Trigger para updated_at
            cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_order_timestamp 
            AFTER UPDATE ON orders
            BEGIN
                UPDATE orders SET updated_at = CURRENT_TIMESTAMP 
                WHERE id = NEW.id;
            END
            """)


# Instancia singleton
_order_db_connection: Optional[OrderDatabaseConnection] = None


def get_order_db_connection() -> OrderDatabaseConnection:
    """
    Obtiene la instancia singleton de la conexión

    Returns:
        Instancia de OrderDatabaseConnection
    """
    global _order_db_connection
    if _order_db_connection is None:
        _order_db_connection = OrderDatabaseConnection()
    return _order_db_connection


def init_order_database():
    """Inicializa el schema de órdenes"""
    db = get_order_db_connection()
    db.init_schema()
    print("✅ Base de datos de órdenes inicializada")
