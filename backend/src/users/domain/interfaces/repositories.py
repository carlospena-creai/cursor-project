"""
Interfaces de Repositorio de Usuarios

Define el contrato para operaciones de persistencia de usuarios.
Principio de Inversión de Dependencias (SOLID-D).
"""

from abc import ABC, abstractmethod
from typing import Optional
from ..models.user import User, UserCreate


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
