import os
import time

import aiohttp

from utils.logger import setup_logger

logger = setup_logger("Pendo")

# TODO: Set the PENDO_INTEGRATION_KEY environment variable with your Pendo
# server-side Track Event secret (x-pendo-integration-key) to enable tracking.
PENDO_INTEGRATION_KEY = os.getenv("PENDO_INTEGRATION_KEY")
PENDO_TRACK_URL = "https://data.pendo.io/data/track"


async def track(event: str, visitor_id: str, account_id: str, properties: dict | None = None):
    """Send a server-side Track Event to the Pendo API."""
    if not PENDO_INTEGRATION_KEY:
        return

    payload = {
        "type": "track",
        "event": event,
        "visitorId": visitor_id,
        "accountId": account_id,
        "timestamp": int(time.time() * 1000),
    }
    if properties:
        payload["properties"] = properties

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                PENDO_TRACK_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "x-pendo-integration-key": PENDO_INTEGRATION_KEY,
                },
            ) as resp:
                if resp.status != 200:
                    logger.warning(f"Pendo track '{event}' returned status {resp.status}")
    except Exception as e:
        logger.warning(f"Pendo track '{event}' failed: {e}")
