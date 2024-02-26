from typing import List, Tuple
from sys import argv
import logging
from apachelogs import LogParser
from utils.plot import plot_time_vs_status


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


def _parse_args(_argv: List[str]) -> None:
    ...


if __name__ == "__main__":
    # read file name from command line
    file_name = argv[1]
    output_file_name = argv[2]
    time_window = int(argv[3]) if len(argv) > 3 else 24
    file_data = None
    with open(file_name, "r") as file:
        file_data = file.read()
    parsed_log_data = parse_apache_log(file_data.split("\n"))
    parsed_log_data = list(filter(lambda x: x[0] != "ERROR" and x[1] != "ERROR", parsed_log_data))
    plot_time_vs_status(parsed_log_data, output_file_name)
