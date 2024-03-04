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
from datetime import datetime, timedelta

TZ = LogTimeZone()

DEFAULT_DIR = Path(__file__).parent.joinpath('./logs')


def parse_apache_log(logs: str) -> List[Tuple[int, int]]:
    pattern = r'\[(\d{2})/(\w{3})/(\d{4}):(\d{2}):(\d{2}):(\d{2}) (\+\d{4})\].*?HTTP\/1\.1" (\d{3})'
    matches = re.findall(pattern, logs)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    log_output = []

    _time_start = datetime(1970, 1, 1)

    for idx, match in enumerate(matches):
        try:
            if not match:
                continue
            day, month, year, hour, minute, second, timezone_offset, status_code = match

            month_num = months.index(month) + 1

            _date = datetime(int(year), month_num, int(day), int(hour), int(minute), int(second))

            tz_offset = int(timezone_offset[1:3]) * 3600 + int(timezone_offset[3:]) * 60

            timestamp = (_date - _time_start) // timedelta(seconds=1)
            if timezone_offset[0] == '-':
                timestamp += tz_offset
            elif timezone_offset[0] == '+':
                timestamp -= tz_offset

            status_code: int = int(status_code)
            log_output.append((timestamp, status_code))

            if idx == 0:
                TZ.time_zone_offset = tz_offset
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
    current_time = current_time or args.current_time
    time_res = time_res or args.time_res

    with open(file_name, "r") as file:
        file_data = file.read()
    parsed_log_data = parse_apache_log(file_data)
    parsed_log_data = list(filter(lambda x: x[0] != "ERROR" and x[1] != "ERROR", parsed_log_data))

    return plot_time_vs_status(parsed_log_data, output_file_name, time_window, current_time, TZ, time_res, save_file=save_file, show_plot=show_plot)


if __name__ == "__main__":
    start = time.time()
    create_graph(save_file=False, show_plot=False)
    print(time.time() - start)
