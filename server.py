import os
import asyncio
import logging
import uuid
from datetime import datetime

from websockets import ConnectionClosed

from sanic import Sanic
from sanic.log import access_logger
from sanic.response import file, redirect


class PingFilter(logging.Filter):
    def filter(self, record):
        return not (record.request.endswith("?healthz") and record.status == 200)


access_logger.addFilter(PingFilter())

app = Sanic()
app.socks = []
app.static("/static", "./static")
app.static("/favicon.ico", "./static/favicon.ico")


@app.route("/")
async def index(_):
    return await file("index.html")


@app.route("/ws")
async def index(_):
    random_uuid = uuid.uuid4().hex
    return redirect(f"/ws/{random_uuid}")


@app.websocket("/ws/<uuid>")
async def time(request, ws, uuid):
    app.socks.append(ws)
    await ws.recv()
    await ws.send()


@app.listener("after_server_start")
async def producer(app, loop):
    while True:
        await asyncio.sleep(1)
        now = datetime.utcnow()

        if app.socks:
            print(f"Sending: {now} to {len(app.socks)} clients")
            for ws in app.socks:
                try:
                    await ws.send(f"{now}")
                except ConnectionClosed:
                    app.socks.remove(ws)


if __name__ == "__main__":
    DEBUG = bool(os.environ.get("DEBUG", False))
    app.run(host="0.0.0.0", port=8000, debug=DEBUG)
