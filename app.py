#!/usr/bin/env python

import asyncio
import http
import signal
from websockets.asyncio.server import serve


async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)


def health_check(connection, request):
    # Respond to health check only if the path matches
    if request.path == "/healthz":
        return connection.respond(http.HTTPStatus.OK, "OK\n")
    # For other requests, do not respond (to avoid HEAD requests)
    return connection.respond(http.HTTPStatus.METHOD_NOT_ALLOWED, "Method Not Allowed\n")


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with serve(
        echo,
        host="",
        port=8080,
        process_request=health_check,
    ):
        await stop


if __name__ == "__main__":
    asyncio.run(main())