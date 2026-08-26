import time

import aiohttp

from utils.logger import setup_logger

logger = setup_logger("Pendo")

PENDO_TRACK_URL = "https://data.pendo.io/data/track"
PENDO_INTEGRATION_KEY = "26f7185f-41a8-44bd-9a73-90a885e28aca"


async def track(
    event: str, visitor_id: str, account_id: str, properties: dict | None = None
):
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
                    "x-pendo-integration-key": PENDO_INTEGRATION_KEY,
                },
            ) as resp,
        ):
            if resp.status >= 400:
                body = await resp.text()
                logger.error(f"Pendo track error {resp.status} for '{event}': {body}")
    except Exception as e:  # noqa: BLE001
        logger.error(f"Pendo track request failed for '{event}': {e}")
