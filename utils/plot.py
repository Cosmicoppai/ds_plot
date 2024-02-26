from typing import List, Tuple
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import defaultdict
import datetime
import time
from utils.logger import LOGGER


def plot_time_vs_status(data: List[Tuple[int, int]], output_file_name: str, time_window: int = 24, current_time=int(time.time()), timezone=datetime.timezone.utc) -> None:
    timestamps, http_status_codes = zip(*data)

    filtered_data = [(ts, code) for ts, code in zip(timestamps, http_status_codes) if (ts <= current_time and current_time - ts <= time_window * 3600)]

    # Count the occurrences of each HTTP status code at each timestamp
    status_counts = defaultdict(lambda: np.zeros(time_window*30 + 1))  # no of 2 minute intervals in time_window hours

    for ts, code in filtered_data:
        try:
            time_diff = current_time - ts
            time_index = int((time_window * 3600 - time_diff) / 120)
            status_counts[code][time_index] += 1
        except Exception as e:
            LOGGER.error(datetime.datetime.fromtimestamp(ts, timezone), datetime.datetime.fromtimestamp(current_time, timezone))
            LOGGER.error(time_index, time_diff, code)
            LOGGER.error(e)

    fig, ax = plt.subplots()

    start_range = current_time - time_window * 3600
    step = 120  # 2 minutes
    end_range = current_time + step

    x = [datetime.datetime.fromtimestamp(ts, timezone) for ts in np.arange(start_range, end_range, step)]

    try:
        for code, counts in status_counts.items():
            ax.plot(x, counts, label=f'HTTP {code}')
    except Exception as e:
        print(e)

    ax.set_xlabel('Time')
    ax.set_ylabel('Status Count')
    ax.set_title(f'HTTP Status Codes vs. Time in the Last {time_window} Hours')
    ax.legend()

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M', timezone))

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    figure = plt.gcf()
    figure.set_size_inches(18.5, 10.5)

    figure.savefig('test.png', bbox_inches='tight', dpi=100)

    # Show the plot
    plt.show()




