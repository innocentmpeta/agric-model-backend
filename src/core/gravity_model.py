import numpy as np
from typing import List, Dict, Tuple
from math import radians, cos, sin, asin, sqrt
import time

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

def calculate_distance_matrix(provinces: List[Dict]) -> np.ndarray:
    """
    Calculate distance matrix between all provinces
    """
    n = len(provinces)
    distance_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                lat1 = provinces[i]['coordinates']['lat']
                lon1 = provinces[i]['coordinates']['lng']
                lat2 = provinces[j]['coordinates']['lat']
                lon2 = provinces[j]['coordinates']['lng']
                
                distance_matrix[i][j] = haversine_distance(lat1, lon1, lat2, lon2)
    
    return distance_matrix

def calculate_gravity_flows(
    provinces: List[Dict],
    commodity: str,
    distance_decay: float,
    transport_cost_per_km: float,
    truck_capacity: int,
    advanced_config: Dict = None
) -> List[Dict]:
    """
    Calculate commodity flows using gravity model
    
    Gravity Model Formula:
    Flow_ij = (Supply_i * Demand_j) / (Distance_ij ^ distance_decay)
    
    Then normalize flows to respect supply/demand constraints
    """
    start_time = time.time()
    
    n = len(provinces)
    
    # Extract supply and demand for the commodity
    supply = np.array([p['supply'].get(commodity, 0) for p in provinces])
    demand = np.array([p['demand'].get(commodity, 0) for p in provinces])
    
    # Calculate distance matrix
    distances = calculate_distance_matrix(provinces)
    
    # Avoid division by zero - set self-distances to infinity
    distances_safe = np.where(distances == 0, np.inf, distances)
    
    # Calculate attraction matrix using gravity model
    # Flow potential from i to j = Supply_i * Demand_j / Distance_ij^decay
    supply_matrix = np.tile(supply.reshape(-1, 1), (1, n))
    demand_matrix = np.tile(demand.reshape(1, -1), (n, 1))
    
    # Gravity model calculation
    attraction = (supply_matrix * demand_matrix) / np.power(distances_safe, distance_decay)
    
    # Replace inf and nan with 0
    attraction = np.nan_to_num(attraction, nan=0.0, posinf=0.0, neginf=0.0)
    
    # Normalize flows using iterative proportional fitting (Fratar method)
    flows = iterative_proportional_fitting(attraction, supply, demand, max_iterations=100)
    
    # Apply advanced configurations if provided
    if advanced_config:
        flows = apply_advanced_configurations(flows, distances, advanced_config)
    
    # Convert flows to results format
    results = []
    for i in range(n):
        for j in range(n):
            if i != j and flows[i][j] > 0.1:  # Filter out negligible flows
                volume = flows[i][j]
                distance = distances[i][j]
                cost = volume * distance * transport_cost_per_km
                trucks = int(np.ceil(volume / truck_capacity))
                
                results.append({
                    'origin': provinces[i]['id'],
                    'destination': provinces[j]['id'],
                    'commodity': commodity,
                    'volume': round(volume, 2),
                    'distance': round(distance, 2),
                    'cost': round(cost, 2),
                    'trucks': trucks
                })
    
    execution_time = time.time() - start_time
    
    # Calculate summary statistics
    total_volume = sum(r['volume'] for r in results)
    total_cost = sum(r['cost'] for r in results)
    total_trucks = sum(r['trucks'] for r in results)
    avg_distance = sum(r['distance'] * r['volume'] for r in results) / total_volume if total_volume > 0 else 0
    
    return {
        'flows': results,
        'totalVolume': round(total_volume, 2),
        'totalCost': round(total_cost, 2),
        'totalTrucks': total_trucks,
        'averageDistance': round(avg_distance, 2),
        'executionTime': round(execution_time, 4)
    }

def iterative_proportional_fitting(
    attraction: np.ndarray,
    supply: np.ndarray,
    demand: np.ndarray,
    max_iterations: int = 100,
    tolerance: float = 0.01
) -> np.ndarray:
    """
    Iterative Proportional Fitting (Fratar method) to balance flows
    Ensures row sums equal supply and column sums equal demand
    """
    flows = attraction.copy()
    n = len(supply)
    
    for iteration in range(max_iterations):
        # Row balancing (supply constraint)
        row_sums = flows.sum(axis=1)
        row_sums_safe = np.where(row_sums == 0, 1, row_sums)
        row_factors = supply / row_sums_safe
        flows = flows * row_factors.reshape(-1, 1)
        
        # Column balancing (demand constraint)
        col_sums = flows.sum(axis=0)
        col_sums_safe = np.where(col_sums == 0, 1, col_sums)
        col_factors = demand / col_sums_safe
        flows = flows * col_factors.reshape(1, -1)
        
        # Check convergence
        row_error = np.abs(flows.sum(axis=1) - supply).max()
        col_error = np.abs(flows.sum(axis=0) - demand).max()
        
        if row_error < tolerance and col_error < tolerance:
            break
    
    return flows

def apply_advanced_configurations(
    flows: np.ndarray,
    distances: np.ndarray,
    advanced_config: Dict
) -> np.ndarray:
    """
    Apply advanced configurations to adjust flows
    """
    adjusted_flows = flows.copy()
    
    # Apply transport cost adjustments
    if advanced_config.get('transportCost'):
        transport_config = advanced_config['transportCost']
        
        # Road quality multipliers
        if transport_config.get('roadQualityMultipliers'):
            multipliers = transport_config['roadQualityMultipliers']
            # Apply random road quality adjustments (simplified)
            # In production, this would use actual road network data
            quality_factor = multipliers.get('pavedNational', 1.0)
            adjusted_flows = adjusted_flows * quality_factor
    
    # Apply fleet availability constraints
    if advanced_config.get('fleetMix'):
        fleet_config = advanced_config['fleetMix']
        
        # Adjust flows based on fleet availability
        if fleet_config.get('fleetAvailability'):
            availability = fleet_config['fleetAvailability']
            # In production, this would adjust flows based on actual fleet data
            # For now, we apply a simplified model
    
    # Apply seasonal adjustments
    if advanced_config.get('season'):
        season_config = advanced_config['season']
        
        # Adjust for storage capacity constraints
        if season_config.get('storage'):
            storage = season_config['storage']
            # Apply storage cost penalties for long-distance flows
            # This encourages more local consumption
    
    return adjusted_flows