# Utah Land & Property — Desk ELO System

Autonomous neighborhood + agent ELO engine for Utah real estate.
Only **Active** listings are graded. The system refreshes itself on a schedule.

## Architecture

- `src/elo/` — Neighborhood and Agent ELO (persisted to `data/elo_state.json`)
- `src/feeds/` — WFRMLS (Active-only), FRED macro, local news
- `src/grade/cascade.py` — BUY / FADE / HOLD / DISTRESSED / STANDARD tree
- `src/autonomous.py` — Scheduler (15 min desk, 60 min macro/news, daily ELO)
- `src/api/routes.py` — FastAPI endpoints
- `web/` — Dark-theme desk UI
- `scripts/run_desk.py` — Single command to start everything

## Setup

1. Create `secrets.toml` (gitignored):

```toml
[wfrmls]
token = "YOUR_BEARER_TOKEN"
base_url = "https://resoapi.utahrealestate.com/reso/odata"

[fred]
api_key = "YOUR_FRED_KEY"  # free at https://fred.stlouisfed.org/docs/api/fred/
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run:

```bash
python scripts/run_desk.py
```

Open http://localhost:8000

Without a WFRMLS token the desk falls back to demo listings so the UI still renders.

## Rules

- Only `StandardStatus eq 'Active'` + fresh modification + ListPrice > 0 are shown.
- Free data sources only.
- PRs only — never push directly to main.

## Existing tools

The Streamlit dashboard (`dashboard.py`), PDF addendum engine, and shield library remain available.
