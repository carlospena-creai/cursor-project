# Clean Architecture - Diagrama y Flujo

## 🏗️ Arquitectura en Capas

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
│                    (FastAPI Endpoints)                           │
│                                                                   │
│  GET /products, POST /products, etc.                            │
│  → Thin Controllers (solo validación HTTP)                      │
└────────────────────┬────────────────────────────────────────────┘
                     │ Calls Use Cases
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                              │
│                      (Use Cases)                                 │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │ CreateProduct    │  │ GetProducts      │                    │
│  │ UseCase          │  │ UseCase          │  ...                │
│  └──────────────────┘  └──────────────────┘                    │
│                                                                   │
│  → Business Logic / Orchestration                               │
└────────────────────┬────────────────────────────────────────────┘
                     │ Uses Interfaces (DIP)
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                     DOMAIN LAYER                                 │
│                 (Models + Interfaces)                            │
│                                                                   │
│  ┌──────────────────────────────────────────┐                   │
│  │  IProductRepository (Interface)          │                   │
│  │  - create()                              │                   │
│  │  - get_by_id()                           │                   │
│  │  - get_all()                             │                   │
│  │  - update()                              │                   │
│  │  - delete()                              │                   │
│  └──────────────────────────────────────────┘                   │
│                                                                   │
│  ┌──────────────────────────────────────────┐                   │
│  │  Product (Domain Model)                  │                   │
│  │  - Business rules                        │                   │
│  │  - Validations                           │                   │
│  │  - Pure Python + Pydantic                │                   │
│  └──────────────────────────────────────────┘                   │
│                                                                   │
│  → Core Business Logic (framework-independent)                  │
└────────────────────┬────────────────────────────────────────────┘
                     │ Implemented by
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│                 INFRASTRUCTURE LAYER                             │
│              (Concrete Implementations)                          │
│                                                                   │
│  ┌──────────────────────────────────────────┐                   │
│  │  SQLiteProductRepository                 │                   │
│  │  implements IProductRepository           │                   │
│  │                                          │                   │
│  │  - Prepared statements                   │                   │
│  │  - Transaction management                │                   │
│  │  - Type conversions                      │                   │
│  └──────────────────────────────────────────┘                   │
│                                                                   │
│  → External dependencies (DB, APIs, etc.)                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  DEPENDENCY INJECTION                            │
│                    (executions.py)                               │
│                                                                   │
│  Wires everything together:                                     │
│  - Repository instances                                         │
│  - Use Case factory functions                                   │
│  - Configuration                                                │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de una Request (Ejemplo: POST /products)

```
1. HTTP Request
   POST /products
   Body: { "name": "iPhone", "price": 999.99, ... }

   ↓

2. FastAPI Endpoint (infrastructure/api/products.py)
   @router.post("/")
   async def create_product(product_data: ProductCreate):
       ✅ Validación HTTP automática (Pydantic)
       ✅ Obtiene Use Case del DI Container

       use_case = get_create_product_use_case()

   ↓

3. DI Container (executions.py)
   def get_create_product_use_case():
       ✅ Crea instancia del Use Case
       ✅ Inyecta dependencias (repository)

       repository = get_product_repository()  # SQLiteProductRepository
       return CreateProductUseCase(repository)

   ↓

4. Use Case (application/create_product.py)
   async def execute(self, product_data: ProductCreate):
       ✅ Business logic / validaciones adicionales
       ✅ Orquestación

       product = await self.repository.create(product_data)

       # Aquí podríamos:
       # - Disparar eventos de dominio
       # - Logging
       # - Notificaciones
       # - Etc.

   ↓

5. Repository (infrastructure/db/repositories/product_repository.py)
   async def create(self, product_data: ProductCreate):
       ✅ Prepared statements (no SQL injection)
       ✅ Transaction management
       ✅ Type conversions (Decimal → int cents)

       cursor.execute(
           "INSERT INTO products (name, price, ...) VALUES (?, ?, ...)",
           (product_data.name, price_cents, ...)
       )

   ↓

6. Database (SQLite)
   ✅ INSERT con constraints
   ✅ Indices para performance
   ✅ Auto-increment ID

   ↓

7. Response Flow (backwards)
   Database → Repository → Use Case → Endpoint → HTTP Response

   ✅ Product domain model retornado
   ✅ FastAPI serializa automáticamente
   ✅ HTTP 201 Created
```

## 🎯 Dependency Flow (Dependency Inversion Principle)

```
High-Level Modules (Application Layer)
         ↓ depends on ↓
      Abstractions (Domain Interfaces)
         ↑ implements ↑
Low-Level Modules (Infrastructure Layer)


Ejemplo Concreto:

CreateProductUseCase (Application)
         ↓ depends on ↓
    IProductRepository (Domain Interface)
         ↑ implements ↑
SQLiteProductRepository (Infrastructure)


✅ BENEFICIO: Podemos cambiar SQLiteProductRepository por
              PostgreSQLProductRepository sin tocar nada más
```

## 📦 Module Dependencies

```
domain/
  ├─ No dependencies (pure Python + Pydantic)
  └─ Self-contained

application/
  ├─ Depends on: domain/
  └─ No infrastructure dependencies

infrastructure/
  ├─ Depends on: domain/, application/
  └─ External dependencies: FastAPI, SQLite, etc.

executions.py
  ├─ Depends on: domain/, application/, infrastructure/
  └─ Wires everything together
```

## 🔑 Key Design Patterns

### 1. Repository Pattern

```python
# Abstraction (Domain)
class IProductRepository(ABC):
    @abstractmethod
    async def create(self, data: ProductCreate) -> Product:
        pass

# Implementation (Infrastructure)
class SQLiteProductRepository(IProductRepository):
    async def create(self, data: ProductCreate) -> Product:
        # Concrete implementation
        pass
```

### 2. Use Case Pattern

```python
class CreateProductUseCase:
    def __init__(self, repository: IProductRepository):
        self.repository = repository

    async def execute(self, data: ProductCreate) -> Product:
        # Business logic here
        return await self.repository.create(data)
```

### 3. Dependency Injection

```python
# Manual DI Container
def get_create_product_use_case() -> CreateProductUseCase:
    repository = get_product_repository()
    return CreateProductUseCase(repository)  # DI here
```

### 4. Factory Pattern

```python
# Factory functions in executions.py
def get_product_repository() -> IProductRepository:
    global _product_repository
    if _product_repository is None:
        _product_repository = SQLiteProductRepository()
    return _product_repository
```

## ✅ SOLID Principles in Action

### Single Responsibility (S)

- `CreateProductUseCase`: Solo crea productos
- `SQLiteProductRepository`: Solo maneja persistencia
- `products.py` endpoints: Solo maneja HTTP

### Open/Closed (O)

- Abierto para extensión: Crear `PostgreSQLProductRepository`
- Cerrado para modificación: No tocar código existente

### Liskov Substitution (L)

- Cualquier implementación de `IProductRepository` puede reemplazar a otra
- `SQLiteProductRepository` ↔ `PostgreSQLProductRepository`

### Interface Segregation (I)

- `IProductRepository`: Interface específica para productos
- No interfaces grandes y monolíticas

### Dependency Inversion (D)

- Use Cases dependen de `IProductRepository` (abstracción)
- No dependen de `SQLiteProductRepository` (implementación)

## 🧪 Testing Strategy

```
Unit Tests (Domain Layer)
  ✅ Test models y validaciones
  ✅ Sin dependencias externas
  ✅ Rápidos y aislados

Use Case Tests (Application Layer)
  ✅ Mock repositories
  ✅ Test business logic
  ✅ Sin tocar DB real

Integration Tests (Infrastructure Layer)
  ✅ Test con DB real (o test DB)
  ✅ Test endpoints E2E
  ✅ Test repository implementations

Example:
  # Unit test
  def test_product_validation():
      product = Product(name="Test", price=Decimal("10.00"), ...)
      assert product.is_available()

  # Use Case test with mock
  async def test_create_product_use_case():
      mock_repo = MockProductRepository()
      use_case = CreateProductUseCase(mock_repo)
      result = await use_case.execute(test_data)
      assert result.id == 1

  # Integration test
  async def test_create_product_endpoint():
      response = await client.post("/products", json={...})
      assert response.status_code == 201
```

## 🚀 Benefits Summary

| Aspect              | Before (Legacy)              | After (Clean Architecture)   |
| ------------------- | ---------------------------- | ---------------------------- |
| **Testability**     | Difícil (acoplado a DB)      | Fácil (mocks)                |
| **Maintainability** | Baja (código mezclado)       | Alta (capas separadas)       |
| **Flexibility**     | Rígido                       | Flexible (cambiar DB, etc.)  |
| **Security**        | SQL Injection vulnerable     | Seguro (prepared statements) |
| **Scalability**     | Difícil                      | Fácil (modular)              |
| **Business Logic**  | Mezclada con infraestructura | Encapsulada en Use Cases     |
| **Dependencies**    | Acoplamiento fuerte          | Bajo acoplamiento            |
