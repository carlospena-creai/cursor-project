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
            raise ValueError("Quantity exceeds maximum allowed value (1000)")
        return v

    class Config:
        schema_extra = {"example": {"product_id": 1, "quantity": 2}}


class OrderItem(BaseModel):
    """
    Item de una orden

    Representa un producto y su cantidad en una orden.
    Incluye el precio al momento de la compra (snapshot).
    """

    id: Optional[int] = None
    product_id: int = Field(..., gt=0)
    product_name: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., gt=0)
    subtotal: Decimal = Field(..., gt=0)

    @validator("quantity")
    def validate_quantity(cls, v):
        """Valida que la cantidad sea positiva y razonable"""
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        if v > 1000:
            raise ValueError("Quantity exceeds maximum allowed value (1000)")
        return v

    @validator("unit_price")
    def validate_unit_price(cls, v):
        """Valida el precio unitario"""
        if v <= 0:
            raise ValueError("Unit price must be greater than 0")
        if v > Decimal("999999.99"):
            raise ValueError("Unit price exceeds maximum allowed value")
        return v

    def calculate_subtotal(self) -> Decimal:
        """Calcula el subtotal del item"""
        return self.unit_price * Decimal(self.quantity)

    class Config:
        json_encoders = {Decimal: lambda v: float(v)}


class Order(BaseModel):
    """
    Modelo de Dominio de Orden

    Representa una orden de compra con sus items y estado.
    Encapsula reglas de negocio y validaciones.
    """

    id: Optional[int] = None
    user_id: int = Field(..., gt=0)
    items: List[OrderItem] = Field(..., min_items=1)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    total: Decimal = Field(..., gt=0)
    shipping_address: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=1000)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator("items")
    def validate_items(cls, v):
        """Valida que haya al menos un item"""
        if not v or len(v) == 0:
            raise ValueError("Order must have at least one item")
        return v

    @validator("total")
    def validate_total(cls, v):
        """Valida que el total sea positivo"""
        if v <= 0:
            raise ValueError("Total must be greater than 0")
        return v

    def calculate_total(self) -> Decimal:
        """Calcula el total de la orden sumando los subtotales de los items"""
        return sum(item.calculate_subtotal() for item in self.items)

    def can_be_cancelled(self) -> bool:
        """Verifica si la orden puede ser cancelada"""
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]

    def can_be_updated(self) -> bool:
        """Verifica si la orden puede ser actualizada"""
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]

    def is_completed(self) -> bool:
        """Verifica si la orden está completada"""
        return self.status == OrderStatus.DELIVERED

    def is_cancelled(self) -> bool:
        """Verifica si la orden está cancelada"""
        return self.status == OrderStatus.CANCELLED

    def update_status(self, new_status: OrderStatus) -> None:
        """Actualiza el estado de la orden con validación"""
        # Reglas de negocio: transiciones de estado válidas
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [
                OrderStatus.PROCESSING,
                OrderStatus.CANCELLED,
            ],
            OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
            OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
            OrderStatus.DELIVERED: [],  # Estado final
            OrderStatus.CANCELLED: [],  # Estado final
        }

        if new_status not in valid_transitions.get(self.status, []):
            raise ValueError(f"Cannot transition from {self.status} to {new_status}")

        self.status = new_status

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None,
            Decimal: lambda v: float(v),
        }
        use_enum_values = True


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

    Solo permite actualizar el estado y campos opcionales.
    """

    status: Optional[OrderStatus] = None
    shipping_address: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=1000)

    class Config:
        use_enum_values = True
