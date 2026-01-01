from fastapi import APIRouter, HTTPException
from typing import List
from src.api.models import ModelRequest, ModelResponse, ProvinceData
from src.services.calculation import calculate_model
from src.services.data_loader import load_provinces_data

router = APIRouter()

@router.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Agricultural Transport Model API",
        "version": "1.0.0"
    }

@router.get("/provinces", response_model=List[ProvinceData])
async def get_provinces():
    """
    Get all provinces with their supply and demand data
    """
    try:
        provinces = load_provinces_data()
        return provinces
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calculate", response_model=ModelResponse)
async def calculate_flows(request: ModelRequest):
    """
    Calculate commodity flows based on gravity model
    """
    try:
        result = calculate_model(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }