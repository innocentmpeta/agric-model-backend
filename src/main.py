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

# Configure CORS - EXPLICITLY allow your domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://gravitymodel.code7.co.za",
        "http://gravitymodel.code7.co.za",
        "https://www.gravitymodel.code7.co.za",
    ],
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
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )