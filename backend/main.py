from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ✅ Clean Architecture: Import del router de Infrastructure
from src.products.infrastructure.api import router as products_router

# ✅ Clean Architecture: Import del DI Container para inicialización
from src.products.executions import init_products_module

# ✅ Configuración mejorada con documentación
app = FastAPI(
    title="E-commerce Clean Architecture API",
    description="E-commerce API refactored with Clean Architecture principles",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ✅ CORS configuration (ajustar según necesidades)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers - Clean Architecture
app.include_router(products_router)


@app.get("/", tags=["General"])
async def root():
    """Root endpoint - basic health check"""
    return {
        "message": "E-commerce Clean Architecture API",
        "status": "running",
        "version": "1.0.0",
        "architecture": "Clean Architecture",
        "principles": ["SOLID", "DDD", "Dependency Injection"],
    }


@app.get("/health", tags=["General"])
async def health_check():
    """Basic health check endpoint"""
    return {"status": "ok", "message": "API is running"}


if __name__ == "__main__":
    # ✅ Initialize products module with Clean Architecture
    print("🔧 Initializing E-commerce API with Clean Architecture...")
    init_products_module()
    print("✅ All modules initialized successfully")

    # ✅ Start server
    print("🚀 Starting E-commerce Clean Architecture API...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
