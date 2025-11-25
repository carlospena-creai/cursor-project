# Products Module - Clean Architecture

## 📚 Arquitectura

Este módulo implementa **Clean Architecture** completa con las siguientes capas:

```
products/
├── domain/                      # 🎯 DOMAIN LAYER
│   ├── interfaces/
│   │   └── repositories.py     # IProductRepository (abstracción)
│   └── models/
│       └── product.py          # Product, ProductCreate, ProductUpdate
│
├── application/                 # 🎯 APPLICATION LAYER
│   ├── create_product.py       # CreateProductUseCase
│   ├── get_products.py         # GetProductsUseCase, GetProductByIdUseCase
│   ├── update_product.py       # UpdateProductUseCase
│   └── delete_product.py       # DeleteProductUseCase
│
├── infrastructure/              # 🎯 INFRASTRUCTURE LAYER
│   ├── api/
│   │   └── products.py         # FastAPI endpoints
│   └── db/
│       ├── connection.py       # Database connection manager
│       └── repositories/
│           └── product_repository.py  # SQLiteProductRepository
│
└── executions.py                # 🎯 DI CONTAINER
```

## ✅ Principios Aplicados

### SOLID

- **S** - Single Responsibility: Cada clase tiene una única responsabilidad
- **O** - Open/Closed: Abierto a extensión, cerrado a modificación
- **L** - Liskov Substitution: Implementaciones intercambiables
- **I** - Interface Segregation: Interfaces específicas y pequeñas
- **D** - Dependency Inversion: Dependemos de abstracciones, no de implementaciones concretas

### Clean Architecture

1. **Domain Layer** (innermost)

   - Sin dependencias externas
   - Models puros con Pydantic
   - Interfaces (abstracciones)
   - Business rules

2. **Application Layer**

   - Use Cases (casos de uso)
   - Orquestación de lógica de negocio
   - Depende solo del Domain

3. **Infrastructure Layer** (outermost)

   - Implementaciones concretas
   - FastAPI endpoints
   - SQLite repository
   - Frameworks y librerías externas

4. **Dependency Injection**
   - DI Container manual
   - Factory functions
   - Inversión de dependencias

## 🔑 Características Implementadas

### ✅ Security

- **No SQL Injection**: Prepared statements en todas las queries
- **Input Validation**: Pydantic models con validaciones estrictas
- **Type Safety**: Python typing completo

### ✅ Performance

- **Database Indexes**: Indices en columnas frecuentemente consultadas
- **Connection Management**: Context managers para transacciones
- **Pagination**: Límites configurables para prevenir overload

### ✅ Data Integrity

- **Decimal en Domain Model**: Precisión matemática para cálculos ($99.99)
- **INTEGER en Database**: Almacena centavos (9999) para evitar imprecisión de floats
- **Repository Pattern**: Conversión automática entre formatos (centavos ↔ Decimal)
- **Enum para categorías**: Type-safe categories
- **CHECK Constraints**: Validaciones a nivel de base de datos
- **Soft Delete**: is_active flag (no hard deletes)

### ✅ Maintainability

- **Clean Architecture**: Capas bien definidas y separadas
- **Dependency Injection**: Fácil testing y cambio de implementaciones
- **Repository Pattern**: Abstracción de persistencia
- **Use Cases**: Lógica de negocio encapsulada

## 🚀 Uso

### Crear un Producto

```python
from src.products.executions import get_create_product_use_case
from src.products.domain.models import ProductCreate, ProductCategory
from decimal import Decimal

# Obtener Use Case del DI Container
use_case = get_create_product_use_case()

# Crear datos del producto
product_data = ProductCreate(
    name="New Product",
    price=Decimal("99.99"),
    stock=50,
    category=ProductCategory.ELECTRONICS,
    description="A great product"
)

# Ejecutar Use Case
product = await use_case.execute(product_data)
print(f"Created product: {product.id}")
```

### Obtener Productos con Filtros

```python
from src.products.executions import get_get_products_use_case

use_case = get_get_products_use_case()

products = await use_case.execute(
    skip=0,
    limit=10,
    category="Electronics",
    min_price=50.0,
    max_price=200.0,
    search="phone"
)
```

### Testing con Mock Repository

```python
class MockProductRepository(IProductRepository):
    """Mock repository para testing"""

    async def create(self, product_data: ProductCreate) -> Product:
        return Product(
            id=1,
            **product_data.dict()
        )

# Usar en test
mock_repo = MockProductRepository()
use_case = CreateProductUseCase(mock_repo)
result = await use_case.execute(test_data)
```

## 🔄 Cambiar Implementación

Para cambiar de SQLite a PostgreSQL (o cualquier otra DB):

1. Crear `PostgreSQLProductRepository` que implemente `IProductRepository`
2. Cambiar en `executions.py`:

```python
def get_product_repository() -> IProductRepository:
    global _product_repository
    if _product_repository is None:
        # Cambiar esta línea:
        _product_repository = PostgreSQLProductRepository()
    return _product_repository
```

¡Listo! Toda la aplicación usa la nueva implementación sin cambiar nada más.

## 📊 Beneficios de Esta Arquitectura

### Antes (Legacy)

❌ SQL Injection vulnerable  
❌ Lógica de negocio mezclada con presentación  
❌ Difícil de testear  
❌ Acoplamiento fuerte  
❌ Float para precios (precision issues)  
❌ Hard deletes  
❌ Sin validaciones robustas

### Ahora (Clean Architecture)

✅ Sin SQL Injection (prepared statements)  
✅ Capas separadas y bien definidas  
✅ Fácil de testear con mocks  
✅ Bajo acoplamiento, alta cohesión  
✅ Decimal para precios (precision)  
✅ Soft deletes  
✅ Validaciones robustas multi-nivel

## 🧪 Testing

Para testing, puedes crear mocks fácilmente:

```python
# tests/test_create_product.py
import pytest
from src.products.application import CreateProductUseCase
from src.products.domain.models import ProductCreate
from tests.mocks import MockProductRepository

@pytest.mark.asyncio
async def test_create_product():
    # Arrange
    mock_repo = MockProductRepository()
    use_case = CreateProductUseCase(mock_repo)
    product_data = ProductCreate(
        name="Test Product",
        price=Decimal("29.99"),
        stock=10,
        category=ProductCategory.ELECTRONICS
    )

    # Act
    result = await use_case.execute(product_data)

    # Assert
    assert result.name == "Test Product"
    assert result.price == Decimal("29.99")
```

## 📈 Próximos Pasos (Mejoras Futuras)

- [ ] Event Bus para eventos de dominio
- [ ] CQRS (Command Query Responsibility Segregation)
- [ ] Caching con Redis
- [ ] Async/await completo con asyncio
- [ ] Rate limiting
- [ ] API versioning
- [ ] GraphQL support
- [ ] Webhooks
- [ ] Audit logs
- [ ] Soft delete recovery
