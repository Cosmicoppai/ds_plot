import argparse
from typing import List, Tuple
from utils.logger import LOGGER
from apachelogs import LogParser
from utils.plot import plot_time_vs_status
import time
from utils.timezone_helper import LogTimeZone


PARSER = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")

TZ = LogTimeZone()


def parse_apache_log(logs: List[str]) -> List[Tuple[int, int]]:
    log_output = []

    for idx, log in enumerate(logs):
        try:
            if not log:
                continue
            parsed_log = PARSER.parse(log)
            if idx == 0:
                TZ.time_zone_offset = int(parsed_log.request_time.utcoffset().total_seconds())

            timestamp: int = int(parsed_log.request_time.timestamp())
            status_code: int = parsed_log.final_status
            log_output.append((int(timestamp), int(status_code)))
        except Exception as e:
            LOGGER.error(f"Error parsing log line: {log} - {e}")
            log_output.append(("ERROR", "ERROR"))
            continue

    return log_output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", required=True, help="Log File name to read logs")
    parser.add_argument("--time_window", required=False, help="Size of time window", default=24)
    parser.add_argument("--output", required=False, help="Output file name", default="plot_output")
    parser.add_argument("--current_time", required=False, help="current time in epoch format", default=int(time.time()))
    parser.add_argument("--time_res", required=False, help="Time Resolution in seconds", default=120)
    args = parser.parse_args()

    file_name = args.filename
    output_file_name = args.output
    time_window = args.time_window
    current_time = args.current_time
    time_res = args.time_res

    with open(file_name, "r") as file:
        file_data = file.read()
    parsed_log_data = parse_apache_log(file_data.split("\n"))
    parsed_log_data = list(filter(lambda x: x[0] != "ERROR" and x[1] != "ERROR", parsed_log_data))

    # @TODO: @CosmicOppai Remove hardcoded current_time
    plot_time_vs_status(parsed_log_data, output_file_name, time_window, 1707519602, TZ, time_res)


if __name__ == "__main__":
    main()
