from typing import List, Tuple
from sys import argv
from datetime import datetime


def parse_apache_log(logs: List[str]) -> List[Tuple[str, str]]:
    log_output = []

    for log in logs:

        try:

            # Split the log line by spaces
            parts = log.split()
            # Extract timestamp,  and status code
            # convert the timestamp into time since epoch
            timestamp = datetime.strptime(parts[3][1:] + ' ' + parts[4][:-1], '%d/%b/%Y:%H:%M:%S %z').timestamp()
            status_code = parts[8]
            log_output.append((int(timestamp), int(status_code)))
        except Exception as e:
            print(e)
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
