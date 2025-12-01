"""
Users API Endpoints

Endpoints para autenticación y gestión de usuarios.
"""

from fastapi import APIRouter, HTTPException, status, Depends

from ...domain.models.user import User, UserCreate, UserLogin, UserResponse
from ...executions import (
    get_register_user_use_case,
    get_login_user_use_case,
)
from ....shared.middleware.auth import get_current_active_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreate):
    """
    Registra un nuevo usuario

    Valida que email y username sean únicos.
    Hashea el password automáticamente.
    """
    try:
        use_case = get_register_user_use_case()
        user = await use_case.execute(user_data)

        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_at=user.created_at,
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Error registering user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user",
        )


@router.post("/login")
async def login(login_data: UserLogin):
    """
    Autentica un usuario y retorna un JWT token

    Acepta email o username para login.
    """
    try:
        use_case = get_login_user_use_case()
        result = await use_case.execute(login_data)

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        print(f"Error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication error",
        )


@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user: User = Depends(get_current_active_user),
):
    """
    Obtiene el perfil del usuario autenticado

    Requiere token JWT en el header Authorization.
    ✅ Usa middleware de autenticación
    """
    try:
        return UserResponse(
            id=current_user.id,
            email=current_user.email,
            username=current_user.username,
            full_name=current_user.full_name,
            is_active=current_user.is_active,
            is_admin=current_user.is_admin,
            created_at=current_user.created_at,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving profile",
        )


@router.get("/health", include_in_schema=False)
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "module": "auth"}
