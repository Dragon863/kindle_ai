import python_weather

import asyncio
import os

from core.event_log import EventLog
from datetime import datetime


async def main(config: dict, eventLog: EventLog):
    while True:
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            weather = await client.get(config["location"])
            eventLog.add(
                {
                    "type": "weather",
                    "data": {
                        "forecast_desc": weather.description,
                        "forecast_temp": weather.temperature,
                    },
                }
            )
        await asyncio.sleep(60 * 10)
