"""Macro state built from confirmed FRED series."""
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class MacroState:
    rate_30yr: float = 0.0
    rate_change_30d: float = 0.0
    unemployment_ut: float = 0.0
    ue_change_3mo: float = 0.0
    hpi_utah: float = 0.0
    hpi_slc: float = 0.0
    median_list_price: float = 0.0
    months_of_supply: float = 0.0
    inventory_change_pct: float = 0.0
    rates_rising: bool = False
    inventory_rising: bool = False
    ue_rising: bool = False
    last_updated: str = ""
    news_flags: list[str] = field(default_factory=list)

def compute_macro(fred_data: dict, inventory_now: int, inventory_prior: int) -> MacroState:
    rates = fred_data.get("rate_30yr", [])
    rate_now = rates[-1]["value"] if rates else 0.0
    rate_30d = rates[0]["value"] if len(rates) > 4 else rate_now
    rate_change = rate_now - rate_30d

    ue = fred_data.get("unemployment_ut", [])
    ue_now = ue[-1]["value"] if ue else 0.0
    ue_3mo = ue[0]["value"] if len(ue) > 3 else ue_now
    ue_change = ue_now - ue_3mo

    hpi_ut = fred_data.get("hpi_utah", [])
    hpi_slc = fred_data.get("hpi_slc_msa", [])
    hpi_ut_val = hpi_ut[-1]["value"] if hpi_ut else 0.0
    hpi_slc_val = hpi_slc[-1]["value"] if hpi_slc else 0.0

    mlp = fred_data.get("median_list_price_ut", [])
    mlp_val = mlp[-1]["value"] if mlp else 0.0

    inv_change = ((inventory_now - inventory_prior) / inventory_prior * 100) if inventory_prior > 0 else 0.0

    return MacroState(
        rate_30yr=rate_now,
        rate_change_30d=rate_change,
        unemployment_ut=ue_now,
        ue_change_3mo=ue_change,
        hpi_utah=hpi_ut_val,
        hpi_slc=hpi_slc_val,
        median_list_price=mlp_val,
        inventory_change_pct=inv_change,
        rates_rising=rate_change > 0.10,
        inventory_rising=inv_change > 10,
        ue_rising=ue_change > 0.2,
        last_updated=datetime.now(timezone.utc).isoformat(),
    )

def macro_flags(m: MacroState) -> tuple[list[str], int]:
    notes = []
    weight = 0
    if m.ue_rising:
        notes.append(f"UE rising (+{m.ue_change_3mo:.1f}pp in 3mo)")
        weight += 1
    if m.rates_rising:
        notes.append(f"Rates up +{m.rate_change_30d:.2f}% in 30d")
        weight += 1
    if m.inventory_rising:
        notes.append(f"Inventory +{m.inventory_change_pct:.0f}% in 30d")
        weight += 1
    if m.months_of_supply > 6:
        notes.append(f"MoS {m.months_of_supply:.1f} (buyer's market)")
        weight += 1
    return notes, weight
