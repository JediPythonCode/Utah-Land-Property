"""
Run the entire Utah Land Desk:

  python scripts/run_desk.py

Starts the FastAPI server (port 8000) and the autonomous scheduler.
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import uvicorn
from src.autonomous import main as autonomous_main
from src.api.routes import app

async def run_all():
    auto_task = asyncio.create_task(autonomous_main())
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    try:
        await server.serve()
    finally:
        auto_task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(run_all())
    except KeyboardInterrupt:
        print("\nUtah Land Desk stopped.")
