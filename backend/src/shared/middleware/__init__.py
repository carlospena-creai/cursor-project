"""
Shared Middleware

Middleware compartido para toda la aplicación.
"""

from .auth import (
    get_current_user,
    get_current_active_user,
    get_current_admin_user,
    get_optional_user,
    security,
)

__all__ = [
    "get_current_user",
    "get_current_active_user",
    "get_current_admin_user",
    "get_optional_user",
    "security",
]
