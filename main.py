import argparse
from typing import List, Tuple
import logging
from apachelogs import LogParser
from utils.plot import plot_time_vs_status
import time


logging.basicConfig(filename='apache_parsing.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

PARSER = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")


def parse_apache_log(logs: List[str]) -> List[Tuple[int, int]]:
    log_output = []

    for log in logs:
        try:
            parsed_log = PARSER.parse(log)
            timestamp: int = int(parsed_log.request_time.timestamp())
            status_code: int = parsed_log.final_status
            log_output.append((int(timestamp), int(status_code)))
        except Exception as e:
            logging.error(f"Error parsing log line: {log} - {e}")
            log_output.append(("ERROR", "ERROR"))
            continue

    return log_output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", required=True, help="Log File name to read logs")
    parser.add_argument("--time_window", required=False, help="Size of time window")
    parser.add_argument("--output", required=False, help="Output file name")
    parser.add_argument("--current_time", required=False, help="current time in epoch format")
    args = parser.parse_args()

    file_name = args.filename
    output_file_name = args.output if args.output else "plot_output"
    time_window = int(args.time_window) if args.time_window else 24
    current_time = int(args.current_time) if args.current_time else int(time.time())

    with open(file_name, "r") as file:
        file_data = file.read()
    parsed_log_data = parse_apache_log(file_data.split("\n"))
    parsed_log_data = list(filter(lambda x: x[0] != "ERROR" and x[1] != "ERROR", parsed_log_data))

    # @TODO: @CosmicOppai Remove hardcoded current_time
    plot_time_vs_status(parsed_log_data, output_file_name, time_window, 1707499900)


if __name__ == "__main__":
    main()
