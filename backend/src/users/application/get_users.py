"""
Get Users Use Cases

✅ Separación de responsabilidades: Un use case por operación
✅ Query objects para filtros complejos
"""

import asyncio
from typing import List, Optional, Tuple
from ..domain.interfaces.repositories import IUserRepository
from ..domain.models.user import User


class GetUsersUseCase:
    """
    Use Case: Get all users with filters

    ✅ Maneja lógica de paginación y filtros
    ✅ Depende de abstracción (repository interface)
    """

    def __init__(self, repository: IUserRepository):
        """
        Initialize use case with repository

        Args:
            repository: User repository implementation
        """
        self.repository = repository

    async def execute(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        is_admin: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> Tuple[List[User], int]:
        """
        Execute the use case

        Args:
            skip: Number of users to skip (pagination)
            limit: Maximum number of users to return
            is_active: Filter by active status (True=active, False=inactive, None=all)
            is_admin: Filter by admin role (True=admins, False=regular, None=all)
            search: Search in email, username or full_name
            sort_by: Field to sort by (id, email, username, full_name, created_at, updated_at)
            sort_order: Sort order (asc, desc)

        Returns:
            Tuple of (List of users matching filters, total count)

        Business Rules:
        - Default limit is 100 (prevent overload)
        - Pagination for performance
        - Validates sort_by and sort_order
        """
        # ✅ Validación de parámetros
        if skip < 0:
            skip = 0

        if limit < 1:
            limit = 1
        elif limit > 100:
            limit = 100

        # ✅ Validar sort_by
        valid_sort_fields = [
            "id",
            "email",
            "username",
            "full_name",
            "created_at",
            "updated_at",
        ]
        if sort_by and sort_by not in valid_sort_fields:
            raise ValueError(
                f"Invalid sort_by field. Must be one of: {valid_sort_fields}"
            )

        # ✅ Validar sort_order
        if sort_order and sort_order not in ["asc", "desc"]:
            raise ValueError("sort_order must be 'asc' or 'desc'")

        # ✅ Obtener usuarios y total en paralelo
        users, total = await asyncio.gather(
            self.repository.get_all(
                skip=skip,
                limit=limit,
                is_active=is_active,
                is_admin=is_admin,
                search=search,
                sort_by=sort_by,
                sort_order=sort_order,
            ),
            self.repository.count(
                is_active=is_active,
                is_admin=is_admin,
                search=search,
            ),
        )

        return users, total
