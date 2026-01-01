from typing import List, Dict

def load_provinces_data() -> List[Dict]:
    """
    Load province data with supply and demand
    In production, this would load from a database or file
    """
    return [
        {
            'id': 'GP',
            'name': 'Gauteng',
            'coordinates': {'lat': -26.2708, 'lng': 28.1123},
            'supply': {'maize': 2500000, 'wheat': 150000},
            'demand': {'maize': 4500000, 'wheat': 800000},
        },
        {
            'id': 'FS',
            'name': 'Free State',
            'coordinates': {'lat': -28.4541, 'lng': 26.7968},
            'supply': {'maize': 5500000, 'wheat': 450000},
            'demand': {'maize': 1200000, 'wheat': 200000},
        },
        {
            'id': 'MP',
            'name': 'Mpumalanga',
            'coordinates': {'lat': -25.5653, 'lng': 30.5279},
            'supply': {'maize': 3200000, 'wheat': 50000},
            'demand': {'maize': 1100000, 'wheat': 150000},
        },
        {
            'id': 'NW',
            'name': 'North West',
            'coordinates': {'lat': -26.6638, 'lng': 25.2837},
            'supply': {'maize': 2800000, 'wheat': 180000},
            'demand': {'maize': 900000, 'wheat': 120000},
        },
        {
            'id': 'LP',
            'name': 'Limpopo',
            'coordinates': {'lat': -23.4013, 'lng': 29.4179},
            'supply': {'maize': 800000, 'wheat': 20000},
            'demand': {'maize': 1500000, 'wheat': 180000},
        },
        {
            'id': 'KZN',
            'name': 'KwaZulu-Natal',
            'coordinates': {'lat': -28.5305, 'lng': 30.8958},
            'supply': {'maize': 1500000, 'wheat': 30000},
            'demand': {'maize': 2800000, 'wheat': 400000},
        },
        {
            'id': 'EC',
            'name': 'Eastern Cape',
            'coordinates': {'lat': -32.2968, 'lng': 26.4194},
            'supply': {'maize': 600000, 'wheat': 80000},
            'demand': {'maize': 1800000, 'wheat': 250000},
        },
        {
            'id': 'WC',
            'name': 'Western Cape',
            'coordinates': {'lat': -33.2277, 'lng': 21.8569},
            'supply': {'maize': 300000, 'wheat': 750000},
            'demand': {'maize': 1600000, 'wheat': 900000},
        },
        {
            'id': 'NC',
            'name': 'Northern Cape',
            'coordinates': {'lat': -29.0467, 'lng': 21.8569},
            'supply': {'maize': 200000, 'wheat': 100000},
            'demand': {'maize': 300000, 'wheat': 80000},
        },
    ]

def load_distance_matrix() -> Dict:
    """
    Load pre-calculated distance matrix
    In production, this could be cached or loaded from file
    """
    # This will be calculated dynamically by the gravity model
    return {}