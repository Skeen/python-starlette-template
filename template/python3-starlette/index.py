# Copyright (c) Emil Madsen 2020. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.
import os

import uvicorn
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route

has_async_handler = False
try:
    from function import async_handler
    has_async_handler = True
except ImportError:
    from function import handler

# distutils.util.strtobool() can throw an exception
def is_true(val):
    return len(val) > 0 and val.lower() == "true" or val == "1"


async def main_route(request):
    raw_body = os.getenv("RAW_BODY", "false")

    as_text = True

    if is_true(raw_body):
        as_text = False

    body = await request.body()
    if as_text:
        body = body.decode("utf-8")

    if has_async_handler:
        ret = await async_handler.handle(body)
    else:
        ret = handler.handle(body)
    return Response(ret)


if __name__ == "__main__":
    routes = [
        Route("/", endpoint=main_route, methods=["GET", "POST"]),
        Route("/{full_path:path}", endpoint=main_route, methods=["GET", "POST"])
    ]
    app = Starlette(routes=routes)
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
