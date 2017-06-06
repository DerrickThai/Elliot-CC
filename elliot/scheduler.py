import csv
from datetime import datetime, timedelta

from elliot.time_interval import TimeInterval


class Scheduler(object):
    def __init__(self, file_name):
        """
        Constructs an Scheduler with the given file name
        :type file_name: str
        """
        with open(file_name, "rb") as csv_file:
            rows = csv.reader(csv_file, delimiter=",", skipinitialspace=True)

            # Since we need to consider all users, we can ignore the user id field
            self.busy_times = [TimeInterval(start=row[1], end=row[2]) for row in rows if len(row) == 3]

    def longest_free_interval(self):
        """
        Finds the longest time interval in a single day that is free for all users to meet
            - interval will be between 8AM and 10PM
            - interval will be on days up to one week from the day this function is called
            - if there is not an interval that is free for all users, returns None
        :rtype: TimeInterval
        """
        # Make a copy of the busy times list and add edge intervals
        busy_times_of_week = self.busy_times
        self._add_edge_intervals(busy_times_of_week)

        # Remember the last interval of the week to know when to stop searching
        last_interval = busy_times_of_week[-1]

        # Sort the list by end time and then compare adjacent intervals
        #   - if they overlap, there is no free time between the intervals
        #   - otherwise, calculate the free time and keep track of the longest free time interval
        busy_times_of_week.sort()

        longest_interval = None
        longest_seconds = 0

        first_interval = busy_times_of_week[0]
        second_interval = busy_times_of_week[1]
        index = 1

        # Stop checking intervals once intervals are out of the current week
        while first_interval != last_interval:
            if first_interval.end < second_interval.start:
                free_time = (second_interval.start - first_interval.end).total_seconds()
                if free_time > longest_seconds:
                    longest_interval = TimeInterval(first_interval.end_str, second_interval.start_str)
                    longest_seconds = free_time

            # Look at the next adjacent intervals
            index += 1
            first_interval = second_interval
            if index < len(busy_times_of_week):
                second_interval = busy_times_of_week[index]

        return longest_interval

    @staticmethod
    def _add_edge_intervals(intervals):
        """
        Adds two busy intervals for the time before 8AM and the time after 10PM
            - does so for every day from today to the same day of the following week (1 + 7 = 8 days)
            - this is to handle cases where all users are not busy on a day
        :type intervals: [TimeInterval] 
        """
        now = datetime.now()
        for day in range(8):
            start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0)
            eight_am = datetime(now.year, now.month, now.day, 8, 0, 0)
            intervals.append(TimeInterval(start_of_day.strftime(TimeInterval.STRING_FORMAT),
                                          eight_am.strftime(TimeInterval.STRING_FORMAT)))

            next_day = now + timedelta(days=1)

            ten_pm = datetime(now.year, now.month, now.day, 22, 0, 0)
            end_of_day = datetime(now.year, now.month, next_day.day, 0, 0, 0)
            intervals.append(TimeInterval(ten_pm.strftime(TimeInterval.STRING_FORMAT),
                                          end_of_day.strftime(TimeInterval.STRING_FORMAT)))

            now = next_day
