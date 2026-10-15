#!/usr/bin/env python3
"""Scrape free public Utah property sources into data/signals.json."""
import json
import random
from datetime import datetime, timezone
from pathlib import Path
import requests

OUT = Path(__file__).parent.parent / "data" / "signals.json"

LAND_IMAGES = [
    "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=600&q=70",
    "https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=600&q=70",
    "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=600&q=70",
    "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=600&q=70",
    "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=600&q=70",
]

def pull_slco_parcels(limit=200):
    url = "https://services1.arcgis.com/99lidPhWCzftIe9K/ArcGIS/rest/services/Parcels_SaltLake_LIR/FeatureServer/0/query"
    params = {
        "where": "BLDG_SQFT IS NULL OR BLDG_SQFT = 0 OR PROP_CLASS LIKE '%Vacant%'",
        "outFields": "PARCEL_ID,PARCEL_ADD,PARCEL_CITY,LAND_MKT_VALUE,PARCEL_ACRES,PROP_CLASS",
        "returnGeometry": "true",
        "f": "json",
        "resultRecordCount": limit,
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        features = r.json().get("features", [])
        rows = []
        for f in features:
            attrs = f.get("attributes", {})
            geom = f.get("geometry") or {}
            lat = lon = None
            rings = geom.get("rings")
            if rings and rings[0]:
                pts = rings[0]
                lon = sum(p[0] for p in pts) / len(pts)
                lat = sum(p[1] for p in pts) / len(pts)
            acres = attrs.get("PARCEL_ACRES") or 0
            rows.append({
                "call": "RAWLAND",
                "source": "Raw Land",
                "price": attrs.get("LAND_MKT_VALUE") or 0,
                "address": attrs.get("PARCEL_ADD") or "Raw land",
                "city": attrs.get("PARCEL_CITY") or "Salt Lake County",
                "beds": 0, "baths": 0, "sqft": 0,
                "why": f"Public parcel. {acres:.1f} acres. Not listed.",
                "lat": lat, "lon": lon,
                "acres": acres,
                "img": random.choice(LAND_IMAGES),
            })
        return rows
    except Exception as e:
        print(f"SLCO error: {e}")
        return []

def pull_gov_parcels(limit=100):
    url = "https://services1.arcgis.com/99lidPhWCzftIe9K/ArcGIS/rest/services/cadastre_government_owned_parcels/FeatureServer/0/query"
    params = {
        "where": "1=1",
        "outFields": "PARCEL_ID,PARCEL_ADD,COUNTY_NAME,Category",
        "returnGeometry": "true",
        "f": "json",
        "resultRecordCount": limit,
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        features = r.json().get("features", [])
        rows = []
        for f in features[:limit]:
            attrs = f.get("attributes", {})
            geom = f.get("geometry") or {}
            lat = lon = None
            rings = geom.get("rings")
            if rings and rings[0]:
                pts = rings[0]
                lon = sum(p[0] for p in pts) / len(pts)
                lat = sum(p[1] for p in pts) / len(pts)
            rows.append({
                "call": "RAWLAND",
                "source": "Gov Parcel",
                "price": 0,
                "address": attrs.get("PARCEL_ADD") or "Government parcel",
                "city": attrs.get("COUNTY_NAME") or "Utah",
                "beds": 0, "baths": 0, "sqft": 0,
                "why": f"Government-owned. {attrs.get('Category', '')}",
                "lat": lat, "lon": lon,
                "img": random.choice(LAND_IMAGES),
            })
        return rows
    except Exception as e:
        print(f"Gov parcels error: {e}")
        return []

def main():
    rows = pull_slco_parcels() + pull_gov_parcels()
    # Deduplicate by address
    seen = set()
    unique = []
    for r in rows:
        key = (r["address"], r["city"])
        if key not in seen:
            seen.add(key)
            unique.append(r)
    out = {"updated": datetime.now(timezone.utc).isoformat(), "rows": unique}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(f"Wrote {len(unique)} signals to {OUT}")

if __name__ == "__main__":
    main()
