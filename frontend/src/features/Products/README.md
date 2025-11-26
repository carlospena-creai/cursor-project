# Products Feature

## Feature-Based Architecture

Este feature encapsula toda la funcionalidad relacionada con productos.

### Estructura

```
Products/
├── components/          # Componentes del feature
│   ├── ProductCard.tsx
│   └── ProductsList.tsx
├── hooks/              # Custom hooks
│   └── useProducts.ts
├── services/           # API clients
│   └── productsApi.ts
├── types/              # Type definitions
│   └── index.ts
├── index.ts            # Barrel export
└── README.md
```

### Componentes

**ProductCard**

- Componente presentacional para mostrar un producto
- Props: product, onEdit?, onDelete?
- Reutilizable en diferentes contextos

**ProductsList**

- Contenedor principal del feature
- Maneja estado, filtros y acciones
- Orquesta ProductCard y useProducts hook

### Hooks

**useProducts**

- Maneja fetching de productos
- Loading states y error handling
- Filtros y refetch

### Servicios

**productsApi**

- Encapsula todas las llamadas HTTP
- CRUD completo de productos
- Error handling centralizado

### Uso

```tsx
import { ProductsList } from "@/features/Products";

// En cualquier página
<ProductsList initialFilters={{ category: "Electronics" }} />;
```

### Principios Aplicados

- ✅ Feature-based architecture
- ✅ Component composition
- ✅ Custom hooks para lógica reutilizable
- ✅ Service layer para API calls
- ✅ TypeScript para type safety
- ✅ Separation of concerns
