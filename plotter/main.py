import argparse
from typing import List, Tuple
from utils.logger import LOGGER
from utils.plot import plot_time_vs_status
import time
from utils.timezone_helper import LogTimeZone
from pathlib import Path
from os import path
from io import BytesIO
import re
from datetime import datetime

TZ = LogTimeZone()

DEFAULT_DIR = Path(__file__).parent.joinpath('./logs')


def parse_apache_log(logs: str) -> List[Tuple[int, int]]:
    pattern = r'\[(.*?)\].*?HTTP\/1\.1" (\d{3})'
    matches = re.findall(pattern, logs)

    log_output = []

    for idx, match in enumerate(matches):
        try:
            if not match:
                continue

            _date = datetime.strptime(match[0], "%d/%b/%Y:%H:%M:%S %z")
            timestamp: int = int(_date.timestamp())
            status_code: int = int(match[1])
            log_output.append((timestamp, status_code))

            if idx == 0:
                TZ.time_zone_offset = int(_date.utcoffset().total_seconds())
        except Exception as e:
            LOGGER.error(f"Error parsing log line: {match} - {e}")
            log_output.append(("ERROR", "ERROR"))
            continue

    return log_output


def create_graph(file_name: str | Path = DEFAULT_DIR.joinpath('access.log'),
                 time_window: int = 24,
                 output: str = f"plot_output_{time.time()}.png",
                 current_time: int = int(time.time()),
                 time_res: int = 120, save_file: bool = False, show_plot: bool = False) -> BytesIO | Path:

    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name", required=False, help="Log File name to read logs", default=DEFAULT_DIR.joinpath('access.log'))
    parser.add_argument("--time_window", required=False, help="Size of time window", default=24, type=int)
    parser.add_argument("--output", required=False, help="Output file name", default=f"plot_output_{time.time()}.png")
    parser.add_argument("--current_time", required=False, help="current time in epoch format", default=int(time.time()), type=int)
    parser.add_argument("--time_res", required=False, help="Time Resolution in seconds", default=120, type=int)
    args = parser.parse_args()

    if not path.exists(args.file_name):
        LOGGER.error(f"File {args.filename} does not exists")
        raise FileNotFoundError(f"File {args.filename} does not exists")

    file_name = file_name or args.filename
    time_window = time_window or args.time_window
    output_file_name = output or args.output
    current_time = 1709334002 or current_time or args.current_time  # @TODO:@CosmicOppai Remove this hardcoded value
    time_res = time_res or args.time_res

    with open(file_name, "r") as file:
        file_data = file.read()
    parsed_log_data = parse_apache_log(file_data)
    parsed_log_data = list(filter(lambda x: x[0] != "ERROR" and x[1] != "ERROR", parsed_log_data))

    return plot_time_vs_status(parsed_log_data, output_file_name, time_window, current_time, TZ, time_res, save_file=save_file, show_plot=show_plot)


if __name__ == "__main__":
    create_graph(save_file=False, show_plot=True)
