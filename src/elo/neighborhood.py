"""Neighborhood ELO with load/save. Persists to data/elo_state.json."""
import json
from dataclasses import dataclass, asdict
from pathlib import Path

K_NEIGHBORHOOD = 32
DATA_FILE = Path(__file__).parent.parent.parent / "data" / "elo_state.json"

@dataclass
class Neighborhood:
    name: str
    county: str
    lat: float
    lon: float
    elo: float = 1500.0
    expected_price_total: float = 0.0
    expected_price_sqft: float = 0.0
    inventory: int = 0
    months_of_supply: float = 0.0
    dom_median: int = 0
    sales_90d: int = 0

def update_neighborhood(n: Neighborhood, sale_price: float, sale_sqft: float):
    """Update ELO after a closed sale. Only called on Closed status sales."""
    expected = n.expected_price_total
    actual = sale_price
    if expected <= 0:
        n.expected_price_total = actual
        n.expected_price_sqft = sale_price / sale_sqft if sale_sqft else 0
        n.sales_90d += 1
        return
    expected_win = expected / (expected + actual)
    result = 1.0 if actual > expected else (0.0 if actual < expected else 0.5)
    n.elo += K_NEIGHBORHOOD * (result - expected_win)
    n.expected_price_total = n.expected_price_total * 0.9 + actual * 0.1
    n.expected_price_sqft = n.expected_price_sqft * 0.9 + (sale_price / sale_sqft if sale_sqft else 0) * 0.1
    n.sales_90d += 1

def load_neighborhoods() -> dict[str, Neighborhood]:
    if not DATA_FILE.exists():
        return _seed_neighborhoods()
    try:
        with open(DATA_FILE) as f:
            raw = json.load(f).get("neighborhoods", {})
        return {k: Neighborhood(**v) for k, v in raw.items()}
    except Exception:
        return _seed_neighborhoods()

def _seed_neighborhoods() -> dict[str, Neighborhood]:
    """Minimal seed so the desk has something to start with."""
    seeds = [
        Neighborhood("Salt Lake City", "Salt Lake", 40.7608, -111.8910),
        Neighborhood("Provo", "Utah", 40.2338, -111.6585),
        Neighborhood("Ogden", "Weber", 41.2230, -111.9738),
        Neighborhood("St. George", "Washington", 37.0965, -113.5684),
        Neighborhood("Draper", "Salt Lake", 40.5247, -111.8638),
        Neighborhood("Millcreek", "Salt Lake", 40.6900, -111.8500),
    ]
    return {n.name: n for n in seeds}

def save_neighborhoods(neighborhoods: dict[str, Neighborhood]):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    raw = {"neighborhoods": {k: asdict(v) for k, v in neighborhoods.items()}}
    with open(DATA_FILE, "w") as f:
        json.dump(raw, f, indent=2)
