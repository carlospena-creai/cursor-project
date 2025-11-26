"""
Use Case: Registrar Usuario

Maneja la lógica de registro de nuevos usuarios.
"""

from ..domain.interfaces.repositories import IUserRepository
from ..domain.models.user import User, UserCreate


class RegisterUserUseCase:
    """
    Use Case: Registrar un nuevo usuario

    Valida que email y username sean únicos.
    Delega el hashing del password al repository/infrastructure.
    """

    def __init__(self, repository: IUserRepository, password_hasher):
        """
        Inicializa el use case

        Args:
            repository: Implementación del repositorio de usuarios
            password_hasher: Utilidad para hashear passwords
        """
        self.repository = repository
        self.password_hasher = password_hasher

    async def execute(self, user_data: UserCreate) -> User:
        """
        Ejecuta el registro de usuario

        Args:
            user_data: Datos del nuevo usuario

        Returns:
            Usuario creado

        Raises:
            ValueError: Si el email o username ya existe

        Reglas de Negocio:
        - Email debe ser único
        - Username debe ser único
        - Password debe cumplir requisitos mínimos
        """
        # Verificar que el email no exista
        if await self.repository.email_exists(user_data.email):
            raise ValueError(f"Email {user_data.email} is already registered")

        # Verificar que el username no exista
        if await self.repository.username_exists(user_data.username):
            raise ValueError(f"Username {user_data.username} is already taken")

        # Hashear el password
        hashed_password = self.password_hasher.hash(user_data.password)

        # Crear el usuario
        user = await self.repository.create(user_data, hashed_password)

        return user
