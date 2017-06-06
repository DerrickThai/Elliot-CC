from datetime import datetime


class TimeInterval(object):
    STRING_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, start, end):
        """
        Constructs a TimeInterval with the given start and end time
        :type start: str
        :type end: str
        """
        # Convert the strings into datetime objects to perform operations on them
        self.start = datetime.strptime(start, TimeInterval.STRING_FORMAT)
        self.end = datetime.strptime(end, TimeInterval.STRING_FORMAT)

        # Keep the original strings for printing
        self.start_str = start
        self.end_str = end

    def __cmp__(self, other):
        """
        Compares this TimeInterval with the given TimeInterval
            - the TimeInterval with the earliest end time is smaller
            - if emd times are equal, the TimeInterval with the earliest start time is smaller
        :type other: TimeInterval
        :rtype: int
        """
        if self.end == other.end:
            return (self.start - other.start).total_seconds()
        return (self.end - other.end).total_seconds()

    def __str__(self):
        """
        Returns a string representation of the TimeInterval
        :rtype: str
        """
        return "({}, {})".format(self.start_str, self.end_str)

    def __repr__(self):
        """
        Returns __str__ (used for printing lists of TimeIntervals)
        :rtype: str
        """
        return self.__str__()
