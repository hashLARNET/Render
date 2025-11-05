from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Importaciones CORREGIDAS - sin "backend."
from api.v1.endpoints import auth, inventory, withdrawals, warehouses, history
from config import settings
from database.base import engine
from models import Base
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Multi-Warehouse Inventory System",
    description="Sistema de gestión de inventario multi-bodega",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
    # Configuración adicional para Render
    openapi_url="/openapi.json"
)

# Add rate limiter state and exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware - Configurado para Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(warehouses.router, prefix="/api/v1/warehouses", tags=["warehouses"])
app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["inventory"])
app.include_router(withdrawals.router, prefix="/api/v1/withdrawals", tags=["withdrawals"])
app.include_router(history.router, prefix="/api/v1/history", tags=["history"])

@app.get("/")
def read_root():
    return {
        "message": "Multi-Warehouse Inventory System API", 
        "status": "running",
        "environment": "production",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/api/info")
def api_info():
    return {
        "name": "Multi-Warehouse Inventory System",
        "version": "1.0.0",
        "docs": "/docs",
        "environment": "render"
    }

# Server startup event
@app.on_event("startup")
async def startup_event():
    print("🚀 Application starting up...")
    print(f"📊 Database URL: {settings.database_url[:30]}...")
    print(f"🌐 Allowed origins: {settings.allowed_origins}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)