"""
Modelo de Dominio de Producto - Clean Architecture

Modelo de dominio puro sin dependencias externas.
Encapsula reglas de negocio y validaciones.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
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
        return v.strip()

    @validator("price")
    def validate_price(cls, v):
        """Valida que el precio sea positivo"""
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @validator("stock")
    def validate_stock(cls, v):
        """Valida que el stock sea no negativo"""
        if v < 0:
            raise ValueError("Stock cannot be negative")
        return v

    def can_fulfill_quantity(self, quantity: int) -> bool:
        """
        Business Rule: Verifica si el producto puede cumplir con una cantidad solicitada

        ✅ Encapsula lógica de negocio en el modelo de dominio
        """
        return self.is_active and self.stock >= quantity

    def reduce_stock(self, quantity: int):
        """
        Business Rule: Reduce el stock del producto

        ✅ Encapsula lógica de negocio en el modelo de dominio
        ✅ Valida antes de modificar
        """
        if not self.can_fulfill_quantity(quantity):
            raise ValueError(
                f"Cannot reduce stock by {quantity}. Available: {self.stock}"
            )
        self.stock -= quantity

    class Config:
        json_encoders = {Decimal: lambda v: float(v)}
        use_enum_values = True


class ProductCreate(BaseModel):
    """
    Data Transfer Object para crear un producto

    Contiene solo los campos necesarios para la creación.
    """

    name: str = Field(..., min_length=1, max_length=255)
    price: Decimal = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category: ProductCategory
    description: Optional[str] = Field(None, max_length=2000)
    is_active: bool = Field(default=True)

    @validator("name")
    def validate_name(cls, v):
        """Valida el nombre del producto"""
        if not v or not v.strip():
            raise ValueError("Product name cannot be empty or whitespace")
        return v.strip()

    class Config:
        use_enum_values = True
        json_encoders = {Decimal: lambda v: float(v)}
        schema_extra = {
            "example": {
                "name": "Laptop HP Pavilion",
                "price": 899.99,
                "stock": 50,
                "category": "Electronics",
                "description": "High performance laptop",
                "is_active": True,
            }
        }


class ProductUpdate(BaseModel):
    """
    Data Transfer Object para actualizar un producto

    Todos los campos son opcionales (partial update).
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
        if v is not None and (not v or not v.strip()):
            raise ValueError("Product name cannot be empty or whitespace")
        return v.strip() if v else v

    class Config:
        use_enum_values = True
        json_encoders = {Decimal: lambda v: float(v)}


class ProductsResponse(BaseModel):
    """
    Respuesta paginada de productos con total
    """

    products: List[Product]
    total: int = Field(
        ..., description="Total de productos que coinciden con los filtros"
    )
    limit: int = Field(..., description="Límite de productos por página")
    offset: int = Field(..., description="Offset de la paginación")

    class Config:
        json_encoders = {Decimal: lambda v: float(v)}
