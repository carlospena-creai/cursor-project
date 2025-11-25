# 💰 Estrategia de Precios - Decimal + Integer

## 🎯 Problema que Resolvemos

### ❌ Float Precision Issues

```python
# Problema con floats:
>>> 0.1 + 0.2
0.30000000000000004  # ❌ Impreciso!

>>> price = 99.99
>>> price * 100
9999.000000000001  # ❌ Error de precisión
```

## ✅ Solución Implementada

Usamos **dos formatos diferentes** en capas diferentes:

### 1. Domain Model (Application Layer)

```python
from decimal import Decimal

class Product(BaseModel):
    price: Decimal  # $99.99

    def calculate_total(self, quantity: int) -> Decimal:
        return self.price * quantity  # ✅ Precisión exacta
```

**Por qué Decimal:**

- ✅ Precisión exacta para cálculos matemáticos
- ✅ No pierde precisión en multiplicaciones/divisiones
- ✅ Ideal para business logic

### 2. Database (Infrastructure Layer)

```sql
CREATE TABLE products (
    price INTEGER NOT NULL  -- Almacena centavos: 9999 = $99.99
);
```

**Por qué INTEGER:**

- ✅ Evita completamente imprecisión de floats
- ✅ Más eficiente en DB (menos espacio)
- ✅ Más rápido en comparaciones e índices
- ✅ Compatible con todos los sistemas de DB

### 3. Repository (Conversión Automática)

```python
class SQLiteProductRepository:
    def _row_to_product(self, row) -> Product:
        """DB → Domain Model"""
        # ✅ Convertir INTEGER (centavos) a Decimal (dólares)
        price = Decimal(row['price']) / 100  # 9999 → $99.99
        return Product(price=price, ...)

    async def create(self, data: ProductCreate) -> Product:
        """Domain Model → DB"""
        # ✅ Convertir Decimal (dólares) a INTEGER (centavos)
        price_cents = int(data.price * 100)  # $99.99 → 9999

        cursor.execute(
            "INSERT INTO products (price) VALUES (?)",
            (price_cents,)
        )
```

## 🔄 Flujo Completo

```
User Input                Domain Model           Database
$99.99 (string)    →     Decimal('99.99')   →   9999 (INTEGER)
                         ↓                       ↓
                         Business Logic          Storage
                         ↓                       ↓
                         Decimal('99.99')   ←   9999 (INTEGER)
                         ↓
                         Response: {"price": 99.99}
```

## 📊 Comparación

| Aspecto           | Float (Legacy)            | Decimal + INTEGER (Clean Arch) |
| ----------------- | ------------------------- | ------------------------------ |
| **Precisión**     | ❌ Imprecisa (0.30000004) | ✅ Exacta (0.30)               |
| **Cálculos**      | ❌ Errores acumulativos   | ✅ Sin errores                 |
| **DB Storage**    | REAL (8 bytes)            | INTEGER (4 bytes) ✅           |
| **Performance**   | Slower                    | ✅ Faster                      |
| **Comparaciones** | ❌ Problemáticas          | ✅ Exactas                     |

## 💡 Ejemplos de Uso

### Crear Producto

```python
from decimal import Decimal
from src.products.domain.models import ProductCreate

# ✅ Domain Model usa Decimal
product_data = ProductCreate(
    name="iPhone 15",
    price=Decimal("999.99"),  # Precisión exacta
    stock=10,
    category="Electronics"
)

# Repository convierte automáticamente a centavos
use_case = get_create_product_use_case()
product = await use_case.execute(product_data)

# Base de datos guarda: 99999 (INTEGER)
```

### Calcular Total

```python
from decimal import Decimal

product = await repository.get_by_id(1)
# product.price = Decimal("999.99")  ← Convertido de 99999

quantity = 3
total = product.price * quantity
# total = Decimal("2999.97")  ✅ Precisión exacta

# Sin errores como: 2999.9700000000003 ❌
```

### API Response

```json
{
  "id": 1,
  "name": "iPhone 15",
  "price": 999.99, // ✅ Serializado desde Decimal
  "stock": 10
}
```

## 🎯 Ventajas de Esta Estrategia

### 1. Mejor de Dos Mundos

- ✅ **Decimal** para cálculos precisos (Domain)
- ✅ **INTEGER** para storage eficiente (Database)

### 2. Separation of Concerns

- Domain Model no sabe sobre centavos
- Database no sabe sobre Decimal
- Repository maneja la conversión

### 3. Clean Architecture

- Domain Layer independiente de DB
- Infrastructure Layer maneja detalles de implementación
- Fácil cambiar implementación

### 4. Testing

```python
# Test Domain (sin DB)
def test_calculate_total():
    product = Product(price=Decimal("99.99"), ...)
    total = product.calculate_total(3)
    assert total == Decimal("299.97")  # ✅ Exacto

# Test Repository (con DB)
async def test_repository_conversion():
    product = await repo.create(ProductCreate(price=Decimal("99.99")))
    # DB tiene: 9999 (centavos)
    retrieved = await repo.get_by_id(product.id)
    assert retrieved.price == Decimal("99.99")  # ✅ Convertido correctamente
```

## 🚨 Validaciones

### Máximo 2 Decimales

```python
@validator('price')
def validate_price(cls, v):
    """Validar máximo 2 decimales"""
    if v.as_tuple().exponent < -2:
        raise ValueError("Price can have at most 2 decimal places")
    return v
```

### Rango de Precios

```python
@validator('price')
def validate_price_range(cls, v):
    """Validar rango razonable"""
    if v <= 0:
        raise ValueError("Price must be positive")
    if v > Decimal('999999.99'):
        raise ValueError("Price too high")
    return v
```

## 📝 Resumen

**Estrategia completa:**

1. ✅ **Input/Output**: Decimal ($99.99) - precisión para usuario
2. ✅ **Business Logic**: Decimal - cálculos exactos
3. ✅ **Storage**: INTEGER centavos (9999) - eficiencia
4. ✅ **Conversión**: Repository Pattern - automática y transparente

**Resultado:**

- 🎯 Precisión matemática perfecta
- 🚀 Performance óptima en DB
- 🧪 Fácil de testear
- 🏗️ Clean Architecture compliant
