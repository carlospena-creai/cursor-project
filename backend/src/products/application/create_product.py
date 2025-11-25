"""
Use Case: Crear Producto

Principio de Responsabilidad Única: Solo se encarga de crear productos.
Dependency Injection: El repositorio es inyectado.
Clean Architecture: Depende de abstracciones (interfaces).
"""

from ..domain.interfaces.repositories import IProductRepository
from ..domain.models.product import Product, ProductCreate


class CreateProductUseCase:
    """
    Use Case: Crear un nuevo producto

    Recibe el repositorio por inyección de dependencias.
    Implementa la lógica de aplicación para la creación de productos.
    Retorna el modelo de dominio.
    """

    def __init__(self, repository: IProductRepository):
        """
        Inicializa el use case con el repositorio

        Args:
            repository: Implementación del repositorio de productos
        """
        self.repository = repository

    async def execute(self, product_data: ProductCreate) -> Product:
        """
        Ejecuta el use case

        Args:
            product_data: Datos para crear el producto

        Returns:
            Producto creado

        Raises:
            ValueError: Si la validación falla

        Reglas de Negocio Aplicadas:
        - El precio debe ser positivo
        - El stock debe ser no negativo
        - La categoría debe ser válida
        """
        # Delegamos la creación al repository
        product = await self.repository.create(product_data)

        # Aquí podríamos disparar eventos de dominio
        # await event_bus.publish(ProductCreatedEvent(product))

        return product
