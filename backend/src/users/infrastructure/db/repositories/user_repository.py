"""
Implementación SQLite del Repositorio de Usuarios

Utiliza prepared statements y maneja la persistencia de usuarios.
"""

from typing import Optional, List
from datetime import datetime
import sqlite3

from ....domain.interfaces.repositories import IUserRepository
from ....domain.models.user import User, UserCreate, UserUpdate
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

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        is_admin: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[User]:
        """
        Obtiene todos los usuarios con filtros y ordenamiento

        Construcción dinámica de query de forma segura con prepared statements.
        Soporta paginación, múltiples filtros y ordenamiento dinámico.
        """
        with self.db.transaction() as conn:
            cursor = conn.cursor()

            # Construcción segura de query
            query = "SELECT * FROM users WHERE 1=1"
            params = []

            if is_active is not None:
                query += " AND is_active = ?"
                params.append(1 if is_active else 0)

            if is_admin is not None:
                query += " AND is_admin = ?"
                params.append(1 if is_admin else 0)

            if search:
                query += " AND (email LIKE ? OR username LIKE ? OR full_name LIKE ?)"
                search_pattern = f"%{search}%"
                params.extend([search_pattern, search_pattern, search_pattern])

            # ✅ Ordenamiento dinámico
            valid_sort_fields = [
                "id",
                "email",
                "username",
                "full_name",
                "created_at",
                "updated_at",
            ]
            if sort_by and sort_by in valid_sort_fields:
                order = "ASC" if sort_order == "asc" else "DESC"
                query += f" ORDER BY {sort_by} {order}"
            else:
                # Ordenamiento por defecto
                query += " ORDER BY created_at DESC"

            query += " LIMIT ? OFFSET ?"
            params.extend([limit, skip])

            cursor.execute(query, params)
            rows = cursor.fetchall()

            return [self._row_to_user(row) for row in rows]

    async def count(
        self,
        is_active: Optional[bool] = None,
        is_admin: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> int:
        """
        Cuenta usuarios con filtros opcionales

        Utiliza prepared statements para seguridad.
        Aplica los mismos filtros que get_all para consistencia.
        """
        with self.db.transaction() as conn:
            cursor = conn.cursor()

            query = "SELECT COUNT(*) FROM users WHERE 1=1"
            params = []

            if is_active is not None:
                query += " AND is_active = ?"
                params.append(1 if is_active else 0)

            if is_admin is not None:
                query += " AND is_admin = ?"
                params.append(1 if is_admin else 0)

            if search:
                query += " AND (email LIKE ? OR username LIKE ? OR full_name LIKE ?)"
                search_pattern = f"%{search}%"
                params.extend([search_pattern, search_pattern, search_pattern])

            cursor.execute(query, params)
            result = cursor.fetchone()

            return result[0] if result else 0

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Actualiza un usuario existente

        Soporta actualización parcial (solo campos proporcionados).
        Utiliza prepared statements.
        Verifica existencia antes de actualizar.
        """
        # Verificar que existe
        existing = await self.get_by_id(user_id)
        if not existing:
            return None

        with self.db.transaction() as conn:
            cursor = conn.cursor()

            # Construir UPDATE dinámico de forma segura
            update_fields = []
            params = []

            update_dict = user_data.dict(exclude_unset=True)

            if "email" in update_dict and update_dict["email"] is not None:
                update_fields.append("email = ?")
                params.append(update_dict["email"].lower())

            if "username" in update_dict and update_dict["username"] is not None:
                update_fields.append("username = ?")
                params.append(update_dict["username"].lower())

            if "full_name" in update_dict:
                update_fields.append("full_name = ?")
                params.append(update_dict["full_name"])

            if "is_active" in update_dict and update_dict["is_active"] is not None:
                update_fields.append("is_active = ?")
                params.append(1 if update_dict["is_active"] else 0)

            if "is_admin" in update_dict and update_dict["is_admin"] is not None:
                update_fields.append("is_admin = ?")
                params.append(1 if update_dict["is_admin"] else 0)

            if not update_fields:
                return existing

            # ✅ Actualizar updated_at cuando se modifica cualquier campo
            update_fields.append("updated_at = ?")
            params.append(datetime.now().isoformat())

            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
            params.append(user_id)

            cursor.execute(query, params)

        # Obtener usuario actualizado después del commit
        return await self.get_by_id(user_id)
