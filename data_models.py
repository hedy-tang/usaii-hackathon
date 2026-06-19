from dataclasses import dataclass
from typing import List, Dict, Optional


# =========================================================
# CORE CLAIM STRUCTURE
# =========================================================

@dataclass
class Claim:
    claim: str
    entity: str
    source_type: str        # official / social / unknown
    certainty: str          # high / medium / low

    # computed later
    embedding: Optional[list] = None
    contradiction_count: int = 0
    contradiction_severity: float = 0.0
    embedding_variance: float = 0.0
    confidence_score: float = 0.0
    explanation: str = ""



# =========================================================
# SAMPLE DATA
# =========================================================

CLAIMS = [

    # =====================================================
    # SCHOOL EVENT
    # =====================================================

    Claim("school will be closed tomorrow due to weather", "school_closure", "social", "high"),
    Claim("district confirms schools remain open", "school_closure", "official", "high"),
    Claim("all classes will move online tomorrow", "school_closure", "news", "medium"),
    Claim("students should avoid campus due to severe weather", "school_closure", "official", "high"),
    Claim("weather conditions are not expected to affect schools", "school_closure", "news", "medium"),
    Claim("district plans to announce closure decision tonight", "school_closure", "official", "medium"),

    Claim("bus transportation services are canceled", "school_transportation", "official", "high"),
    Claim("school buses will operate on normal schedule", "school_transportation", "social", "medium"),

    Claim("after-school activities have been canceled", "school_activities", "official", "high"),
    Claim("all sports practices will continue as scheduled", "school_activities", "social", "medium"),

    # =====================================================
    # WILDFIRE EVENT
    # =====================================================

    Claim("fire is spreading near downtown area", "wildfire_fire_status", "social", "high"),
    Claim("official report says fire is 40 percent contained", "wildfire_fire_status", "official", "medium"),
    Claim("fire has reached residential neighborhoods", "wildfire_fire_status", "social", "high"),
    Claim("fire remains outside residential zones", "wildfire_fire_status", "official", "high"),

    Claim("evacuation warning issued for east district", "wildfire_evacuation", "official", "high"),
    Claim("no evacuation warning has been issued", "wildfire_evacuation", "social", "medium"),

    Claim("road 17 is closed due to wildfire activity", "wildfire_road_status", "official", "high"),
    Claim("road 17 remains open to traffic", "wildfire_road_status", "social", "medium"),

    Claim("air quality levels are hazardous", "wildfire_air_quality", "official", "high"),
    Claim("air quality is improving throughout the region", "wildfire_air_quality", "social", "low"),

    # =====================================================
    # EVACUATION EVENT
    # =====================================================

    Claim("evacuation order issued for river valley", "evacuation_orders", "official", "high"),
    Claim("residents are safe to stay home", "evacuation_orders", "social", "medium"),
    Claim("mandatory evacuation begins at 6 PM", "evacuation_orders", "official", "high"),
    Claim("evacuation orders have been lifted", "evacuation_orders", "social", "medium"),
    Claim("residents should leave immediately", "evacuation_orders", "official", "high"),
    Claim("authorities advise remaining indoors", "evacuation_orders", "social", "medium"),

    Claim("local shelters are open for displaced residents", "evacuation_shelters", "official", "high"),
    Claim("shelters have reached full capacity", "evacuation_shelters", "news", "medium"),

    Claim("emergency services are assisting evacuations", "evacuation_operations", "official", "high"),
    Claim("roads are too congested for evacuation", "evacuation_operations", "social", "medium"),

    # =====================================================
    # FLOOD EVENT
    # =====================================================

    Claim("river levels are rising rapidly", "flood_water_level", "official", "high"),
    Claim("river levels remain stable", "flood_water_level", "social", "medium"),

    Claim("flood warning issued for northern communities", "flood_warning", "official", "high"),
    Claim("flood threat has passed", "flood_warning", "social", "medium"),

    Claim("water has entered several homes", "flood_damage", "news", "high"),
    Claim("no residential flooding has been reported", "flood_damage", "official", "medium"),
    Claim("residents report severe street flooding", "flood_damage", "social", "high"),

    Claim("sandbag stations have opened", "flood_preparation", "official", "high"),

    Claim("roads near the river are closed", "flood_road_status", "official", "high"),
    Claim("all major roads remain open", "flood_road_status", "social", "medium"),

    # =====================================================
    # PUBLIC HEALTH EVENT
    # =====================================================

    Claim("water contamination detected in city supply", "health_water_safety", "official", "high"),
    Claim("tap water is safe to drink", "health_water_safety", "social", "medium"),
    Claim("boil water advisory has been issued", "health_water_safety", "official", "high"),
    Claim("boil water advisory has been lifted", "health_water_safety", "social", "medium"),
    Claim("residents report unusual taste in water", "health_water_safety", "social", "medium"),
    Claim("laboratory tests confirm contamination", "health_water_safety", "official", "high"),
    Claim("testing found no harmful substances", "health_water_safety", "news", "medium"),

    Claim("bottled water distribution centers are open", "health_response", "official", "high"),

    Claim("local hospitals report increased illness", "health_illness", "news", "medium"),
    Claim("health officials report no unusual illness patterns", "health_illness", "official", "high"),

    # =====================================================
    # TRANSPORTATION EVENT
    # =====================================================

    Claim("major highway closed due to accident", "transport_highway_status", "official", "high"),
    Claim("highway remains open in both directions", "transport_highway_status", "social", "medium"),
    Claim("accident scene has been cleared", "transport_highway_status", "news", "medium"),

    Claim("traffic delays exceed two hours", "transport_traffic", "news", "medium"),
    Claim("traffic conditions are normal", "transport_traffic", "social", "medium"),
    Claim("alternate routes are recommended", "transport_traffic", "official", "high"),
    Claim("commuters should avoid downtown", "transport_traffic", "official", "high"),

    Claim("rail service has been suspended", "transport_rail_status", "official", "high"),
    Claim("rail service is operating normally", "transport_rail_status", "social", "medium"),

    Claim("all transit systems remain unaffected", "transport_system_status", "social", "medium"),
    Claim("Calimesa, California - 06/15/2026 - Shore Fire near Riverside County at 500+ acres, evacuations and crews added", "wildfire_fire_status", "social", "high"),
    Claim("Calimesa, California - 06/15/2026 - Shore Fire near Riverside County at 500+ acres, evacuations and crews added", "wildfire_fire_status", "social", "medium"),
    Claim("[Local] - 06/16/2026 - Stretch of 60 Freeway remains closed, evacuation orders issued due to Shore Fire in Riverside County | NY Post", "wildfire_fire_status", "news", "high"),
]

# =========================================================
# HELPERS
# =========================================================

def to_dict_list(claims: List[Claim]) -> List[Dict]:
    return [c.__dict__ for c in claims]


    Claim("Calimesa, California - 06/15/2026 - Shore Fire near Riverside County at 500+ acres, evacuations and crews added", "wildfire_fire_status", "social", "low"),
    Claim("Calimesa, California - 06/15/2026 - Shore Fire near Riverside County at 500+ acres, evacuations and crews added", "wildfire_fire_status", "social", "low"),
    Claim("[Local] - 06/16/2026 - Stretch of 60 Freeway remains closed, evacuation orders issued due to Shore Fire in Riverside County | NY Post", "wildfire_fire_status", "social", "low"),
