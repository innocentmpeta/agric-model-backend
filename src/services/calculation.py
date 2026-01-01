from typing import Dict, List
from src.core.gravity_model import calculate_gravity_flows
from src.services.data_loader import load_provinces_data
from src.api.models import ModelRequest, ModelResponse, FlowResult

def calculate_model(request: ModelRequest) -> ModelResponse:
    """
    Main calculation service that processes model request
    """
    # Load province data
    provinces = load_provinces_data()
    
    # Extract parameters
    params = request.parameters
    
    # Prepare advanced config for gravity model
    advanced_config = {}
    if request.advancedConfig:
        if request.advancedConfig.season:
            advanced_config['season'] = request.advancedConfig.season.dict()
        if request.advancedConfig.transportCost:
            advanced_config['transportCost'] = request.advancedConfig.transportCost.dict()
        if request.advancedConfig.fleetMix:
            advanced_config['fleetMix'] = request.advancedConfig.fleetMix.dict()
    
    # Calculate flows using gravity model
    result = calculate_gravity_flows(
        provinces=provinces,
        commodity=params.commodity.value,
        distance_decay=params.distanceDecay,
        transport_cost_per_km=params.transportCostPerKm,
        truck_capacity=params.truckCapacity,
        advanced_config=advanced_config if advanced_config else None
    )
    
    # Convert to response format
    flows = [FlowResult(**flow) for flow in result['flows']]
    
    return ModelResponse(
        flows=flows,
        totalVolume=result['totalVolume'],
        totalCost=result['totalCost'],
        totalTrucks=result['totalTrucks'],
        averageDistance=result['averageDistance'],
        executionTime=result['executionTime']
    )