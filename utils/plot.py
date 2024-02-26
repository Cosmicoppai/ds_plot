from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import datetime
import time


def plot_time_vs_status(data: List[Tuple[int, int]], output_file_name: str, time_window: int = 24, current_time=int(time.time())) -> None:
    timestamps, http_status_codes = zip(*data)

    filtered_data = [(ts, code) for ts, code in zip(timestamps, http_status_codes) if (ts < current_time and current_time - ts <= time_window * 3600)]

    # Count the occurrences of each HTTP status code at each timestamp
    status_counts = defaultdict(lambda: np.zeros(time_window*30))  # no of 2 minute intervals in time_window hours

    for ts, code in filtered_data:
        try:
            time_diff = current_time - ts
            time_index = int((time_window * 3600 - time_diff) / 120)
            status_counts[code][time_index] += 1
        except Exception as e:
            print(datetime.datetime.fromtimestamp(ts), datetime.datetime.fromtimestamp(current_time))
            print(time_index, time_diff, e, code)

    fig, ax = plt.subplots()

    x = [datetime.datetime.fromtimestamp(ts) for ts in np.arange(current_time - time_window * 3600, current_time, 120)]
    for code, counts in status_counts.items():
        ax.plot(x, counts, label=f'HTTP {code}')

    ax.set_xlabel('Time')
    ax.set_ylabel('Status Count')
    ax.set_title(f'HTTP Status Codes vs. Time in the Last {time_window} Hours')
    ax.legend()

    # Save the plot as a PNG file
    plt.savefig(f'{output_file_name}.png')

    # Show the plot
    # plt.show()




