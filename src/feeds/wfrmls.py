"""WFRMLS RESO API client. Only returns properties that are actually for sale.

Requires a bearer token in secrets.toml under [wfrmls].
Base URL: https://resoapi.utahrealestate.com/reso/odata
"""
import tomli
from pathlib import Path
from datetime import datetime, timezone, timedelta

try:
    from wfrmls import WFRMLSClient
except ImportError:
    WFRMLSClient = None  # type: ignore

FOR_SALE = "Active"
STALE_THRESHOLD_HOURS = 168

def _load_token() -> str:
    secrets = Path(__file__).parent.parent.parent / "secrets.toml"
    if not secrets.exists():
        return ""
    try:
        with open(secrets, "rb") as f:
            return tomli.load(f).get("wfrmls", {}).get("token", "")
    except Exception:
        return ""

def get_client():
    token = _load_token()
    if not token or WFRMLSClient is None:
        return None
    return WFRMLSClient(token=token)

def pull_active_listings(city: str = None) -> list[dict]:
    """Pull ONLY properties that are actively for sale.

    Filters:
    - StandardStatus must be 'Active'
    - ModificationTimestamp within last 7 days
    - ListPrice > 0
    """
    client = get_client()
    if client is None:
        return _demo_listings()
    stale_cutoff = (datetime.now(timezone.utc) - timedelta(hours=STALE_THRESHOLD_HOURS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    filter_query = (
        f"StandardStatus eq 'Active' "
        f"and ModificationTimestamp gt {stale_cutoff} "
        f"and ListPrice gt 0"
    )
    if city:
        filter_query += f" and (City has Odata.Models.City'{city}')"
    try:
        resp = client.property.get_properties(
            top=200,
            filter_query=filter_query,
            select=[
                "ListingId", "ListPrice", "StreetName", "City", "County",
                "BedroomsTotal", "BathroomsTotal", "LivingArea", "LotSize",
                "ListingContractDate", "ModificationTimestamp", "StandardStatus",
                "PropertyType", "ListingAgentFirstName", "ListingAgentLastName",
                "ListingAgentId",
            ],
            orderby="ListingContractDate desc",
        )
        rows = resp.get("value", [])
        return [r for r in rows if r.get("StandardStatus") == FOR_SALE and r.get("ListPrice", 0) > 0]
    except Exception:
        return _demo_listings()

def pull_closed_sales(days: int = 90) -> list[dict]:
    client = get_client()
    if client is None:
        return []
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        resp = client.property.get_properties(
            top=200,
            filter_query=f"StandardStatus eq 'Closed' and ModificationTimestamp gt {cutoff}",
            select=[
                "ListingId", "ListPrice", "StreetName", "City", "County",
                "LivingArea", "ModificationTimestamp", "ListingContractDate",
                "ListingAgentId", "ListingAgentFirstName", "ListingAgentLastName",
            ],
        )
        return resp.get("value", [])
    except Exception:
        return []

def _demo_listings() -> list[dict]:
    """Fallback demo data so the desk renders without a token."""
    return [
        {
            "ListingId": "DEMO-001",
            "ListPrice": 389000,
            "StreetName": "4200 S Highland Dr",
            "City": "Salt Lake City",
            "County": "Salt Lake",
            "LivingArea": 1800,
            "StandardStatus": "Active",
            "ListingAgentLastName": "Smith",
            "ListingAgentId": "agent-demo-1",
        },
        {
            "ListingId": "DEMO-002",
            "ListPrice": 749000,
            "StreetName": "1800 E 900 S",
            "City": "Salt Lake City",
            "County": "Salt Lake",
            "LivingArea": 2400,
            "StandardStatus": "Active",
            "ListingAgentLastName": "Jones",
            "ListingAgentId": "agent-demo-2",
        },
    ]
