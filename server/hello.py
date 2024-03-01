from sanic import Sanic, text, html, HTTPResponse, file, log
from os import path
from pathlib import Path
from .middleware import authorize
from plotter import IMG_DIR

app = Sanic("LogRate", configure_logging=True)

CURR_PATH = Path(__file__).parent

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
        log.logger.error(e)
        return text("We could not find index.html")


@app.get("/graphs")
async def get_graphs(request) -> HTTPResponse:
    try:
        with open(CURR_PATH.joinpath('./pics.html'), 'r', encoding="utf-8") as f:
            index_data = f.read()
        return html(index_data)
    except FileNotFoundError as e:
        log.logger.error(e)
        return text("We could not find index.html")


@app.route('/graph/<file_name>')
async def get_graph(request, file_name: str) -> HTTPResponse:
    _file = IMG_DIR.joinpath(f"{file_name}.png")
    if not path.exists(_file):
        return text('File does not exists')

    return await file(_file)
