"""Agent ELO with load/save."""
import json
from dataclasses import dataclass, asdict
from pathlib import Path

K_AGENT = 16
DATA_FILE = Path(__file__).parent.parent.parent / "data" / "elo_state.json"

@dataclass
class Agent:
    id: str
    name: str
    office: str
    elo: float = 1500.0
    deals_closed: int = 0
    avg_sale_to_list: float = 1.0
    avg_dom: int = 0
    active_listings: int = 0

def update_agent(a: Agent, sale_price: float, list_price: float, dom: int):
    """Update ELO after a closed deal. Overpricing = negative (bad for buyer)."""
    sale_to_list = sale_price / list_price if list_price else 1.0
    delta = (sale_to_list - 1.0) * 10
    a.elo -= K_AGENT * delta
    a.deals_closed += 1
    a.avg_sale_to_list = a.avg_sale_to_list * 0.9 + sale_to_list * 0.1
    a.avg_dom = int(a.avg_dom * 0.9 + dom * 0.1)

def load_agents() -> dict[str, Agent]:
    if not DATA_FILE.exists():
        return {}
    try:
        with open(DATA_FILE) as f:
            raw = json.load(f).get("agents", {})
        return {k: Agent(**v) for k, v in raw.items()}
    except Exception:
        return {}

def save_agents(agents: dict[str, Agent]):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE) as f:
                existing = json.load(f)
        except Exception:
            pass
    existing["agents"] = {k: asdict(v) for k, v in agents.items()}
    with open(DATA_FILE, "w") as f:
        json.dump(existing, f, indent=2)
