from sanic import Sanic, text, html, HTTPResponse, log
from pathlib import Path
from .middleware import authorize
from plotter import IMG_DIR, create_graph
from io import BytesIO
from .cache import lru_cache_ttl

app = Sanic("LogRate", configure_logging=True)

CURR_PATH = Path(__file__).parent
TEMPLATE_DIR = CURR_PATH.joinpath('./templates')
ASSETS_DIR = CURR_PATH.joinpath('./assets')

# register middleware
app.register_middleware(authorize, "request")  # attach this middleware to request

# Define a route to serve static files
app.static("/static", ASSETS_DIR, )


@app.get("/")
async def index(request) -> HTTPResponse:
    try:
        with open(TEMPLATE_DIR.joinpath("./index.html"), 'r', encoding="utf-8") as f:
            index_data = f.read()
        return html(index_data)
    except FileNotFoundError as e:
        log.logger.error(e)
        return text("We could not find index.html")


@app.get("/log_graph")
async def get_graphs(request) -> HTTPResponse:
    try:
        with open(TEMPLATE_DIR.joinpath('./pics.html'), 'r', encoding="utf-8") as f:
            index_data = f.read()
        return html(index_data)
    except FileNotFoundError as e:
        log.logger.error(e)
        return text("We could not find index.html")

@app.get("/graph")
async def get_latest_graph(request) -> HTTPResponse:
    try:
        # return serve the binary file
        _figure: BytesIO = _get_graph()
        return HTTPResponse(body=_figure.getvalue(), content_type="image/png", status=200)
    except FileNotFoundError as e:
        log.logger.error(e)
        return text(str(e))
    except ValueError as e:
        log.logger.error(e)
        return text(str(e))


@lru_cache_ttl()
def _get_graph() -> BytesIO:
    _figure: BytesIO = create_graph(save_file=False)
    return _figure
