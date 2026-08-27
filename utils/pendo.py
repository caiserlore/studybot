import os
import time

import aiohttp

from utils.logger import setup_logger

logger = setup_logger("Pendo")

# TODO: Set PENDO_TRACK_EVENT_SECRET environment variable with your Pendo
# integration key. This is required for server-side track events to reach Pendo.
PENDO_TRACK_URL = "https://data.pendo.io/data/track"


async def track(
    event: str, visitor_id: str, account_id: str, properties: dict | None = None
):
    integration_key = os.getenv("PENDO_TRACK_EVENT_SECRET")
    if not integration_key:
        logger.warning("PENDO_TRACK_EVENT_SECRET not set; skipping track event: %s", event)
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
        async with (
            aiohttp.ClientSession() as session,
            session.post(
                PENDO_TRACK_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "x-pendo-integration-key": integration_key,
                },
            ) as resp,
        ):
            if resp.status >= 400:
                body = await resp.text()
                logger.error(f"Pendo track error {resp.status} for '{event}': {body}")
    except Exception as e:  # noqa: BLE001
        logger.error(f"Pendo track request failed for '{event}': {e}")
