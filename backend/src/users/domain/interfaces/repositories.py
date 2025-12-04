"""
Interfaces de Repositorio de Usuarios

Define el contrato para operaciones de persistencia de usuarios.
Principio de Inversión de Dependencias (SOLID-D).
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from ..models.user import User, UserCreate, UserUpdate


class IUserRepository(ABC):
    """
    Interfaz del Repositorio de Usuarios

    Define el contrato para operaciones CRUD de usuarios.
    Independiente de la implementación de persistencia.
    """

    @abstractmethod
    async def create(self, user_data: UserCreate, hashed_password: str) -> User:
        """
        Crea un nuevo usuario

        Args:
            user_data: Datos del usuario
            hashed_password: Password ya hasheado

        Returns:
            Usuario creado con ID asignado

        Raises:
            ValueError: Si el email o username ya existe
        """
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por ID

        Args:
            user_id: Identificador del usuario

        Returns:
            Usuario si existe, None si no se encuentra
        """
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por email

        Args:
            email: Email del usuario

        Returns:
            Usuario si existe, None si no se encuentra
        """
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Obtiene un usuario por username

        Args:
            username: Username del usuario

        Returns:
            Usuario si existe, None si no se encuentra
        """
        pass

    @abstractmethod
    async def get_password_hash(self, user_id: int) -> Optional[str]:
        """
        Obtiene el hash del password de un usuario

        Args:
            user_id: Identificador del usuario

        Returns:
            Hash del password si el usuario existe
        """
        pass

    @abstractmethod
    async def email_exists(self, email: str) -> bool:
        """
        Verifica si un email ya está registrado

        Args:
            email: Email a verificar

        Returns:
            True si el email existe
        """
        pass

    @abstractmethod
    async def username_exists(self, username: str) -> bool:
        """
        Verifica si un username ya está registrado

        Args:
            username: Username a verificar

        Returns:
            True si el username existe
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        is_admin: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[User]:
        """
        Obtiene todos los usuarios con filtros opcionales y ordenamiento

        Args:
            skip: Número de usuarios a omitir (paginación)
            limit: Número máximo de usuarios a retornar
            is_active: Filtrar por estado activo (True=activos, False=inactivos, None=todos)
            is_admin: Filtrar por rol admin (True=admins, False=regulares, None=todos)
            search: Búsqueda en email, username o full_name
            sort_by: Campo por el cual ordenar (id, email, username, full_name, created_at, updated_at)
            sort_order: Orden de clasificación (asc, desc)

        Returns:
            Lista de usuarios que coinciden con los filtros
        """
        pass

    @abstractmethod
    async def count(
        self,
        is_active: Optional[bool] = None,
        is_admin: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> int:
        """
        Cuenta usuarios con filtros opcionales

        Args:
            is_active: Filtrar por estado activo
            is_admin: Filtrar por rol admin
            search: Búsqueda en email, username o full_name

        Returns:
            Número de usuarios que coinciden con los filtros
        """
        pass

    @abstractmethod
    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Actualiza un usuario existente

        Args:
            user_id: Identificador del usuario
            user_data: Datos para actualizar el usuario

        Returns:
            Usuario actualizado si existe, None si no se encuentra
        """
        pass
