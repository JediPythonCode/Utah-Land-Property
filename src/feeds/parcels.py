"""
Public parcel / assessor signals for raw or vacant land not on the MLS.

Uses the free UGRC Salt Lake County LIR FeatureServer.
Filters for parcels with low or zero building square footage (potential raw/vacant land).

Extend with other county LIR endpoints the same way.
Falls back to empty list on error.
"""
import logging
import requests
from typing import Any

logger = logging.getLogger("utah-desk.parcels")

SLCO_LIR_URL = (
    "https://services1.arcgis.com/99lidPhWCzftIe9K/ArcGIS/rest/services/Parcels_SaltLake_LIR/FeatureServer/0/query"
)

def pull_vacant_land_slco(limit: int = 150) -> list[dict[str, Any]]:
    """Pull parcels in Salt Lake County with little or no building (raw/vacant candidates)."""
    # PROP_CLASS or BLDG_SQFT = 0 / null indicates potential vacant or raw land
    params = {
        "where": "BLDG_SQFT IS NULL OR BLDG_SQFT = 0 OR PROP_CLASS LIKE '%Vacant%'",
        "outFields": "PARCEL_ID,PARCEL_ADD,PARCEL_CITY,LAND_MKT_VALUE,TOTAL_MKT_VALUE,PARCEL_ACRES,PROP_CLASS,BLDG_SQFT",
        "returnGeometry": "true",
        "f": "json",
        "resultRecordCount": limit,
    }
    try:
        r = requests.get(SLCO_LIR_URL, params=params, timeout=25)
        r.raise_for_status()
        data = r.json()
        features = data.get("features", [])
        rows = []
        for f in features:
            attrs = f.get("attributes", {})
            geom = f.get("geometry") or {}
            # Centroid approximation if rings present
            lat = lon = None
            rings = geom.get("rings")
            if rings and rings[0]:
                pts = rings[0]
                lon = sum(p[0] for p in pts) / len(pts)
                lat = sum(p[1] for p in pts) / len(pts)
            acres = attrs.get("PARCEL_ACRES") or 0
            land_val = attrs.get("LAND_MKT_VALUE") or 0
            rows.append({
                "source": "Public Parcel",
                "type": "RAW_LAND",
                "id": attrs.get("PARCEL_ID"),
                "address": attrs.get("PARCEL_ADD") or "Raw land",
                "city": attrs.get("PARCEL_CITY") or "Salt Lake County",
                "state": "UT",
                "price": land_val,
                "acres": acres,
                "sqft": 0,
                "prop_class": attrs.get("PROP_CLASS"),
                "lat": lat,
                "lon": lon,
                "status": "Off-Market / Vacant",
                "note": f"Public parcel record. {acres:.1f} acres. Not listed on MLS. Potential raw land.",
            })
        logger.info(f"SLCO vacant/raw parcels: {len(rows)}")
        return rows
    except Exception as e:
        logger.warning(f"Parcel pull failed: {e}")
        return []

def pull_raw_land_utah() -> list[dict[str, Any]]:
    """Aggregate raw/vacant land signals from public parcel records."""
    return pull_vacant_land_slco()
