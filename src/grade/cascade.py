"""The one grade tree. Mirrors the sports gradeBase pattern."""
from src.elo.engine import Grade
from src.elo.neighborhood import Neighborhood
from src.elo.agent import Agent
from src.elo.macro import MacroState, macro_flags

def grade_property(listing: dict, neighborhood: Neighborhood, agent: Agent, macro: MacroState) -> Grade:
    price = listing.get("ListPrice", 0) or 0
    expected = neighborhood.expected_price_total
    gap_pct = (price - expected) / expected if expected > 0 else 0

    # Distressed / short sale heuristic
    remarks = (listing.get("PublicRemarks") or listing.get("Remarks") or "").lower()
    if any(kw in remarks for kw in ("short sale", "foreclosure", "estate sale", "probate")):
        return Grade(
            call="DISTRESSED",
            side=listing.get("StreetName", ""),
            line=f"${price:,} (ARV ~${int(expected or price * 1.1):,})",
            why="Distressed indicator in remarks. Seller may be motivated. Verify with title.",
            anomalies=["Distressed keywords"],
            weight=2,
            row=listing,
        )

    # Agent overpricing pattern
    if agent.elo < 1450 and gap_pct > 0.12:
        return Grade(
            call="FADE",
            side=listing.get("StreetName", ""),
            line=f"${price:,} (+{gap_pct*100:.0f}% vs ELO)",
            why=f"Agent {agent.name} (ELO {agent.elo:.0f}) shows overpricing pattern. "
                f"Listing is {gap_pct*100:.0f}% above neighborhood ELO.",
            anomalies=[f"Agent ELO {agent.elo:.0f}", f"+{gap_pct*100:.0f}% vs ELO"],
            weight=2,
            row=listing,
        )

    # Neighborhood mispricing
    if gap_pct < -0.10 and not macro.rates_rising:
        return Grade(
            call="BUY",
            side=listing.get("StreetName", ""),
            line=f"${price:,} ({gap_pct*100:.0f}% vs ELO)",
            why=f"Priced {abs(gap_pct)*100:.0f}% below neighborhood ELO. Rates stable.",
            anomalies=[f"{gap_pct*100:.0f}% below ELO"],
            weight=1,
            row=listing,
        )
    if gap_pct > 0.15 and macro.inventory_rising:
        return Grade(
            call="FADE",
            side=listing.get("StreetName", ""),
            line=f"${price:,} (+{gap_pct*100:.0f}% vs ELO)",
            why=f"{gap_pct*100:.0f}% above ELO while inventory is rising.",
            anomalies=[f"+{gap_pct*100:.0f}% vs ELO", "Inventory rising"],
            weight=2,
            row=listing,
        )

    # Macro stack
    notes, weight = macro_flags(macro)
    if weight >= 3:
        return Grade(
            call="HOLD",
            side=listing.get("StreetName", ""),
            line=f"${price:,}",
            why=f"Macro headwind stack: {', '.join(notes)}.",
            anomalies=notes,
            weight=weight,
            row=listing,
        )

    # Sharp agent + fair price
    if agent.elo >= 1550 and abs(gap_pct) <= 0.03:
        return Grade(
            call="STANDARD",
            side=listing.get("StreetName", ""),
            line=f"${price:,} (fair)",
            why=f"Sharp agent (ELO {agent.elo:.0f}), price near ELO. No edge.",
            anomalies=[],
            weight=0,
            row=listing,
        )

    return Grade(
        call="STANDARD",
        side=listing.get("StreetName", ""),
        line=f"${price:,}",
        why="No schematic anomaly detected.",
        anomalies=[],
        weight=0,
        row=listing,
    )
