#!/usr/bin/env python
"""
Contains all unit classes
"""
import datetime
import math

class Unit():
    """
    Base class for units.
    Used for Days, Hours inherits.
    """

    @staticmethod
    def get_hour():
        """
        Return the hour of the time
        """
        def get(time):
            # return event.start.hour
            return time.hour
        return get

    @staticmethod
    def get_day():
        """
        Return the weekday of the time
        """
        def get(time):
            # return event.start.weekday()
            return time.weekday()
        return get

    @staticmethod
    def get_month():
        """
        Return the month of the time
        """
        def get(time):
            return time.month - 1
        return get

    @staticmethod
    def get_week():
        """
        Return the week number of the time
        """
        def get(time):
            return time.isocalendar()[1]
        return get



    def __init__(self, event, get_x, get_y):
        self.start = self.create_dt(event, "start")
        self.end = self.create_dt_end(event)
        self.duration = self.end - self.start

        self.get_x = get_x()
        self.get_y = get_y()



    def create_dt(self, event, when):
        """
        create datetime object
        """
        hour = self.create_hour(event, when)
        day = int(event["date" + when][8:])
        month = int(event["date" + when][5:7])
        year = int(event["date" + when][:4])

        return datetime.datetime(hour=hour, day=day, month=month, year=year)



    def create_dt_end(self, event):
        """
        Creates datetime for evend end
        """
        end = self.create_dt(event, "end")
        round_up = self.create_timedelta()
        return end + round_up



    def create_hour(self, event, when):
        """
        Create hour for datetime

        Overriden in Hour class
        """
        return 0



    def calc_aoristic_value(self):
        """
        Calculate and return the aoristic value
        """
        time_span = self.get_duration()
        return round(1 / time_span, 3)



    def create_timedelta(self, days=1):
        """
        Creates a timedelta for round up of end datetime

        Overriden in Hour class
        """
        return datetime.timedelta(days=days)



    def get_duration(self):
        """
        Return events durations as days, rounded up.
        """
        #remove float?
        return float(self.duration.days)



    def __repr__(self):
        """
        Used in prints
        """
        return "Start: {start}\nEnd: {end}\nDuration: {dur}".format(start=self.start, end=self.end, dur=self.duration)



    # Generator method
    def __iter__(self):
        """
        Iterate over dates
        """
        while self.start < self.end:
            yield self.start
            self.start += self.create_timedelta()



class Hour(Unit):
    """
    Sub class of Unit for hours
    """

    def create_hour(self, event, when):
        """
        Create hour for datetime
        """
        return int(event["time" + when][:2])



    def create_timedelta(self, hours=1):
        """
        Creates a timedelta for round up of end datetime

        Overriden in Hour class
        """
        return datetime.timedelta(hours=hours)



    def get_duration(self):
        """
        Return events durations as hours, rounded up.
        """
        #remove float?
        return float(math.ceil((self.duration.total_seconds()/3600)))
