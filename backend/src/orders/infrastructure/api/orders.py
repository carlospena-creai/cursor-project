"""
Orders API Endpoints - Clean Architecture

✅ Thin controllers (solo presentación)
✅ Delegan lógica a Use Cases
✅ DTOs para request/response
✅ Error handling consistente
"""

from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional

from ...domain.models.order import Order, OrderCreate, OrderUpdate, OrderStatus
from ...application import (
    CreateOrderUseCase,
    GetOrdersUseCase,
    GetOrderByIdUseCase,
    UpdateOrderStatusUseCase,
)
from ...executions import (
    get_create_order_use_case,
    get_get_orders_use_case,
    get_get_order_by_id_use_case,
    get_update_order_status_use_case,
)
from ...infrastructure.db.repositories.order_repository import SQLiteOrderRepository


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=List[Order])
async def get_orders(
    user_id: Optional[int] = Query(None, gt=0, description="Filter by user ID"),
    status: Optional[OrderStatus] = Query(None, description="Filter by status"),
    limit: int = Query(20, ge=1, le=100, description="Number of orders to return"),
    offset: int = Query(0, ge=0, description="Number of orders to skip"),
):
    """
    Get all orders with optional filters

    ✅ Thin controller - delega a Use Case
    ✅ Validación con Query parameters
    ✅ Error handling
    """
    try:
        # ✅ Obtener Use Case del DI Container
        use_case: GetOrdersUseCase = get_get_orders_use_case()

        # ✅ Ejecutar Use Case
        orders = await use_case.execute(
            user_id=user_id,
            status=status,
            skip=offset,
            limit=limit,
        )

        return orders

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # ✅ Log del error (en producción usar logging apropiado)
        print(f"Error getting orders: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: int):
    """
    Get a single order by ID

    ✅ Thin controller
    ✅ Error handling apropiado
    """
    try:
        # ✅ Obtener Use Case del DI Container
        use_case: GetOrderByIdUseCase = get_get_order_by_id_use_case()

        # ✅ Ejecutar Use Case
        order = await use_case.execute(order_id)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {order_id} not found",
            )

        return order

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error getting order {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate):
    """
    Create a new order

    ✅ Pydantic validation automática
    ✅ Thin controller
    ✅ DTO apropiado (OrderCreate)
    ✅ Maneja reducción de stock automáticamente
    """
    try:
        # ✅ Obtener Use Case del DI Container
        use_case: CreateOrderUseCase = get_create_order_use_case()

        # ✅ Ejecutar Use Case
        order = await use_case.execute(order_data)

        return order

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error creating order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating order",
        )


@router.patch("/{order_id}/status", response_model=Order)
async def update_order_status(order_id: int, new_status: OrderStatus):
    """
    Update order status

    ✅ Pydantic validation automática
    ✅ Thin controller
    ✅ Valida transiciones de estado
    """
    try:
        # ✅ Obtener Use Case del DI Container
        use_case: UpdateOrderStatusUseCase = get_update_order_status_use_case()

        # ✅ Ejecutar Use Case
        order = await use_case.execute(order_id, new_status)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {order_id} not found",
            )

        return order

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error updating order status {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating order status",
        )


@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: int, order_data: OrderUpdate):
    """
    Update an existing order

    ✅ Pydantic validation automática
    ✅ Partial update (PATCH-like)
    ✅ Thin controller
    """
    try:
        # Para actualizar estado, usar el endpoint específico
        if order_data.status:
            return await update_order_status(order_id, order_data.status)

        # Para otros campos, usar el repositorio directamente
        repository = SQLiteOrderRepository()
        order = await repository.update(order_id, order_data)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id {order_id} not found",
            )

        return order

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error updating order {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating order",
        )


# ✅ Endpoint adicional útil: Health check
@router.get("/health", include_in_schema=False)
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "module": "orders"}
