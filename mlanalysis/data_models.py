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
    Claim("school will be closed tomorrow due to weather", "school", "social", "high"),
    Claim("district confirms schools remain open", "school", "official", "high"),
    Claim("fire is spreading near downtown area", "wildfire", "social", "high"),
    Claim("official report says fire is 40 percent contained", "wildfire", "official", "medium"),
    Claim("evacuation order issued for river valley", "evacuation", "official", "high"),
    Claim("residents are safe to stay home", "evacuation", "social", "medium"),
]


# =========================================================
# HELPERS
# =========================================================

def to_dict_list(claims: List[Claim]) -> List[Dict]:
    return [c.__dict__ for c in claims]
