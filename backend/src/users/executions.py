"""
Contenedor de Inyección de Dependencias - Users Module

Conecta todas las capas del módulo de usuarios.
"""

from typing import Optional

# Domain
from .domain.interfaces.repositories import IUserRepository

# Application
from .application.register import RegisterUserUseCase
from .application.login import LoginUserUseCase
from .application.get_profile import GetProfileUseCase

# Infrastructure
from .infrastructure.db.repositories.user_repository import SQLiteUserRepository
from .infrastructure.security.password import PasswordHasher
from .infrastructure.security.jwt import JWTHandler


# ============================================================================
# INSTANCIAS SINGLETON
# ============================================================================

_user_repository: Optional[IUserRepository] = None
_password_hasher: Optional[PasswordHasher] = None
_jwt_handler: Optional[JWTHandler] = None


def get_user_repository() -> IUserRepository:
    """Obtiene la instancia del repositorio de usuarios"""
    global _user_repository
    if _user_repository is None:
        _user_repository = SQLiteUserRepository()
    return _user_repository


def get_password_hasher() -> PasswordHasher:
    """Obtiene la instancia del password hasher"""
    global _password_hasher
    if _password_hasher is None:
        _password_hasher = PasswordHasher()
    return _password_hasher


def get_jwt_handler() -> JWTHandler:
    """Obtiene la instancia del JWT handler"""
    global _jwt_handler
    if _jwt_handler is None:
        _jwt_handler = JWTHandler()
    return _jwt_handler


# ============================================================================
# FACTORY FUNCTIONS PARA USE CASES
# ============================================================================


def get_register_user_use_case() -> RegisterUserUseCase:
    """Crea instancia de RegisterUserUseCase"""
    repository = get_user_repository()
    password_hasher = get_password_hasher()
    return RegisterUserUseCase(repository, password_hasher)


def get_login_user_use_case() -> LoginUserUseCase:
    """Crea instancia de LoginUserUseCase"""
    repository = get_user_repository()
    password_hasher = get_password_hasher()
    jwt_handler = get_jwt_handler()
    return LoginUserUseCase(repository, password_hasher, jwt_handler)


def get_profile_use_case() -> GetProfileUseCase:
    """Crea instancia de GetProfileUseCase"""
    repository = get_user_repository()
    return GetProfileUseCase(repository)


# ============================================================================
# INICIALIZACIÓN
# ============================================================================


def init_users_module():
    """Inicializa el módulo de usuarios"""
    from .infrastructure.db.connection import init_user_database

    print("🔧 Inicializando módulo de Users...")
    init_user_database()
    print("✅ Módulo de Users inicializado correctamente")
