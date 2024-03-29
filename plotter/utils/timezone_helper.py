from datetime import timedelta, tzinfo


class LogTimeZone(tzinfo):
    """
    A class to represent the timezone of the log file.
    """
    def __init__(self, time_zone_offset: int = 0):
        self.time_zone_offset = time_zone_offset
        super().__init__()

    def utcoffset(self, dt):
        return timedelta(seconds=self.time_zone_offset)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        # @TODO: @CosmicOppai: Implement this to return the timezone name
        return "UTC"
