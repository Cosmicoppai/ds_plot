from typing import List, Tuple
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import defaultdict
import datetime
import time
from utils.logger import LOGGER


def plot_time_vs_status(data: List[Tuple[int, int]], output_file_name: str, time_window_in_hrs: int = 24, current_time=int(time.time()), timezone=datetime.timezone.utc, time_res_in_sec=120) -> None:
    """
    data : [(timestamp, http_status_code), ...] List of timestamp and http status code tuples
    output_file_name : "plot_output" (name of the output file)
    @time_window_in_hrs : 24 (size of time window in hours i.e the duration for which we want to plot graph)
    current_time : int(time.time()) (current time in epoch format, default is current time. It will be used as the end time for the graph)
    timezone : timezone as per the log file.To properly add legends in the graph
    time_res_in_sec : Resolution of time in seconds. Default is 120 seconds (2 minutes)
    """

    timestamps, http_status_codes = zip(*data)

    filtered_data = [(ts, code) for ts, code in zip(timestamps, http_status_codes) if (ts <= current_time and current_time - ts <= time_window_in_hrs * 3600)]

    if len(filtered_data) == 0:
        LOGGER.error("No data available for the given time window")
        return

    no_of_intervals_in_hr = 3600 // time_res_in_sec

    # Count the occurrences of each HTTP status code at each timestamp
    status_count_per_ts = defaultdict(lambda: np.zeros(time_window_in_hrs * no_of_intervals_in_hr + 1))  # no of resolution intervals in time_window

    for ts, code in filtered_data:
        try:
            time_diff = current_time - ts  # time difference in seconds between current time and the timestamp

            # calculate an index for each timestamp i.e. which interval it falls in
            ts_index = int((time_window_in_hrs * 3600 - time_diff) / time_res_in_sec)
            status_count_per_ts[code][ts_index] += 1
        except Exception as e:
            LOGGER.error(datetime.datetime.fromtimestamp(ts, timezone), datetime.datetime.fromtimestamp(current_time, timezone))
            LOGGER.error(ts_index, time_diff, code)
            LOGGER.error(e)

    fig, ax = plt.subplots()

    start_range = current_time - time_window_in_hrs * 3600
    step = time_res_in_sec
    end_range = current_time + step

    x = [datetime.datetime.fromtimestamp(ts, timezone) for ts in np.arange(start_range, end_range, step)]

    try:
        for code, counts in status_count_per_ts.items():
            ax.plot(x, counts, label=f'HTTP {code}')
    except Exception as e:
        LOGGER.error(e)

    ax.set_xlabel('Time')
    ax.set_ylabel('Status Count')
    ax.set_title(f'HTTP Status Codes vs. Time in the Last {time_window_in_hrs} Hours')
    ax.legend()

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M', timezone))

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    figure = plt.gcf()
    figure.set_size_inches(18.5, 10.5)

    figure.savefig(f'{output_file_name}.png', bbox_inches='tight', dpi=100)

    # Show the plot
    plt.show()
