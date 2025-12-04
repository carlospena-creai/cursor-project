"""
Admin Dashboard Models

Modelos de dominio para el dashboard administrativo.
"""

from pydantic import BaseModel, Field
from typing import List
from decimal import Decimal


class DashboardStats(BaseModel):
    """
    Estadísticas del dashboard administrativo
    """

    total_products: int = Field(..., description="Total de productos")
    active_products: int = Field(..., description="Productos activos")
    total_orders: int = Field(..., description="Total de órdenes")
    pending_orders: int = Field(..., description="Órdenes pendientes")
    total_users: int = Field(..., description="Total de usuarios")
    active_users: int = Field(..., description="Usuarios activos")
    total_revenue: Decimal = Field(..., description="Ingresos totales")
    recent_orders_count: int = Field(
        default=0, description="Órdenes recientes (últimas 24h)"
    )

    class Config:
        json_encoders = {Decimal: lambda v: float(v)}


class ProductBulkCreate(BaseModel):
    """
    Modelo para crear múltiples productos
    """

    products: List[dict] = Field(
        ..., min_items=1, description="Lista de productos a crear"
    )

    class Config:
        schema_extra = {
            "example": {
                "products": [
                    {
                        "name": "Product 1",
                        "description": "Description 1",
                        "price": 10.99,
                        "stock": 100,
                        "category": "Electronics",
                    },
                    {
                        "name": "Product 2",
                        "description": "Description 2",
                        "price": 20.99,
                        "stock": 50,
                        "category": "Clothing",
                    },
                ]
            }
        }


class ProductBulkUpdate(BaseModel):
    """
    Modelo para actualizar múltiples productos
    """

    updates: List[dict] = Field(
        ..., min_items=1, description="Lista de actualizaciones"
    )

    class Config:
        schema_extra = {
            "example": {
                "updates": [
                    {"product_id": 1, "price": 15.99, "stock": 120},
                    {"product_id": 2, "price": 25.99, "stock": 60},
                ]
            }
        }


class ProductBulkDelete(BaseModel):
    """
    Modelo para eliminar múltiples productos
    """

    product_ids: List[int] = Field(
        ..., min_items=1, description="IDs de productos a eliminar"
    )

    class Config:
        schema_extra = {"example": {"product_ids": [1, 2, 3]}}
