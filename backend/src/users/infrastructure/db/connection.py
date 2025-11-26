"""
Gestor de Conexión a Base de Datos para Users

Maneja el schema y datos iniciales de la tabla de usuarios.
"""

import sqlite3
from contextlib import contextmanager
from typing import Optional


class UserDatabaseConnection:
    """
    Gestor de Conexión para Users

    Comparte la misma base de datos que Products pero maneja su propio schema.
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
        Inicializa el schema de la tabla users

        Crea la tabla users con todos los constraints necesarios.
        """
        with self.transaction() as conn:
            cursor = conn.cursor()

            # Tabla users
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE CHECK(length(trim(email)) > 0),
                username TEXT NOT NULL UNIQUE CHECK(length(trim(username)) >= 3),
                password_hash TEXT NOT NULL,
                full_name TEXT,
                is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN (0, 1)),
                is_admin INTEGER NOT NULL DEFAULT 0 CHECK(is_admin IN (0, 1)),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Índices para performance
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_email 
            ON users(email)
            """)

            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_username 
            ON users(username)
            """)

            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_active 
            ON users(is_active)
            """)

            # Trigger para updated_at
            cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_user_timestamp 
            AFTER UPDATE ON users
            BEGIN
                UPDATE users SET updated_at = CURRENT_TIMESTAMP 
                WHERE id = NEW.id;
            END
            """)

    def seed_data(self):
        """
        Inserta usuario admin de ejemplo si no existe

        Password por defecto: "admin123"
        """
        with self.transaction() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]

            if count == 0:
                print("👤 Creando usuario administrador por defecto...")

                # Hash de "admin123" con bcrypt
                # En producción esto debería generarse dinámicamente
                import bcrypt

                password_hash = bcrypt.hashpw(
                    "admin123".encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8")

                cursor.execute(
                    """
                INSERT INTO users (email, username, password_hash, full_name, is_admin)
                VALUES (?, ?, ?, ?, 1)
                """,
                    ("admin@example.com", "admin", password_hash, "Administrator"),
                )

                print("✅ Usuario admin creado (username: admin, password: admin123)")


# Instancia singleton
_user_db_connection: Optional[UserDatabaseConnection] = None


def get_user_db_connection() -> UserDatabaseConnection:
    """
    Obtiene la instancia singleton de la conexión

    Returns:
        Instancia de UserDatabaseConnection
    """
    global _user_db_connection
    if _user_db_connection is None:
        _user_db_connection = UserDatabaseConnection()
    return _user_db_connection


def init_user_database():
    """Inicializa el schema y datos de usuarios"""
    db = get_user_db_connection()
    db.init_schema()
    db.seed_data()
    print("✅ Base de datos de usuarios inicializada")
