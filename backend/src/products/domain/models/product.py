"""
Modelo de Dominio de Producto - Clean Architecture

Modelo de dominio puro sin dependencias externas.
Encapsula reglas de negocio y validaciones.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum


class ProductCategory(str, Enum):
    """Enumeración de categorías de productos para seguridad de tipos"""

    ELECTRONICS = "Electronics"
    HOME = "Home"
    SPORTS = "Sports"
    CLOTHING = "Clothing"
    BOOKS = "Books"
    FOOD = "Food"
    TOYS = "Toys"
    OTHER = "Other"


class Product(BaseModel):
    """
    Modelo de Dominio de Producto

    Utiliza Decimal para precisión monetaria y Enum para categorías type-safe.
    Encapsula reglas de negocio y lógica de dominio.
    """

    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=255)
    price: Decimal = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category: ProductCategory
    description: Optional[str] = Field(None, max_length=2000)
    is_active: bool = Field(default=True)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator("name")
    def validate_name(cls, v):
        """Valida el nombre del producto, rechaza strings vacíos y caracteres prohibidos"""
        if not v or not v.strip():
            raise ValueError("Product name cannot be empty or whitespace")
        forbidden_chars = ["<", ">", "{", "}", "|", "\\", "^", "~", "[", "]", "`"]
        if any(char in v for char in forbidden_chars):
            raise ValueError("Product name contains forbidden characters")
        return v.strip()

    @validator("price")
    def validate_price(cls, v):
        """Valida el rango de precio y máximo 2 decimales"""
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        if v > Decimal("999999.99"):
            raise ValueError("Price exceeds maximum allowed value")
        if v.as_tuple().exponent < -2:
            raise ValueError("Price can have at most 2 decimal places")
        return v

    @validator("stock")
    def validate_stock(cls, v):
        """Valida que el stock esté dentro de rangos aceptables"""
        if v < 0:
            raise ValueError("Stock cannot be negative")
        if v > 1000000:
            raise ValueError("Stock exceeds maximum allowed value")
        return v

    def is_available(self) -> bool:
        """Verifica si el producto está disponible para compra"""
        return self.is_active and self.stock > 0

    def can_fulfill_quantity(self, quantity: int) -> bool:
        """Verifica si se puede cumplir una orden de la cantidad dada"""
        return self.is_active and self.stock >= quantity > 0

    def reduce_stock(self, quantity: int) -> None:
        """Reduce el stock por la cantidad especificada"""
        if not self.can_fulfill_quantity(quantity):
            raise ValueError(
                f"Cannot reduce stock by {quantity}. Available: {self.stock}"
            )
        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """Incrementa el stock por la cantidad especificada"""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.stock += quantity

    def deactivate(self) -> None:
        """Desactiva el producto (soft delete)"""
        self.is_active = False

    def activate(self) -> None:
        """Activa el producto"""
        self.is_active = True

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None,
            Decimal: lambda v: float(v),
        }
        use_enum_values = True


class ProductCreate(BaseModel):
    """
    Data Transfer Object para crear un producto.
    Contiene solo los campos necesarios para la creación.
    """

    name: str = Field(..., min_length=1, max_length=255)
    price: Decimal = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category: ProductCategory
    description: Optional[str] = Field(None, max_length=2000)

    @validator("name")
    def validate_name(cls, v):
        """Valida el nombre del producto"""
        if not v or not v.strip():
            raise ValueError("Product name cannot be empty")
        forbidden_chars = ["<", ">", "{", "}", "|", "\\", "^", "~", "[", "]", "`"]
        if any(char in v for char in forbidden_chars):
            raise ValueError("Product name contains forbidden characters")
        return v.strip()

    @validator("price")
    def validate_price(cls, v):
        """Valida precio con máximo 2 decimales"""
        if v.as_tuple().exponent < -2:
            raise ValueError("Price can have at most 2 decimal places")
        return v

    class Config:
        use_enum_values = True


class ProductUpdate(BaseModel):
    """
    Data Transfer Object para actualizar un producto.
    Todos los campos son opcionales para soportar actualizaciones parciales.
    """

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[Decimal] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[ProductCategory] = None
    description: Optional[str] = Field(None, max_length=2000)
    is_active: Optional[bool] = None

    @validator("name")
    def validate_name(cls, v):
        """Valida el nombre del producto si se proporciona"""
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Product name cannot be empty")
            forbidden_chars = ["<", ">", "{", "}", "|", "\\", "^", "~", "[", "]", "`"]
            if any(char in v for char in forbidden_chars):
                raise ValueError("Product name contains forbidden characters")
            return v.strip()
        return v

    @validator("price")
    def validate_price(cls, v):
        """Valida precio con máximo 2 decimales si se proporciona"""
        if v is not None and v.as_tuple().exponent < -2:
            raise ValueError("Price can have at most 2 decimal places")
        return v

    class Config:
        use_enum_values = True
