from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.api.routes import router
import os

# Create FastAPI application
app = FastAPI(
    title="Agricultural Transport Model API",
    description="Gravity model for agricultural commodity flows in South Africa",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api", tags=["model"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Agricultural Transport Model API",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Use Railway's PORT
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )