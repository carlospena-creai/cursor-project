"""
Use Case: Obtener Perfil de Usuario

Recupera la información del perfil de un usuario autenticado.
"""

from typing import Optional
from ..domain.interfaces.repositories import IUserRepository
from ..domain.models.user import User


class GetProfileUseCase:
    """
    Use Case: Obtener el perfil de un usuario

    Retorna la información del usuario por su ID.
    """

    def __init__(self, repository: IUserRepository):
        """
        Inicializa el use case

        Args:
            repository: Implementación del repositorio de usuarios
        """
        self.repository = repository

    async def execute(self, user_id: int) -> Optional[User]:
        """
        Ejecuta la obtención del perfil

        Args:
            user_id: ID del usuario

        Returns:
            Usuario si existe, None si no se encuentra

        Raises:
            ValueError: Si el user_id es inválido
        """
        if user_id <= 0:
            raise ValueError("Invalid user ID")

        user = await self.repository.get_by_id(user_id)

        if not user:
            return None

        # Verificar que el usuario esté activo
        if not user.is_active:
            raise ValueError("User account is disabled")

        return user
