import asyncio
from core.event_log import EventLog
from datetime import datetime


async def main(config: dict, eventLog: EventLog):
    counter = 0
    await asyncio.sleep(20)
    while True:
        print(counter)
        if counter > 100:
            time = datetime.now().strftime("%H:%M %b %d")
            eventLog.add({"type": "time", "data": time, "notify_llm": True})
            counter = 0
        else:
            await asyncio.sleep(1)
            time = datetime.now().strftime("%H:%M %b %d")
            eventLog.add({"type": "time", "data": time})
            counter += 1
