import asyncio
from core.event_log import EventLog
from core.logger import Logger
import aiohttp
from datetime import datetime, timedelta

log = Logger()


async def main(config: dict, eventLog: EventLog):
    while True:
        async with aiohttp.ClientSession() as session:
            if config["baseUrl"].endswith("/"):
                base = config["baseUrl"][:-1]
            else:
                base = config["baseUrl"]

            dt = datetime.now() - timedelta(hours=2)

            async with session.get(
                base + "/api/logbook/" + dt.strftime("%Y-%m-%dT%H:%M:%S%z"),
                headers={"Authorization": "Bearer " + config["token"]},
            ) as response:
                log.info("Status: " + str(response.status))
                for event in await response.json():
                    if (
                        event["entity_id"] in config["entities"]
                        and event["state"] != "unavailable"
                    ):
                        log.info(event["entity_id"] + " - " + event["state"])
                        eventLog.add(
                            {
                                "type": "sensor_update",
                                "data": event["entity_id"] + "=" + event["state"],
                            }
                        )

        await asyncio.sleep(60 * 60)
