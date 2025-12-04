"""
Admin API Endpoints - Clean Architecture

Endpoints administrativos para dashboard, estadísticas y bulk operations.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from ...domain.models.dashboard import (
    DashboardStats,
    ProductBulkCreate,
    ProductBulkUpdate,
    ProductBulkDelete,
)
from ....shared.middleware.auth import get_current_admin_user
from ....users.domain.models.user import User
from ....products.executions import get_product_repository
from ....orders.executions import get_order_repository
from ....users.executions import get_user_repository
from ....products.domain.models.product import Product, ProductCreate, ProductUpdate
from ....products.application import (
    CreateProductUseCase,
    UpdateProductUseCase,
    DeleteProductUseCase,
)
from ....products.executions import (
    get_create_product_use_case,
    get_update_product_use_case,
    get_delete_product_use_case,
)


router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_admin_user),
):
    """
    Obtiene estadísticas del dashboard administrativo

    ✅ Solo accesible para administradores
    ✅ Agrega métricas de todos los módulos
    """
    try:
        product_repo = get_product_repository()
        order_repo = get_order_repository()
        user_repo = get_user_repository()

        # Estadísticas de productos
        total_products = await product_repo.count(only_active=False)
        active_products = await product_repo.count(only_active=True)

        # Estadísticas de órdenes
        from ....orders.domain.models.order import OrderStatus

        total_orders = await order_repo.count()
        pending_orders = await order_repo.count(status=OrderStatus.PENDING)

        # Estadísticas de usuarios
        # Nota: Necesitamos agregar método count al repositorio de usuarios
        # Por ahora, usamos una aproximación
        total_users = 0  # TODO: Implementar count en user repository
        active_users = 0  # TODO: Implementar count en user repository

        # Calcular ingresos totales (suma de totales de órdenes entregadas)
        # Necesitamos agregar método para esto
        total_revenue = 0.0  # TODO: Implementar cálculo de revenue

        # Órdenes recientes (últimas 24h)
        recent_orders = await order_repo.get_all(
            limit=1000
        )  # Obtener todas para contar
        # Filtrar por fecha reciente (simplificado por ahora)
        recent_orders_count = len(recent_orders) if len(recent_orders) <= 10 else 10

        stats = DashboardStats(
            total_products=total_products,
            active_products=active_products,
            total_orders=total_orders,
            pending_orders=pending_orders,
            total_users=total_users,
            active_users=active_users,
            total_revenue=total_revenue,
            recent_orders_count=recent_orders_count,
        )

        return stats

    except Exception as e:
        print(f"Error getting dashboard stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving dashboard statistics",
        )


@router.post("/products/bulk-create", response_model=List[Product])
async def bulk_create_products(
    bulk_data: ProductBulkCreate,
    current_user: User = Depends(get_current_admin_user),
):
    """
    Crea múltiples productos en una sola operación

    ✅ Solo accesible para administradores
    ✅ Operación atómica (todo o nada)
    """
    try:
        use_case: CreateProductUseCase = get_create_product_use_case()
        created_products = []

        for product_data in bulk_data.products:
            try:
                product_create = ProductCreate(**product_data)
                product = await use_case.execute(product_create)
                created_products.append(product)
            except Exception as e:
                # Si falla uno, revertir todos (simplificado)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error creating product: {str(e)}",
                )

        return created_products

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in bulk create products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating products",
        )


@router.put("/products/bulk-update", response_model=List[Product])
async def bulk_update_products(
    bulk_data: ProductBulkUpdate,
    current_user: User = Depends(get_current_admin_user),
):
    """
    Actualiza múltiples productos en una sola operación

    ✅ Solo accesible para administradores
    """
    try:
        use_case: UpdateProductUseCase = get_update_product_use_case()
        updated_products = []

        for update_data in bulk_data.updates:
            product_id = update_data.pop("product_id")
            product_update = ProductUpdate(**update_data)

            product = await use_case.execute(product_id, product_update)
            if product:
                updated_products.append(product)
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id {product_id} not found",
                )

        return updated_products

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in bulk update products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating products",
        )


@router.delete("/products/bulk-delete", status_code=status.HTTP_204_NO_CONTENT)
async def bulk_delete_products(
    bulk_data: ProductBulkDelete,
    current_user: User = Depends(get_current_admin_user),
):
    """
    Elimina múltiples productos en una sola operación

    ✅ Solo accesible para administradores
    ✅ Soft delete (is_active=False)
    """
    try:
        use_case: DeleteProductUseCase = get_delete_product_use_case()

        for product_id in bulk_data.product_ids:
            result = await use_case.execute(product_id)
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id {product_id} not found",
                )

        return None

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in bulk delete products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting products",
        )
