from datetime import datetime
import os
from pathlib import Path
from aiohttp import web
import jinja2
from core.event_log import EventLog
from core.logger import Logger
import aiohttp_jinja2

log = Logger()


async def main(config: dict, eventLog: EventLog):
    async def render(request):
        dtformat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return aiohttp_jinja2.render_template(
            "render.html",
            request,
            {
                "title": eventLog.title,
                "subtitle": eventLog.subtitle,
                "dtformat": dtformat,
            },
        )

    async def pngRes(request):
        data = Path("data/dash.png").read_bytes()
        return web.Response(body=data, content_type="image/png")

    app = web.Application()
    app.add_routes([web.get("/", render)])
    app.add_routes([web.get("/render.png", pngRes)])

    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "data/html"))
    )
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=config["host"], port=int(config["port"]))
    await site.start()
    log.info("Websocket server started on %s:%s" % (config["host"], config["port"]))
