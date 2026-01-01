from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from enum import Enum

class Commodity(str, Enum):
    MAIZE = "maize"
    WHEAT = "wheat"

class Season(str, Enum):
    POST_HARVEST = "post-harvest"
    OFF_SEASON = "off-season"
    PLANTING = "planting"

class ProvinceData(BaseModel):
    id: str
    name: str
    coordinates: Dict[str, float]  # {lat, lng}
    supply: Dict[str, float]  # {commodity: tonnes}
    demand: Dict[str, float]  # {commodity: tonnes}

class GravityModelParameters(BaseModel):
    commodity: Commodity = Field(default=Commodity.MAIZE)
    distanceDecay: float = Field(default=2.0, ge=0.5, le=5.0)
    transportCostPerKm: float = Field(default=0.5, ge=0.1, le=2.0)
    truckCapacity: int = Field(default=30, ge=20, le=50)
    season: Season = Field(default=Season.POST_HARVEST)

class AdvancedSeasonConfig(BaseModel):
    harvestWindows: Optional[Dict] = None
    storage: Optional[Dict] = None
    demandPatterns: Optional[Dict] = None

class AdvancedTransportConfig(BaseModel):
    baseCostPerKm: float = 0.5
    fuelSurcharges: Optional[Dict] = None
    roadQualityMultipliers: Optional[Dict] = None
    borderCrossing: Optional[Dict] = None
    weighbridgeAvoidance: bool = False

class AdvancedFleetConfig(BaseModel):
    vehicleTypes: Optional[Dict] = None
    fleetAvailability: Optional[Dict] = None
    backhaul: Optional[Dict] = None

class AdvancedConfiguration(BaseModel):
    season: Optional[AdvancedSeasonConfig] = None
    transportCost: Optional[AdvancedTransportConfig] = None
    fleetMix: Optional[AdvancedFleetConfig] = None

class InfrastructureConfig(BaseModel):
    showSilos: bool = False
    showWeighbridges: bool = False
    showPorts: bool = False
    showBorders: bool = False
    showRoadCorridors: bool = False
    capacityLimits: Optional[Dict] = None
    roadConstraints: Optional[Dict] = None

class ModelRequest(BaseModel):
    parameters: GravityModelParameters
    advancedConfig: Optional[AdvancedConfiguration] = None
    infrastructureConfig: Optional[InfrastructureConfig] = None

class FlowResult(BaseModel):
    origin: str
    destination: str
    commodity: str
    volume: float  # tonnes
    trucks: int
    cost: float  # rand
    distance: float  # km

class ModelResponse(BaseModel):
    flows: List[FlowResult]
    totalVolume: float
    totalCost: float
    totalTrucks: int
    averageDistance: float
    executionTime: float  # seconds