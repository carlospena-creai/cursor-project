"""
Users Admin API Endpoints

Endpoints administrativos para gestión de usuarios.
Solo accesibles para administradores.
"""

from fastapi import APIRouter, HTTPException, Query, status, Depends
from typing import Optional

from ...domain.models.user import User, UserResponse, UserUpdate, UsersResponse
from ...executions import (
    get_get_users_use_case,
    get_update_user_use_case,
)
from ....shared.middleware.auth import get_current_admin_user


router = APIRouter(prefix="/admin/users", tags=["Admin - Users"])


@router.get("/", response_model=UsersResponse)
async def get_users(
    current_user: User = Depends(get_current_admin_user),
    is_active: Optional[bool] = Query(
        None,
        description="Filter by active status (True=active, False=inactive, None=all)",
    ),
    is_admin: Optional[bool] = Query(
        None, description="Filter by admin role (True=admins, False=regular, None=all)"
    ),
    search: Optional[str] = Query(
        None, description="Search in email, username or full_name"
    ),
    limit: int = Query(20, ge=1, le=100, description="Number of users to return"),
    offset: int = Query(0, ge=0, description="Number of users to skip"),
    sort_by: Optional[str] = Query(
        None,
        description="Field to sort by (id, email, username, full_name, created_at, updated_at)",
    ),
    sort_order: Optional[str] = Query(None, description="Sort order (asc, desc)"),
):
    """
    Get all users with optional filters and sorting

    ✅ Thin controller - delega a Use Case
    ✅ Validación con Query parameters
    ✅ Error handling
    ✅ Retorna usuarios paginados con total
    ✅ Soporta ordenamiento del servidor
    ✅ Protected endpoint - requires admin authentication
    """
    try:
        # ✅ Obtener Use Case del DI Container
        use_case = get_get_users_use_case()

        # ✅ Ejecutar Use Case
        users, total = await use_case.execute(
            skip=offset,
            limit=limit,
            is_active=is_active,
            is_admin=is_admin,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        # Convertir a UserResponse
        user_responses = [
            UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                is_active=user.is_active,
                is_admin=user.is_admin,
                created_at=user.created_at,
            )
            for user in users
        ]

        return UsersResponse(
            users=user_responses,
            total=total,
            limit=limit,
            offset=offset,
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error getting users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
):
    """
    Update an existing user

    ✅ Pydantic validation automática
    ✅ Thin controller
    ✅ Partial update (PATCH-like)
    ✅ Protected endpoint - requires admin authentication
    """
    try:
        # ✅ Obtener Use Case del DI Container
        use_case = get_update_user_use_case()

        # ✅ Ejecutar Use Case
        user = await use_case.execute(user_id, user_data)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_at=user.created_at,
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error updating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user",
        )
