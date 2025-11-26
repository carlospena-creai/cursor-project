"""
User Domain Model

Modelo de dominio puro para usuarios.
Incluye validaciones y reglas de negocio.
"""

from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional
from datetime import datetime
import re


class User(BaseModel):
    """
    Modelo de Dominio de Usuario

    Representa un usuario en el sistema con sus atributos y reglas de negocio.
    """

    id: Optional[int] = None
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator("username")
    def validate_username(cls, v):
        """Valida que el username sea alfanumérico con guiones y guiones bajos"""
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "Username can only contain letters, numbers, hyphens and underscores"
            )
        return v.lower()

    @validator("full_name")
    def validate_full_name(cls, v):
        """Valida el nombre completo si se proporciona"""
        if v is not None:
            v = v.strip()
            if len(v) < 2:
                raise ValueError("Full name must be at least 2 characters")
        return v

    def is_authenticated(self) -> bool:
        """Verifica si el usuario está autenticado (activo)"""
        return self.is_active

    def has_admin_access(self) -> bool:
        """Verifica si el usuario tiene acceso de administrador"""
        return self.is_active and self.is_admin

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}


class UserCreate(BaseModel):
    """
    Data Transfer Object para crear un usuario

    Incluye el password en texto plano que será hasheado antes de almacenar.
    """

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)
    full_name: Optional[str] = Field(None, max_length=100)

    @validator("username")
    def validate_username(cls, v):
        """Valida formato del username"""
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "Username can only contain letters, numbers, hyphens and underscores"
            )
        return v.lower()

    @validator("password")
    def validate_password(cls, v):
        """Valida la fortaleza del password"""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v


class UserLogin(BaseModel):
    """
    Data Transfer Object para login

    Acepta email o username para login.
    """

    email_or_username: str
    password: str


class UserResponse(BaseModel):
    """
    Data Transfer Object para respuestas de usuario

    Excluye información sensible como el password.
    """

    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: Optional[datetime]

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}
