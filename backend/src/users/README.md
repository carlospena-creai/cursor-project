# Users Module - JWT Authentication

## ✅ Módulo Completado - DÍA 2

Módulo de autenticación y gestión de usuarios con Clean Architecture.

### Estructura

```
src/users/
├── domain/                  # Domain Layer
│   ├── interfaces/
│   │   └── repositories.py  # IUserRepository
│   └── models/
│       └── user.py         # User, UserCreate, UserLogin
│
├── application/            # Application Layer
│   ├── register.py        # RegisterUserUseCase
│   ├── login.py           # LoginUserUseCase
│   └── get_profile.py     # GetProfileUseCase
│
├── infrastructure/         # Infrastructure Layer
│   ├── security/
│   │   ├── password.py    # PasswordHasher (bcrypt)
│   │   └── jwt.py         # JWTHandler
│   ├── db/
│   │   ├── connection.py
│   │   └── repositories/
│   │       └── user_repository.py
│   └── api/
│       └── users.py       # Endpoints
│
└── executions.py          # DI Container
```

### Endpoints Disponibles

```
POST /auth/register  - Registrar nuevo usuario
POST /auth/login     - Autenticar y obtener JWT
GET  /auth/profile   - Obtener perfil (requiere JWT)
```

### Seguridad Implementada

- ✅ Password Hashing con bcrypt
- ✅ JWT Tokens con expiración
- ✅ Validación de email y username únicos
- ✅ Password strength validation
- ✅ Protected endpoints con Bearer token

### Usuario por Defecto

```
username: admin
password: admin123
email: admin@example.com
```

### Ejemplo de Uso

**Register:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "SecurePass123",
    "full_name": "John Doe"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email_or_username": "johndoe",
    "password": "SecurePass123"
  }'
```

**Get Profile:**
```bash
curl http://localhost:8000/auth/profile \
  -H "Authorization: Bearer <your_token_here>"
```

