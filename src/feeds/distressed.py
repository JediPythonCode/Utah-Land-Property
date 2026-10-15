"""
Distressed, foreclosure, short-sale, and REO signals for Utah.

Primary free source: HUD FHA Single Family REO FeatureServer (public ArcGIS).
Filtered to STATE_CODE = 'UT'.

Falls back to empty list on any error so the desk continues.
"""
import logging
import requests
from typing import Any

logger = logging.getLogger("utah-desk.distressed")

HUD_REO_URL = (
    "https://services.arcgis.com/VTyQ9soqVukalItT/arcgis/rest/services/SF_REO/FeatureServer/0/query"
)

def pull_hud_reo_utah(limit: int = 200) -> list[dict[str, Any]]:
    """Pull active HUD REO properties in Utah."""
    params = {
        "where": "STATE_CODE = 'UT'",
        "outFields": "*",
        "returnGeometry": "true",
        "f": "json",
        "resultRecordCount": limit,
    }
    try:
        r = requests.get(HUD_REO_URL, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        features = data.get("features", [])
        rows = []
        for f in features:
            attrs = f.get("attributes", {})
            geom = f.get("geometry") or {}
            rows.append({
                "source": "HUD REO",
                "type": "REO",
                "id": attrs.get("CASE_NUM"),
                "address": f"{attrs.get('STREET_NUM', '')} {attrs.get('STREET_NAME', '')}".strip(),
                "city": attrs.get("CITY", ""),
                "state": "UT",
                "price": attrs.get("LIST_PRICE") or attrs.get("PRICE"),
                "beds": attrs.get("BEDROOMS"),
                "baths": attrs.get("BATHROOMS"),
                "sqft": attrs.get("SQUARE_FEET"),
                "lat": geom.get("y"),
                "lon": geom.get("x"),
                "status": "REO",
                "note": "HUD REO — bank-owned foreclosure inventory",
            })
        logger.info(f"HUD REO Utah: {len(rows)} properties")
        return rows
    except Exception as e:
        logger.warning(f"HUD REO pull failed: {e}")
        return []

def pull_distressed_utah() -> list[dict[str, Any]]:
    """Aggregate distressed signals. Currently HUD REO; extend with other free sources."""
    return pull_hud_reo_utah()
