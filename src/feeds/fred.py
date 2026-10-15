"""FRED data pulls. All series IDs confirmed as of design time."""
import httpx
import tomli
from pathlib import Path

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"

SERIES = {
    "rate_30yr": "MORTGAGE30US",
    "unemployment_ut": "UTUR",
    "hpi_utah": "UTSTHPI",
    "hpi_slc_msa": "ATNHPIUS41620Q",
    "hpi_utah_county": "ATNHPIUS49049A",
    "hpi_sl_county": "ATNHPIUS49035A",
    "hpi_st_george": "ATNHPIUS41100Q",
    "median_list_price_ut": "MEDLISPRIUT",
    "median_dom_sl_county": "MEDDAYONMAR49035",
    "median_dom_ut_county": "MEDDAYONMAR49049",
    "construction_employment": "UTCONS",
}

def _fred_key() -> str:
    secrets = Path(__file__).parent.parent.parent / "secrets.toml"
    if not secrets.exists():
        return ""
    try:
        with open(secrets, "rb") as f:
            return tomli.load(f).get("fred", {}).get("api_key", "")
    except Exception:
        return ""

def fetch_series(series_id: str, limit: int = 31) -> list[dict]:
    key = _fred_key()
    if not key:
        return []
    try:
        resp = httpx.get(
            FRED_BASE,
            params={"series_id": series_id, "api_key": key, "file_type": "json", "sort_order": "asc", "limit": limit},
            timeout=10,
        )
        if resp.status_code != 200:
            return []
        return [
            {"date": o["date"], "value": float(o["value"])}
            for o in resp.json().get("observations", [])
            if o.get("value") != "."
        ]
    except Exception:
        return []

def fetch_all() -> dict[str, list[dict]]:
    return {name: fetch_series(sid) for name, sid in SERIES.items()}
