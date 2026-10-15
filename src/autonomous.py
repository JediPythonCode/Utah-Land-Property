"""
Autonomous Utah Land Desk engine.

Schedules:
- Every 15 min: refresh active listings + grades
- Every 60 min: macro + news
- Daily 6am MDT: ELO update from closed sales
- Daily 7am MDT: morning report (log only unless SMS configured)

Start with: python scripts/run_desk.py
"""
import asyncio
import logging
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from src.feeds.wfrmls import pull_active_listings, pull_closed_sales
from src.feeds.fred import fetch_all
from src.feeds.news import pull_news, filter_anomalies
from src.elo.neighborhood import Neighborhood, update_neighborhood, load_neighborhoods, save_neighborhoods
from src.elo.agent import Agent, update_agent, load_agents, save_agents
from src.elo.macro import MacroState, compute_macro
from src.grade.cascade import grade_property

logger = logging.getLogger("utah-desk")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")

neighborhoods: dict[str, Neighborhood] = {}
agents: dict[str, Agent] = {}
macro: MacroState = MacroState()
desk_memory: dict = {}
seen_listings: set[str] = set()
alert_history: dict[str, datetime] = {}
ALERT_COOLDOWN_HOURS = 24

async def refresh_desk():
    global desk_memory
    try:
        listings = pull_active_listings()
        rows = []
        for listing in listings:
            city = listing.get("City", "Unknown")
            hood = neighborhoods.get(city, Neighborhood(name=city, county=city, lat=40.7, lon=-111.9))
            agent_id = listing.get("ListingAgentId", "")
            agent = agents.get(agent_id, Agent(
                id=agent_id,
                name=listing.get("ListingAgentLastName", "Unknown"),
                office="Unknown",
            ))
            grade = grade_property(listing, hood, agent, macro)
            rows.append({
                "id": listing.get("ListingId"),
                "address": f"{listing.get('StreetName', '')}, {listing.get('City', '')}",
                "price": listing.get("ListPrice"),
                "status": listing.get("StandardStatus"),
                "grade": {
                    "call": grade.call,
                    "line": grade.line,
                    "why": grade.why,
                    "anomalies": grade.anomalies,
                    "weight": grade.weight,
                },
                "agent": {"name": agent.name, "elo": agent.elo},
                "neighborhood": {"name": hood.name, "elo": hood.elo, "expected": hood.expected_price_total},
            })
        order = {"DISTRESSED": 0, "BUY": 1, "FADE": 2, "HOLD": 3, "STANDARD": 4}
        rows.sort(key=lambda r: order.get(r["grade"]["call"], 9))
        desk_memory = {
            "updated": datetime.now(timezone.utc).isoformat(),
            "source": "live" if listings else "demo",
            "rows": rows,
            "macro": {
                "rate_30yr": macro.rate_30yr,
                "unemployment_ut": macro.unemployment_ut,
                "rates_rising": macro.rates_rising,
                "ue_rising": macro.ue_rising,
            },
        }
        logger.info(f"Desk refreshed: {len(rows)} active listings")
    except Exception as e:
        logger.error(f"Desk refresh failed: {e}")

async def refresh_macro_data():
    global macro
    try:
        fred_data = fetch_all()
        all_active = pull_active_listings()
        prior = desk_memory.get("inventory_prior", len(all_active))
        macro = compute_macro(fred_data, len(all_active), prior)
        desk_memory["inventory_prior"] = len(all_active)
        logger.info(f"Macro refreshed: rate={macro.rate_30yr:.2f}% UE={macro.unemployment_ut:.1f}%")
    except Exception as e:
        logger.error(f"Macro refresh failed: {e}")

async def refresh_news():
    try:
        articles = pull_news()
        anomalies = filter_anomalies(articles)
        macro.news_flags = [a["title"] for a in anomalies[:5]]
        if anomalies:
            logger.info(f"News flags: {[a['title'] for a in anomalies[:3]]}")
    except Exception as e:
        logger.error(f"News refresh failed: {e}")

async def update_elo_daily():
    try:
        sales = pull_closed_sales(days=1)
        for sale in sales:
            city = sale.get("City", "")
            price = sale.get("ListPrice", 0)
            sqft = sale.get("LivingArea", 0)
            if not city or price <= 0:
                continue
            hood = neighborhoods.get(city)
            if hood and sqft > 0:
                update_neighborhood(hood, price, sqft)
            agent_id = sale.get("ListingAgentId", "")
            agent = agents.get(agent_id)
            if agent:
                update_agent(agent, price, price, 30)
        save_neighborhoods(neighborhoods)
        save_agents(agents)
        logger.info(f"ELO updated from {len(sales)} closed sales")
    except Exception as e:
        logger.error(f"ELO update failed: {e}")

async def daily_report():
    rows = desk_memory.get("rows", [])
    buys = [r for r in rows if r["grade"]["call"] == "BUY"]
    logger.info(f"Morning brief: {len(buys)} BUY signals, {len(rows)} active listings, rate {macro.rate_30yr:.2f}%")

def create_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="America/Denver")
    scheduler.add_job(refresh_desk, IntervalTrigger(minutes=15), id="desk", max_instances=1)
    scheduler.add_job(refresh_macro_data, IntervalTrigger(minutes=60), id="macro", max_instances=1)
    scheduler.add_job(refresh_news, IntervalTrigger(minutes=60), id="news", max_instances=1)
    scheduler.add_job(update_elo_daily, CronTrigger(hour=6, minute=0), id="elo", max_instances=1)
    scheduler.add_job(daily_report, CronTrigger(hour=7, minute=0), id="report", max_instances=1)
    return scheduler

async def main():
    logger.info("=== UTAH LAND DESK — Autonomous Engine Starting ===")
    neighborhoods.clear()
    neighborhoods.update(load_neighborhoods())
    agents.clear()
    agents.update(load_agents())
    logger.info(f"Loaded {len(neighborhoods)} neighborhoods, {len(agents)} agents")
    await refresh_macro_data()
    await refresh_desk()
    await refresh_news()
    scheduler = create_scheduler()
    scheduler.start()
    logger.info("Scheduler running. Jobs: desk(15m), macro(60m), news(60m), elo(6am), report(7am)")
    try:
        while True:
            await asyncio.sleep(60)
    except asyncio.CancelledError:
        scheduler.shutdown()
        save_neighborhoods(neighborhoods)
        save_agents(agents)
