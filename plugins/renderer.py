import asyncio
import os
from pyppeteer import launch
from core.event_log import EventLog


async def main(config: dict, eventLog: EventLog):
    while True:
        URL = config["url"]

        browser = await launch(
            args=["--no-sandbox", "--disable-setuid-sandbox"],
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False,
        )

        page = await browser.newPage()

        # Kindle 4 NT resolution
        await page.setViewport({"width": 600, "height": 800})

        await page.goto(URL, {"waitUntil": "networkidle2"})

        # This is a bit silly. ¯\_(ツ)_/¯
        # Networkidle2 doesn't always seem to wait long enough.
        await asyncio.sleep(3)

        await page.screenshot({"path": "data/dash.png"})

        await browser.close()

        # Convert to grayscale 8-bit
        os.system("convert data/dash.png -colorspace Gray data/dash.png ")

        await asyncio.sleep(60)
