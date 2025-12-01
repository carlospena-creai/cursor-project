"""
Products API Endpoints - Clean Architecture

✅ Thin controllers (solo presentación)
✅ Delegan lógica a Use Cases
✅ DTOs para request/response
✅ Error handling consistente
"""

from fastapi import APIRouter, HTTPException, Query, status, Depends
from typing import List, Optional

from ...domain.models.product import Product, ProductCreate, ProductUpdate
from ....shared.middleware.auth import get_current_admin_user
from ....users.domain.models.user import User
from ...application import (
    CreateProductUseCase,
    GetProductsUseCase,
    GetProductByIdUseCase,
    UpdateProductUseCase,
    DeleteProductUseCase,
)
from ...executions import (
    get_create_product_use_case,
    get_get_products_use_case,
    get_get_product_by_id_use_case,
    get_update_product_use_case,
    get_delete_product_use_case,
)


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[Product])
async def get_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    search: Optional[str] = Query(None, description="Search in product name"),
    limit: int = Query(20, ge=1, le=100, description="Number of products to return"),
    offset: int = Query(0, ge=0, description="Number of products to skip"),
):
    """
    Get all products with optional filters

    ✅ Thin controller - delega a Use Case
    ✅ Validación con Query parameters
    ✅ Error handling
    """
    try:
        # ✅ Obtener Use Case del DI Container
        use_case: GetProductsUseCase = get_get_products_use_case()

        # ✅ Ejecutar Use Case
        products = await use_case.execute(
            skip=offset,
            limit=limit,
            category=category,
            min_price=min_price,
            max_price=max_price,
            search=search,
            only_active=True,
        )

        return products

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # ✅ Log del error (en producción usar logging apropiado)
        print(f"Error getting products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """
    Get a single product by ID

    ✅ Thin controller
    ✅ Error handling apropiado
    """
    try:
        # ✅ Obtener Use Case del DI Container
        use_case: GetProductByIdUseCase = get_get_product_by_id_use_case()

        # ✅ Ejecutar Use Case
        product = await use_case.execute(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found",
            )

        return product

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error getting product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_admin_user),
):
    """
    Create a new product

    ✅ Pydantic validation automática
    ✅ Thin controller
    ✅ DTO apropiado (ProductCreate)
    ✅ Protected endpoint - requires admin authentication
    """
    try:
        # ✅ Obtener Use Case del DI Container
        use_case: CreateProductUseCase = get_create_product_use_case()

        # ✅ Ejecutar Use Case
        product = await use_case.execute(product_data)

        return product

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error creating product: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating product",
        )


@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_admin_user),
):
    """
    Update an existing product

    ✅ Pydantic validation automática
    ✅ Partial update (PATCH-like)
    ✅ Thin controller
    ✅ Protected endpoint - requires admin authentication
    """
    try:
        # ✅ Obtener Use Case del DI Container
        use_case: UpdateProductUseCase = get_update_product_use_case()

        # ✅ Ejecutar Use Case
        product = await use_case.execute(product_id, product_data)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found",
            )

        return product

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error updating product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating product",
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_admin_user),
):
    """
    Delete a product (soft delete)

    ✅ Soft delete implementado
    ✅ Thin controller
    ✅ HTTP 204 No Content en éxito
    ✅ Protected endpoint - requires admin authentication
    """
    try:
        # ✅ Obtener Use Case del DI Container
        use_case: DeleteProductUseCase = get_delete_product_use_case()

        # ✅ Ejecutar Use Case
        result = await use_case.execute(product_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found",
            )

        return None  # ✅ HTTP 204 No Content

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error deleting product {product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting product",
        )


# ✅ Endpoint adicional útil: Health check
@router.get("/health", include_in_schema=False)
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "module": "products"}
