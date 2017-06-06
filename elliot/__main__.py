from elliot.time_interval import TimeInterval
from scheduler import Scheduler


def main():
    # Read the CSV and determine the longest block of time in which all users are free to meet
    scheduler = Scheduler("../calendar.csv")
    longest_interval = scheduler.longest_free_interval()

    if longest_interval is None:
        print "There is no time from 8AM to 10PM on any day up to a week from today" \
              " in which all users are free to meet"
    else:
        print "The longest block of time that is free for all users to meet is" \
              " from {} to {}".format(longest_interval.start.strftime(TimeInterval.STRING_FORMAT),
                                      longest_interval.end.strftime(TimeInterval.STRING_FORMAT))


if __name__ == "__main__":
    main()
