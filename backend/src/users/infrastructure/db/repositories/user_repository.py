"""
Implementación SQLite del Repositorio de Usuarios

Utiliza prepared statements y maneja la persistencia de usuarios.
"""

from typing import Optional
from datetime import datetime
import sqlite3

from ....domain.interfaces.repositories import IUserRepository
from ....domain.models.user import User, UserCreate
from ..connection import get_user_db_connection


class SQLiteUserRepository(IUserRepository):
    """
    Implementación SQLite del Repositorio de Usuarios

    Maneja todas las operaciones CRUD de usuarios con seguridad.
    """

    def __init__(self):
        """Inicializa el repositorio"""
        self.db = get_user_db_connection()

    def _row_to_user(self, row: sqlite3.Row) -> User:
        """Convierte una fila de BD a modelo de dominio User"""
        return User(
            id=row["id"],
            email=row["email"],
            username=row["username"],
            full_name=row["full_name"],
            is_active=bool(row["is_active"]),
            is_admin=bool(row["is_admin"]),
            created_at=datetime.fromisoformat(row["created_at"])
            if row["created_at"]
            else None,
            updated_at=datetime.fromisoformat(row["updated_at"])
            if row["updated_at"]
            else None,
        )

    async def create(self, user_data: UserCreate, hashed_password: str) -> User:
        """Crea un nuevo usuario"""
        with self.db.transaction() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
            INSERT INTO users (email, username, password_hash, full_name, is_active, is_admin)
            VALUES (?, ?, ?, ?, 1, 0)
            """,
                (
                    user_data.email.lower(),
                    user_data.username.lower(),
                    hashed_password,
                    user_data.full_name,
                ),
            )

            user_id = cursor.lastrowid

            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return self._row_to_user(row)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene usuario por ID"""
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return self._row_to_user(row) if row else None

    async def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene usuario por email"""
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email.lower(),))
            row = cursor.fetchone()
            return self._row_to_user(row) if row else None

    async def get_by_username(self, username: str) -> Optional[User]:
        """Obtiene usuario por username"""
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ?", (username.lower(),)
            )
            row = cursor.fetchone()
            return self._row_to_user(row) if row else None

    async def get_password_hash(self, user_id: int) -> Optional[str]:
        """Obtiene el hash del password"""
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return row["password_hash"] if row else None

    async def email_exists(self, email: str) -> bool:
        """Verifica si un email existe"""
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM users WHERE email = ?", (email.lower(),))
            return cursor.fetchone() is not None

    async def username_exists(self, username: str) -> bool:
        """Verifica si un username existe"""
        with self.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM users WHERE username = ?", (username.lower(),)
            )
            return cursor.fetchone() is not None
