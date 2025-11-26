"""
Use Case: Login de Usuario

Maneja la autenticación de usuarios y generación de JWT tokens.
"""

from typing import Dict
from ..domain.interfaces.repositories import IUserRepository
from ..domain.models.user import UserLogin


class LoginUserUseCase:
    """
    Use Case: Autenticar usuario y generar token JWT

    Valida credenciales y genera token de acceso.
    """

    def __init__(self, repository: IUserRepository, password_hasher, token_generator):
        """
        Inicializa el use case

        Args:
            repository: Implementación del repositorio de usuarios
            password_hasher: Utilidad para verificar passwords
            token_generator: Utilidad para generar JWT tokens
        """
        self.repository = repository
        self.password_hasher = password_hasher
        self.token_generator = token_generator

    async def execute(self, login_data: UserLogin) -> Dict:
        """
        Ejecuta el login de usuario

        Args:
            login_data: Credenciales del usuario

        Returns:
            Dict con access_token y tipo de token

        Raises:
            ValueError: Si las credenciales son inválidas

        Reglas de Negocio:
        - Usuario debe existir
        - Password debe ser correcto
        - Usuario debe estar activo
        """
        # Buscar usuario por email o username
        user = None

        # Intentar buscar por email primero
        if "@" in login_data.email_or_username:
            user = await self.repository.get_by_email(login_data.email_or_username)
        else:
            # Buscar por username
            user = await self.repository.get_by_username(login_data.email_or_username)

        # Verificar que el usuario existe
        if not user:
            raise ValueError("Invalid credentials")

        # Verificar que el usuario está activo
        if not user.is_active:
            raise ValueError("User account is disabled")

        # Obtener el hash del password
        password_hash = await self.repository.get_password_hash(user.id)

        # Verificar el password
        if not self.password_hasher.verify(login_data.password, password_hash):
            raise ValueError("Invalid credentials")

        # Generar token JWT
        token = self.token_generator.create_access_token(
            data={"sub": str(user.id), "username": user.username, "email": user.email}
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "is_admin": user.is_admin,
            },
        }
