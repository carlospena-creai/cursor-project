"""
Order Domain Model - Clean Architecture

Modelo de dominio puro para órdenes.
Incluye validaciones y reglas de negocio.
Maneja relaciones con Product y User.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum


class OrderStatus(str, Enum):
    """Estados posibles de una orden"""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItemCreate(BaseModel):
    """
    Item para crear una orden

    Representa un producto y su cantidad al momento de crear una orden.
    Solo contiene los datos mínimos necesarios (product_id y quantity).
    """

    product_id: int = Field(..., gt=0, description="ID del producto a ordenar")
    quantity: int = Field(..., gt=0, description="Cantidad del producto")

    @validator("product_id")
    def validate_product_id(cls, v):
        """Valida que el product_id sea positivo"""
        if v <= 0:
            raise ValueError("product_id must be a positive integer")
        return v

    @validator("quantity")
    def validate_quantity(cls, v):
        """Valida que la cantidad sea positiva y razonable"""
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        if v > 1000:
            raise ValueError("Quantity cannot exceed 1000")
        return v


class OrderItem(BaseModel):
    """
    Item de una orden

    Representa un producto en una orden con su información snapshot.
    """

    id: Optional[int] = None
    product_id: int = Field(..., description="ID del producto")
    product_name: str = Field(..., description="Nombre del producto (snapshot)")
    quantity: int = Field(..., gt=0, description="Cantidad ordenada")
    unit_price: Decimal = Field(
        ..., gt=0, description="Precio unitario al momento de la orden"
    )
    subtotal: Decimal = Field(
        ..., gt=0, description="Subtotal del item (quantity * unit_price)"
    )

    @validator("quantity")
    def validate_quantity(cls, v):
        """Valida que la cantidad sea positiva"""
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v

    class Config:
        json_encoders = {Decimal: lambda v: float(v)}


class Order(BaseModel):
    """
    Modelo de Dominio de Orden

    Encapsula reglas de negocio y validaciones.
    """

    id: Optional[int] = None
    user_id: int = Field(..., gt=0, description="ID del usuario que creó la orden")
    items: List[OrderItem] = Field(..., min_items=1, description="Items de la orden")
    status: OrderStatus = Field(
        default=OrderStatus.PENDING, description="Estado de la orden"
    )
    total: Decimal = Field(..., gt=0, description="Total de la orden")
    shipping_address: Optional[str] = Field(
        None, max_length=500, description="Dirección de envío"
    )
    notes: Optional[str] = Field(None, max_length=1000, description="Notas adicionales")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator("items")
    def validate_items(cls, v):
        """Valida que haya al menos un item"""
        if not v or len(v) == 0:
            raise ValueError("Order must have at least one item")
        return v

    @validator("total")
    def validate_total(cls, v, values):
        """Valida que el total coincida con la suma de los items"""
        if "items" in values:
            calculated_total = sum(item.subtotal for item in values["items"])
            if abs(calculated_total - v) > Decimal("0.01"):
                raise ValueError(
                    f"Total {v} does not match sum of items {calculated_total}"
                )
        return v

    def can_transition_to(self, new_status: OrderStatus) -> bool:
        """
        Business Rule: Verifica si la transición de estado es válida

        ✅ Encapsula lógica de negocio en el modelo de dominio
        """
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
            OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
            OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
            OrderStatus.DELIVERED: [],  # Estado final
            OrderStatus.CANCELLED: [],  # Estado final
        }

        return new_status in valid_transitions.get(self.status, [])

    class Config:
        use_enum_values = True
        json_encoders = {Decimal: lambda v: float(v)}


class OrderCreate(BaseModel):
    """
    Data Transfer Object para crear una orden

    Contiene solo los campos necesarios para la creación.
    Los items deben incluir product_id y quantity.
    El user_id se obtiene automáticamente del usuario autenticado (opcional en request).
    """

    user_id: Optional[int] = Field(
        None,
        gt=0,
        description="ID del usuario (se obtiene del token JWT si no se proporciona)",
    )
    items: List[OrderItemCreate] = Field(
        ..., min_items=1, description="Lista de items de la orden"
    )
    shipping_address: Optional[str] = Field(
        None, max_length=500, description="Dirección de envío"
    )
    notes: Optional[str] = Field(
        None, max_length=1000, description="Notas adicionales para la orden"
    )

    @validator("items")
    def validate_items(cls, v):
        """Valida que haya al menos un item"""
        if not v or len(v) == 0:
            raise ValueError("Order must have at least one item")
        return v

    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "items": [
                    {"product_id": 1, "quantity": 2},
                    {"product_id": 3, "quantity": 1},
                ],
                "shipping_address": "123 Main St, City",
                "notes": "Please deliver in the morning",
            }
        }


class OrderUpdate(BaseModel):
    """
    Data Transfer Object para actualizar una orden

    Todos los campos son opcionales (partial update).
    """

    status: Optional[OrderStatus] = Field(
        None, description="Estado de la orden"
    )
    shipping_address: Optional[str] = Field(
        None, max_length=500, description="Dirección de envío"
    )
    notes: Optional[str] = Field(None, max_length=1000, description="Notas adicionales")

    class Config:
        use_enum_values = True


class OrdersResponse(BaseModel):
    """
    Respuesta paginada de órdenes con total
    """

    orders: List[Order]
    total: int = Field(
        ..., description="Total de órdenes que coinciden con los filtros"
    )
    limit: int = Field(..., description="Límite de órdenes por página")
    offset: int = Field(..., description="Offset de la paginación")

    class Config:
        json_encoders = {Decimal: lambda v: float(v)}
        use_enum_values = True
