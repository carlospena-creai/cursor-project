"""
Implementación del Repositorio de Productos para SQLite

Implementa la interfaz IProductRepository.
Utiliza prepared statements para prevenir SQL injection.
Maneja transacciones y conversiones de tipos apropiadamente.
"""

from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import sqlite3

from ....domain.interfaces.repositories import IProductRepository
from ....domain.models.product import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductCategory,
)
from ..connection import get_db_connection


class SQLiteProductRepository(IProductRepository):
    """
    Implementación SQLite del Repositorio de Productos

    Implementa la interfaz IProductRepository con SQLite como backend.
    Utiliza prepared statements para seguridad.
    Realiza conversiones de tipos apropiadas (centavos <-> Decimal).
    """

    def __init__(self):
        """Inicializa el repositorio con la conexión a base de datos"""
        self.db = get_db_connection()

    def _row_to_product(self, row: sqlite3.Row) -> Product:
        """
        Convierte una fila de base de datos a modelo de dominio Product

        Realiza la conversión de tipos apropiada:
        - Precio: INTEGER (centavos) -> Decimal (dólares)
        """
        return Product(
            id=row["id"],
            name=row["name"],
            price=Decimal(row["price"]) / 100,  # Centavos a Decimal
            stock=row["stock"],
            category=ProductCategory(row["category"]),
            description=row["description"],
            is_active=bool(row["is_active"]),
            created_at=datetime.fromisoformat(row["created_at"])
            if row["created_at"]
            else None,
            updated_at=datetime.fromisoformat(row["updated_at"])
            if row["updated_at"]
            else None,
        )

    async def create(self, product_data: ProductCreate) -> Product:
        """
        Crea un nuevo producto

        Utiliza prepared statement para seguridad.
        Maneja la transacción automáticamente.
        """
        with self.db.transaction() as conn:
            cursor = conn.cursor()

            # Convertir precio a centavos para almacenamiento
            price_cents = int(product_data.price * 100)

            cursor.execute(
                """
            INSERT INTO products (name, price, stock, category, description, is_active)
            VALUES (?, ?, ?, ?, ?, 1)
            """,
                (
                    product_data.name,
                    price_cents,
                    product_data.stock,
                    product_data.category.value
                    if isinstance(product_data.category, ProductCategory)
                    else product_data.category,
                    product_data.description,
                ),
            )

            product_id = cursor.lastrowid

            # Obtener el producto creado
            cursor.execute(
                """
            SELECT * FROM products WHERE id = ?
            """,
                (product_id,),
            )

            row = cursor.fetchone()
            return self._row_to_product(row)

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por ID

        Utiliza prepared statement.
        Retorna None si no se encuentra.
        """
        with self.db.transaction() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
            SELECT * FROM products WHERE id = ?
            """,
                (product_id,),
            )

            row = cursor.fetchone()
            if row:
                return self._row_to_product(row)
            return None

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        search: Optional[str] = None,
        only_active: Optional[bool] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[Product]:
        """
        Obtiene todos los productos con filtros y ordenamiento

        Construcción dinámica de query de forma segura con prepared statements.
        Soporta paginación, múltiples filtros y ordenamiento dinámico.
        """
        with self.db.transaction() as conn:
            cursor = conn.cursor()

            # Construcción segura de query
            query = "SELECT * FROM products WHERE 1=1"
            params = []

            if only_active is not None:
                query += " AND is_active = ?"
                params.append(1 if only_active else 0)

            if category:
                query += " AND category = ?"
                params.append(category)

            if min_price is not None:
                query += " AND price >= ?"
                params.append(int(min_price * 100))  # Convertir a centavos

            if max_price is not None:
                query += " AND price <= ?"
                params.append(int(max_price * 100))

            if search:
                query += " AND name LIKE ?"
                params.append(f"%{search}%")

            # ✅ Ordenamiento dinámico
            valid_sort_fields = [
                "id",
                "name",
                "price",
                "stock",
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

            return [self._row_to_product(row) for row in rows]

    async def update(
        self, product_id: int, product_data: ProductUpdate
    ) -> Optional[Product]:
        """
        Actualiza un producto existente

        Soporta actualización parcial (solo campos proporcionados).
        Utiliza prepared statements.
        Verifica existencia antes de actualizar.
        """
        # Verificar que existe
        existing = await self.get_by_id(product_id)
        if not existing:
            return None

        with self.db.transaction() as conn:
            cursor = conn.cursor()

            # Construir UPDATE dinámico de forma segura
            update_fields = []
            params = []

            update_dict = product_data.dict(exclude_unset=True)

            if "name" in update_dict and update_dict["name"] is not None:
                update_fields.append("name = ?")
                params.append(update_dict["name"])

            if "price" in update_dict and update_dict["price"] is not None:
                update_fields.append("price = ?")
                params.append(int(update_dict["price"] * 100))  # Convertir a centavos

            if "stock" in update_dict and update_dict["stock"] is not None:
                update_fields.append("stock = ?")
                params.append(update_dict["stock"])

            if "category" in update_dict and update_dict["category"] is not None:
                update_fields.append("category = ?")
                cat_value = update_dict["category"]
                params.append(
                    cat_value.value
                    if isinstance(cat_value, ProductCategory)
                    else cat_value
                )

            if "description" in update_dict:
                update_fields.append("description = ?")
                params.append(update_dict["description"])

            if "is_active" in update_dict and update_dict["is_active"] is not None:
                update_fields.append("is_active = ?")
                params.append(1 if update_dict["is_active"] else 0)

            if not update_fields:
                return existing

            query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = ?"
            params.append(product_id)

            cursor.execute(query, params)

        # Obtener producto actualizado después del commit
        return await self.get_by_id(product_id)

    async def delete(self, product_id: int) -> bool:
        """
        Elimina un producto (soft delete)

        Establece is_active=0 en lugar de eliminar el registro.
        """
        with self.db.transaction() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
            UPDATE products SET is_active = 0 WHERE id = ?
            """,
                (product_id,),
            )

            return cursor.rowcount > 0

    async def exists(self, product_id: int) -> bool:
        """Verifica si un producto existe"""
        product = await self.get_by_id(product_id)
        return product is not None

    async def count(
        self,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        search: Optional[str] = None,
        only_active: Optional[bool] = None,
    ) -> int:
        """
        Cuenta productos con filtros

        Utiliza prepared statements para seguridad.
        Aplica los mismos filtros que get_all para consistencia.
        """
        with self.db.transaction() as conn:
            cursor = conn.cursor()

            query = "SELECT COUNT(*) FROM products WHERE 1=1"
            params = []

            if only_active is not None:
                query += " AND is_active = ?"
                params.append(1 if only_active else 0)

            if category:
                query += " AND category = ?"
                params.append(category)

            if min_price is not None:
                query += " AND price >= ?"
                params.append(int(min_price * 100))  # Convertir a centavos

            if max_price is not None:
                query += " AND price <= ?"
                params.append(int(max_price * 100))

            if search:
                query += " AND name LIKE ?"
                params.append(f"%{search}%")

            cursor.execute(query, params)
            result = cursor.fetchone()

            return result[0] if result else 0
