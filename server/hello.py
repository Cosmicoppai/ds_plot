from sanic import Sanic, text, html, HTTPResponse, file
from os import path
from pathlib import Path
from middleware import authorize
import logging


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

app = Sanic("LogRate")

CURR_PATH = Path(__file__).parent
IMG_DIR = CURR_PATH.parent.joinpath('plotter/graphs')

# register middleware
app.register_middleware(authorize, "request")  # attach this middleware to request

# Define a route to serve static files
app.static("/imgs", CURR_PATH.joinpath('./imgs'), )


@app.get("/")
async def index(request) -> HTTPResponse:
    try:
        with open(CURR_PATH.joinpath("./index.html"), 'r', encoding="utf-8") as f:
            index_data = f.read()
        return html(index_data)
    except FileNotFoundError as e:
        LOGGER.error(e)
        return text("We could not find index.html")


@app.get("/pics")
async def get_pics(request) -> HTTPResponse:
    try:
        with open(CURR_PATH.joinpath('./pics.html'), 'r', encoding="utf-8") as f:
            index_data = f.read()
        return html(index_data)
    except FileNotFoundError as e:
        LOGGER.error(e)
        return text("We could not find index.html")


@app.route('/images/<name>')
async def hello(request, file_name: str) -> HTTPResponse:

    _file = IMG_DIR.joinpath(f"{file_name}.png")
    if not path.exists(_file):
        return text('File does not exists')

    return await file(_file)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
