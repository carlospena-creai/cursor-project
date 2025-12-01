"""
Implementación del Repositorio de Órdenes para SQLite

Implementa la interfaz IOrderRepository.
Utiliza prepared statements para prevenir SQL injection.
Maneja transacciones y conversiones de tipos apropiadamente.
"""

from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import sqlite3

from ....domain.interfaces.repositories import IOrderRepository
from ....domain.models.order import (
    Order,
    OrderCreate,
    OrderUpdate,
    OrderStatus,
    OrderItem,
)
from ..connection import get_order_db_connection
from src.products.executions import get_product_repository


class SQLiteOrderRepository(IOrderRepository):
    """
    Implementación SQLite del Repositorio de Órdenes

    Implementa la interfaz IOrderRepository con SQLite como backend.
    Utiliza prepared statements para seguridad.
    Realiza conversiones de tipos apropiadas (centavos <-> Decimal).
    """

    def __init__(self):
        """Inicializa el repositorio con la conexión a base de datos"""
        self.db = get_order_db_connection()

    def _row_to_order_item(self, row: sqlite3.Row) -> OrderItem:
        """Convierte una fila de order_items a OrderItem"""
        return OrderItem(
            id=row["id"],
            product_id=row["product_id"],
            product_name=row["product_name"],
            quantity=row["quantity"],
            unit_price=Decimal(row["unit_price"]) / 100,  # Centavos a Decimal
            subtotal=Decimal(row["subtotal"]) / 100,  # Centavos a Decimal
        )

    def _row_to_order(self, order_row: sqlite3.Row, items: List[OrderItem]) -> Order:
        """Convierte filas de BD a modelo de dominio Order"""
        return Order(
            id=order_row["id"],
            user_id=order_row["user_id"],
            items=items,
            status=OrderStatus(order_row["status"]),
            total=Decimal(order_row["total"]) / 100,  # Centavos a Decimal
            shipping_address=order_row["shipping_address"],
            notes=order_row["notes"],
            created_at=datetime.fromisoformat(order_row["created_at"])
            if order_row["created_at"]
            else None,
            updated_at=datetime.fromisoformat(order_row["updated_at"])
            if order_row["updated_at"]
            else None,
        )

    async def create(self, order_data: OrderCreate) -> Order:
        """
        Crea una nueva orden

        Utiliza prepared statement para seguridad.
        Maneja la transacción automáticamente.
        Requiere que los productos existan para obtener precios y nombres.
        """
        # Necesitamos obtener los productos para construir los OrderItems completos
        product_repo = get_product_repository()

        with self.db.transaction() as conn:
            cursor = conn.cursor()

            # Construir OrderItems completos
            order_items = []
            total_cents = 0

            for item in order_data.items:
                product_id = item.product_id
                quantity = item.quantity

                # Obtener producto para precio y nombre
                product = await product_repo.get_by_id(product_id)
                if not product:
                    raise ValueError(f"Product with id {product_id} not found")

                unit_price_cents = int(product.price * 100)
                subtotal_cents = unit_price_cents * quantity
                total_cents += subtotal_cents

                # Crear OrderItem
                order_item = OrderItem(
                    product_id=product_id,
                    product_name=product.name,
                    quantity=quantity,
                    unit_price=product.price,
                    subtotal=product.price * Decimal(quantity),
                )
                order_items.append(order_item)

            # Insertar orden
            cursor.execute(
                """
            INSERT INTO orders (user_id, status, total, shipping_address, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
                (
                    order_data.user_id,
                    "pending",
                    total_cents,
                    order_data.shipping_address,
                    order_data.notes,
                ),
            )

            order_id = cursor.lastrowid

            # Insertar order_items
            for item in order_items:
                cursor.execute(
                    """
                INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price, subtotal)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        order_id,
                        item.product_id,
                        item.product_name,
                        item.quantity,
                        int(item.unit_price * 100),  # Convertir a centavos
                        int(item.subtotal * 100),  # Convertir a centavos
                    ),
                )

            # Obtener la orden creada
            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            order_row = cursor.fetchone()

            # Obtener items
            cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
            item_rows = cursor.fetchall()
            items = [self._row_to_order_item(row) for row in item_rows]

            return self._row_to_order(order_row, items)

    async def get_by_id(self, order_id: int) -> Optional[Order]:
        """
        Obtiene una orden por ID

        Utiliza prepared statement.
        Retorna None si no se encuentra.
        """
        with self.db.transaction() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            order_row = cursor.fetchone()

            if not order_row:
                return None

            # Obtener items
            cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
            item_rows = cursor.fetchall()
            items = [self._row_to_order_item(row) for row in item_rows]

            return self._row_to_order(order_row, items)

    async def get_all(
        self,
        user_id: Optional[int] = None,
        status: Optional[OrderStatus] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Order]:
        """
        Obtiene todas las órdenes con filtros

        Construcción dinámica de query de forma segura con prepared statements.
        Soporta paginación y múltiples filtros.
        """
        with self.db.transaction() as conn:
            cursor = conn.cursor()

            # Construcción segura de query
            query = "SELECT * FROM orders WHERE 1=1"
            params = []

            if user_id:
                query += " AND user_id = ?"
                params.append(user_id)

            if status:
                query += " AND status = ?"
                params.append(status.value)

            query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, skip])

            cursor.execute(query, params)
            order_rows = cursor.fetchall()

            orders = []
            for order_row in order_rows:
                order_id = order_row["id"]
                cursor.execute(
                    "SELECT * FROM order_items WHERE order_id = ?", (order_id,)
                )
                item_rows = cursor.fetchall()
                items = [self._row_to_order_item(row) for row in item_rows]
                orders.append(self._row_to_order(order_row, items))

            return orders

    async def update(self, order_id: int, order_data: OrderUpdate) -> Optional[Order]:
        """
        Actualiza una orden existente

        Soporta actualización parcial (solo campos proporcionados).
        Utiliza prepared statements.
        Verifica existencia antes de actualizar.
        """
        # Verificar que existe
        existing = await self.get_by_id(order_id)
        if not existing:
            return None

        with self.db.transaction() as conn:
            cursor = conn.cursor()

            # Construir UPDATE dinámico de forma segura
            update_fields = []
            params = []

            update_dict = order_data.dict(exclude_unset=True)

            if "status" in update_dict and update_dict["status"] is not None:
                update_fields.append("status = ?")
                status_value = update_dict["status"]
                params.append(
                    status_value.value
                    if isinstance(status_value, OrderStatus)
                    else status_value
                )

            if "shipping_address" in update_dict:
                update_fields.append("shipping_address = ?")
                params.append(update_dict["shipping_address"])

            if "notes" in update_dict:
                update_fields.append("notes = ?")
                params.append(update_dict["notes"])

            if not update_fields:
                return existing

            query = f"UPDATE orders SET {', '.join(update_fields)} WHERE id = ?"
            params.append(order_id)

            cursor.execute(query, params)

        # Obtener orden actualizada después del commit
        return await self.get_by_id(order_id)

    async def update_status(
        self, order_id: int, new_status: OrderStatus
    ) -> Optional[Order]:
        """
        Actualiza el estado de una orden

        Método especializado para actualizar solo el estado.
        """
        order_update = OrderUpdate(status=new_status)
        return await self.update(order_id, order_update)

    async def exists(self, order_id: int) -> bool:
        """Verifica si una orden existe"""
        order = await self.get_by_id(order_id)
        return order is not None

    async def count(
        self, user_id: Optional[int] = None, status: Optional[OrderStatus] = None
    ) -> int:
        """
        Cuenta órdenes con filtros opcionales

        Utiliza prepared statements para seguridad.
        """
        with self.db.transaction() as conn:
            cursor = conn.cursor()

            query = "SELECT COUNT(*) FROM orders WHERE 1=1"
            params = []

            if user_id:
                query += " AND user_id = ?"
                params.append(user_id)

            if status:
                query += " AND status = ?"
                params.append(status.value)

            cursor.execute(query, params)
            result = cursor.fetchone()

            return result[0] if result else 0
