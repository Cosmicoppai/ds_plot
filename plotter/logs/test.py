import re
from datetime import datetime, timedelta

# Define the regex pattern
pattern = r'\[(\d{2})/(\w{3})/(\d{4}):(\d{2}):(\d{2}):(\d{2}) (\+\d{4})\].*?HTTP\/1\.1" (\d{3})'

# Read the log file
with open('access.log', 'r') as file:
    log_data = file.read()

# Use regex to find matches
matches = re.findall(pattern, log_data)

# Convert matches to timestamps
for match in matches:
    day, month, year, hour, minute, second, timezone_offset, status_code = match

    # Convert month abbreviation to month number
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_num = months.index(month) + 1

    # Create a datetime object without timezone info
    log_time = datetime(int(year), month_num, int(day), int(hour), int(minute), int(second))

    # Parse the timezone offset
    tz_hours = int(timezone_offset[1:3])
    tz_minutes = int(timezone_offset[3:])
    tz_offset = timedelta(hours=tz_hours, minutes=tz_minutes)
    break

    # Calculate the timestamp manually and adjust for the timezone offset
    timestamp = (log_time - datetime(1970, 1, 1)) // timedelta(seconds=1)
    if timezone_offset[0] == '-':
        timestamp += tz_hours * 3600 + tz_minutes * 60
    elif timezone_offset[0] == '+':
        timestamp -= tz_hours * 3600 + tz_minutes * 60

    print(f"Timestamp: {timestamp}, Status Code: {status_code}")
