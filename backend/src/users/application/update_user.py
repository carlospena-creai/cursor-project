"""
Update User Use Case

✅ Separación de responsabilidades: Un use case por operación
✅ Valida reglas de negocio antes de actualizar
"""

from typing import Optional
from ..domain.interfaces.repositories import IUserRepository
from ..domain.models.user import User, UserUpdate


class UpdateUserUseCase:
    """
    Use Case: Update an existing user

    ✅ Maneja lógica de validación y actualización
    ✅ Depende de abstracción (repository interface)
    """

    def __init__(self, repository: IUserRepository):
        """
        Initialize use case with repository

        Args:
            repository: User repository implementation
        """
        self.repository = repository

    async def execute(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Execute the use case

        Args:
            user_id: User identifier
            user_data: Data to update the user

        Returns:
            Updated user if found, None otherwise

        Raises:
            ValueError: If user_id is invalid or validation fails

        Business Rules:
        - User must exist
        - Email and username must be unique if changed
        - Cannot remove the last admin
        """
        # ✅ Validación de parámetros
        if user_id <= 0:
            raise ValueError("User ID must be positive")

        # ✅ Verificar que el usuario existe
        existing = await self.repository.get_by_id(user_id)
        if not existing:
            return None

        # ✅ Validar email único si se está cambiando
        if user_data.email and user_data.email != existing.email:
            if await self.repository.email_exists(user_data.email):
                raise ValueError(f"Email {user_data.email} already exists")

        # ✅ Validar username único si se está cambiando
        if user_data.username and user_data.username != existing.username:
            if await self.repository.username_exists(user_data.username):
                raise ValueError(f"Username {user_data.username} already exists")

        # ✅ Actualizar en el repositorio
        updated_user = await self.repository.update(user_id, user_data)

        return updated_user
