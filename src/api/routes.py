"""FastAPI server for the Utah Land Desk."""
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pathlib import Path

from src.autonomous import desk_memory, neighborhoods, agents, macro

app = FastAPI(title="Utah Land Desk")

@app.get("/api/desk")
async def get_desk(city: str = Query(None)):
    if not desk_memory.get("rows"):
        return JSONResponse({"updated": "", "rows": [], "source": "loading", "macro": {}})
    rows = desk_memory["rows"]
    if city:
        rows = [r for r in rows if city.lower() in r.get("address", "").lower()]
    return {
        "updated": desk_memory.get("updated", ""),
        "source": desk_memory.get("source", "live"),
        "rows": rows,
        "macro": desk_memory.get("macro", {}),
    }

@app.get("/api/agents")
async def get_agents():
    return sorted(
        [{"id": a.id, "name": a.name, "elo": a.elo, "deals": a.deals_closed} for a in agents.values()],
        key=lambda a: abs(a["elo"] - 1500),
        reverse=True,
    )[:20]

@app.get("/api/macro")
async def get_macro():
    return macro.__dict__

@app.get("/api/health")
async def health():
    return {
        "ok": True,
        "desk_updated": desk_memory.get("updated", "never"),
        "listings": len(desk_memory.get("rows", [])),
        "neighborhoods": len(neighborhoods),
        "agents": len(agents),
    }

# Serve frontend if web/ exists
web_dir = Path(__file__).parent.parent.parent / "web"
if web_dir.exists():
    app.mount("/", StaticFiles(directory=str(web_dir), html=True), name="static")
