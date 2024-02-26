from typing import List, Tuple
from sys import argv
import logging
from apachelogs import LogParser


logging.basicConfig(filename='apache_parsing.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

PARSER = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")


def parse_apache_log(logs: List[str]) -> List[Tuple[str, str]]:
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


if __name__ == "__main__":
    # read file name from command line
    file_name = argv[1]
    file_data = None
    with open(file_name, "r") as file:
        file_data = file.read()
    log_data = parse_apache_log(file_data.split("\n"))
    print(log_data)
