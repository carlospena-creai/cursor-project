"""
Authentication Middleware

Middleware global para autenticación JWT.
Proporciona dependencias FastAPI para proteger endpoints.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ...users.domain.models.user import User

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> "User":
    """
    Dependency para obtener el usuario actual autenticado

    Verifica el token JWT y retorna el usuario correspondiente.
    Lanza HTTPException si el token es inválido o el usuario no existe.

    Args:
        credentials: Credenciales HTTP Bearer token

    Returns:
        Usuario autenticado

    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    # Importar aquí para evitar circular dependency
    from ...users.executions import get_jwt_handler, get_user_repository

    token = credentials.credentials

    # Verificar token
    jwt_handler = get_jwt_handler()
    payload = jwt_handler.verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Obtener user_id del payload
    user_id = int(payload.get("sub"))

    # Obtener usuario
    user_repository = get_user_repository()
    user = await user_repository.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user


async def get_current_active_user(
    current_user: "User" = Depends(get_current_user),
) -> "User":
    """
    Dependency para obtener usuario activo

    Verifica que el usuario esté autenticado y activo.

    Args:
        current_user: Usuario obtenido de get_current_user

    Returns:
        Usuario activo

    Raises:
        HTTPException: Si el usuario no está activo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    return current_user


async def get_current_admin_user(
    current_user: "User" = Depends(get_current_user),
) -> "User":
    """
    Dependency para obtener usuario administrador

    Verifica que el usuario esté autenticado, activo y sea administrador.

    Args:
        current_user: Usuario obtenido de get_current_user

    Returns:
        Usuario administrador

    Raises:
        HTTPException: Si el usuario no es administrador
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
) -> Optional["User"]:
    """
    Dependency opcional para obtener usuario

    Similar a get_current_user pero no lanza excepción si no hay token.
    Útil para endpoints que funcionan tanto autenticados como no autenticados.

    Args:
        credentials: Credenciales HTTP Bearer token (opcional)

    Returns:
        Usuario si está autenticado, None si no hay token
    """
    if not credentials:
        return None

    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None
