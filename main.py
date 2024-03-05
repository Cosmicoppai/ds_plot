from sys import path
from pathlib import Path

# include the plotter module in the root directory
path.append(Path(__file__).parent.joinpath('./plotter').__str__())
from server import app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, access_log=True)
