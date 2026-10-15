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


def mercator_to_latlon(x, y):
    import math
    lon = x / 20037508.34 * 180
    lat = y / 20037508.34 * 180
    lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180)) - math.pi / 2)
    return lat, lon

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
                mx = sum(p[0] for p in pts) / len(pts)
                my = sum(p[1] for p in pts) / len(pts)
                lat, lon = mercator_to_latlon(mx, my)
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
                mx = sum(p[0] for p in pts) / len(pts)
                my = sum(p[1] for p in pts) / len(pts)
                lat, lon = mercator_to_latlon(mx, my)
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



def pull_county_lir(county, limit=100):
    """Pull vacant/raw parcels from a county LIR FeatureServer."""
    url = f"https://services1.arcgis.com/99lidPhWCzftIe9K/ArcGIS/rest/services/Parcels_{county}_LIR/FeatureServer/0/query"
    params = {
        "where": "BLDG_SQFT IS NULL OR BLDG_SQFT = 0 OR PROP_CLASS LIKE '%Vacant%' OR PROP_CLASS LIKE '%Agricultural%'",
        "outFields": "PARCEL_ID,PARCEL_ADD,PARCEL_CITY,LAND_MKT_VALUE,PARCEL_ACRES,PROP_CLASS,COUNTY_NAME",
        "returnGeometry": "true",
        "f": "json",
        "resultRecordCount": limit,
    }
    try:
        r = requests.get(url, params=params, timeout=25)
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
                mx = sum(p[0] for p in pts) / len(pts)
                my = sum(p[1] for p in pts) / len(pts)
                lat, lon = mercator_to_latlon(mx, my)
            acres = attrs.get("PARCEL_ACRES") or 0
            rows.append({
                "call": "RAWLAND",
                "source": "Raw Land",
                "price": attrs.get("LAND_MKT_VALUE") or 0,
                "address": attrs.get("PARCEL_ADD") or "Raw land",
                "city": attrs.get("PARCEL_CITY") or attrs.get("COUNTY_NAME") or county,
                "beds": 0, "baths": 0, "sqft": 0,
                "why": f"Public parcel. {acres:.1f} acres. {county} County.",
                "lat": lat, "lon": lon,
                "acres": acres,
                "img": random.choice(LAND_IMAGES),
            })
        print(f"{county}: {len(rows)}")
        return rows
    except Exception as e:
        print(f"{county} error: {e}")
        return []


def pull_hud_reo(limit=200):
    """Pull FHA/HUD REO properties in Utah from HUD eGIS."""
    url = "https://egis.hud.gov/arcgis/rest/services/cpdmaps/HudSfReo/MapServer/0/query"
    params = {
        "where": "STATE_CODE = 'UT'",
        "outFields": "ADDRESS,CITY,STATE_CODE,MAP_LATITUDE,MAP_LONGITUDE,CASE_NUM",
        "returnGeometry": "true",
        "f": "json",
        "resultRecordCount": limit,
    }
    try:
        r = requests.get(url, params=params, timeout=25)
        r.raise_for_status()
        features = r.json().get("features", [])
        rows = []
        for f in features:
            attrs = f.get("attributes", {})
            rows.append({
                "call": "REO",
                "source": "HUD REO",
                "price": 0,
                "address": (attrs.get("ADDRESS") or "HUD REO").strip(),
                "city": (attrs.get("CITY") or "Utah").strip(),
                "beds": 0, "baths": 0, "sqft": 0,
                "why": "HUD REO. Foreclosure inventory.",
                "lat": attrs.get("MAP_LATITUDE"),
                "lon": attrs.get("MAP_LONGITUDE"),
                "img": random.choice(LAND_IMAGES),
            })
        print(f"HUD REO: {len(rows)}")
        return rows
    except Exception as e:
        print(f"HUD REO error: {e}")
        return []


def pull_ksl_fsbo(limit=50):
    """Scrape KSL Classifieds FSBO / private real estate listings."""
    import re
    url = "https://classifieds.ksl.com/v2/search/cat/Other+Real+Estate/sellerType/Private/marketType/Sale"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        r.raise_for_status()
        # Simple regex extraction of titles and prices
        titles = re.findall(r'<a[^>]*href="/listing/\d+"[^>]*>([^<]+)</a>', r.text)
        prices = re.findall(r'\$([\d,]+\.\d{2})', r.text)
        rows = []
        for i, title in enumerate(titles[:limit]):
            price = float(prices[i].replace(",", "")) if i < len(prices) else 0
            rows.append({
                "call": "FSBO",
                "source": "FSBO",
                "price": price,
                "address": title.strip()[:80],
                "city": "Utah",
                "beds": 0, "baths": 0, "sqft": 0,
                "why": "KSL Classifieds private listing.",
                "lat": None, "lon": None,
                "img": random.choice(LAND_IMAGES),
            })
        print(f"KSL FSBO: {len(rows)}")
        return rows
    except Exception as e:
        print(f"KSL error: {e}")
        return []

def main():
    counties = ["Davis", "Utah", "Weber", "Cache", "Washington", "Tooele", "BoxElder", "Uintah", "Iron", "Kane", "Garfield", "Sanpete", "Sevier", "Millard", "Beaver"]
    rows = pull_slco_parcels() + pull_gov_parcels() + pull_hud_reo() + pull_ksl_fsbo()
    for c in counties:
        rows += pull_county_lir(c, limit=80)
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
